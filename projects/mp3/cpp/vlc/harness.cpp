#include "harness.h"
#include <vlc/vlc.h>
#include <chrono>
#include <condition_variable>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <mutex>
#include <unistd.h>

// libvlccore is linked statically with dynamic plugins disabled, so its module
// bank registers plugins from this table instead of loading them from disk.
// These are the five plugins on VLC's local MP3 preparse path: file access, the
// ID3/APE tag-skipping stream filter, the MPEG audio ES demuxer (which parses the
// skipped ID3v2 tag with VLC's native ID3 headers), its MPEG audio packetizer,
// and the TagLib meta reader. The table needs C linkage: src/modules/bank.c
// declares it as a weak C symbol.
extern "C" {
typedef int (*parsarium_vlc_plugin_cb)(int (*)(void *, void *, int, ...), void *);
int vlc_entry__filesystem(int (*)(void *, void *, int, ...), void *);
int vlc_entry__skiptags(int (*)(void *, void *, int, ...), void *);
int vlc_entry__es(int (*)(void *, void *, int, ...), void *);
int vlc_entry__mpegaudio(int (*)(void *, void *, int, ...), void *);
int vlc_entry__taglib(int (*)(void *, void *, int, ...), void *);
__attribute__((visibility("default")))
parsarium_vlc_plugin_cb vlc_static_modules[] = {
    vlc_entry__filesystem, vlc_entry__skiptags, vlc_entry__es,
    vlc_entry__mpegaudio, vlc_entry__taglib, nullptr};
}

namespace {

constexpr std::size_t max_input = 1u << 20;
// VLC_CODEC_MP3: the ES demuxer reports MPEG audio Layer III as 'mp3 '.
constexpr std::uint32_t codec_mp3 = 0x2033706d;

struct parse_wait {
    std::mutex lock;
    std::condition_variable done;
    int status = 0;
};

void parsed_changed(const libvlc_event_t *event, void *opaque) {
    auto *wait = static_cast<parse_wait *>(opaque);
    std::lock_guard<std::mutex> guard(wait->lock);
    wait->status = event->u.media_parsed_changed.new_status;
    wait->done.notify_one();
}

// The input is written to a private local file because the selected API is
// libVLC's local-path media parser; the file is removed on every return path.
// The .mp3 suffix matters: TagLib's FileRef picks MPEG::File by extension.
class temp_file {
public:
    temp_file(const std::uint8_t *data, std::size_t size) {
        int fd = mkstemps(path_, 4);
        if (fd < 0) return;
        created_ = true;
        std::size_t offset = 0;
        while (offset < size) {
            ssize_t n = write(fd, data + offset, size - offset);
            if (n <= 0) break;
            offset += static_cast<std::size_t>(n);
        }
        bool complete = offset == size;
        written_ = close(fd) == 0 && complete;
    }
    ~temp_file() { if (created_) unlink(path_); }
    temp_file(const temp_file &) = delete;
    temp_file &operator=(const temp_file &) = delete;
    bool ok() const { return written_; }
    const char *path() const { return path_; }
    const char *name() const { return std::strrchr(path_, '/') + 1; }

private:
    char path_[32] = "/tmp/parsarium-XXXXXX.mp3";
    bool created_ = false, written_ = false;
};

struct media_release { void operator()(libvlc_media_t *media) const { libvlc_media_release(media); } };
struct vlc_string_free { void operator()(char *text) const { libvlc_free(text); } };

std::string fourcc(std::uint32_t codec) {
    std::string out(4, '?');
    for (int i = 0; i < 4; ++i) {
        unsigned char c = static_cast<unsigned char>(codec >> (8 * i));
        if (c >= 32 && c < 127) out[i] = static_cast<char>(c);
    }
    return out;
}

libvlc_instance_t *instance() {
    // No configuration file, no network metadata lookups, no outputs.
    static libvlc_instance_t *const vlc = [] {
        const char *args[] = {"--ignore-config", "--no-metadata-network-access",
                              "--no-video", "--no-audio", "--no-stats"};
        return libvlc_new(sizeof(args) / sizeof(args[0]), args);
    }();
    return vlc;
}

}  // namespace

bool parsarium_parse_mp3(const std::uint8_t *data, std::size_t size, parsarium_mp3_result &result) {
    result = parsarium_mp3_result{};
    if (!data || !size || size > max_input) return false;
    libvlc_instance_t *vlc = instance();
    if (!vlc) return false;
    temp_file file(data, size);
    if (!file.ok()) return false;
    std::unique_ptr<libvlc_media_t, media_release> media(libvlc_media_new_path(vlc, file.path()));
    if (!media) return false;
    parse_wait wait;
    libvlc_event_manager_t *events = libvlc_media_event_manager(media.get());
    if (libvlc_event_attach(events, libvlc_MediaParsedChanged, parsed_changed, &wait)) return false;
    bool ok = false;
    if (libvlc_media_parse_with_options(media.get(), libvlc_media_parse_local, 5000) == 0) {
        int status;
        {
            std::unique_lock<std::mutex> guard(wait.lock);
            wait.done.wait_for(guard, std::chrono::seconds(6), [&] { return wait.status != 0; });
            status = wait.status;
        }
        if (status == libvlc_media_parsed_status_done) {
            // Without title metadata libVLC returns the item name, which here is
            // the random temporary file name; report no title instead.
            std::unique_ptr<char, vlc_string_free> title(libvlc_media_get_meta(media.get(), libvlc_meta_Title));
            if (title && std::strcmp(title.get(), file.name()) != 0) result.title = title.get();
            libvlc_media_track_t **tracks = nullptr;
            unsigned count = libvlc_media_tracks_get(media.get(), &tracks);
            for (unsigned i = 0; i < count; ++i) {
                const libvlc_media_track_t &track = *tracks[i];
                if (track.i_type != libvlc_track_audio) continue;
                if (track.i_codec == codec_mp3) ++result.mp3_tracks;
                if (!result.audio_tracks++) {
                    result.audio_codec = fourcc(track.i_codec);
                    result.rate = track.audio->i_rate;
                    result.channels = track.audio->i_channels;
                }
            }
            if (count) libvlc_media_tracks_release(tracks, count);
            ok = count > 0;
        }
    }
    // Parsing runs on libVLC's preparser thread; stop it before the wait state
    // leaves scope.
    libvlc_media_parse_stop(media.get());
    libvlc_event_detach(events, libvlc_MediaParsedChanged, parsed_changed, &wait);
    return ok;
}
