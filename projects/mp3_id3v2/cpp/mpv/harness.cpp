#include "harness.h"
#include <mpv/client.h>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <string>
#include <utility>
#include <fcntl.h>
#include <unistd.h>

namespace {

constexpr std::size_t max_input = 1u << 20;

// The input is written to a private local file because the selected API is
// libmpv's loadfile command on a local path; the file is removed on every
// return path, after the player that read it has been destroyed.
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

private:
    char path_[32] = "/tmp/parsarium-mpv-XXXXXX.mp3";
    bool created_ = false, written_ = false;
};

#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
// AFL++ defines this macro; upstream mpv accepts fuzzing file streams only
// through descriptor 42. Keep it open until the player is destroyed.
class fuzz_fd {
public:
    explicit fuzz_fd(const char *path) {
        int source = open(path, O_RDONLY | O_CLOEXEC);
        if (source < 0) return;
        if (source != 42) {
            if (dup2(source, 42) != 42) { close(source); return; }
            close(source);
        }
        ready_ = true;
    }
    ~fuzz_fd() { if (ready_) close(42); }
    bool ok() const { return ready_; }
private:
    bool ready_ = false;
};
#endif

struct player_destroy { void operator()(mpv_handle *mpv) const { mpv_terminate_destroy(mpv); } };
struct mpv_string_free { void operator()(char *text) const { mpv_free(text); } };
using player = std::unique_ptr<mpv_handle, player_destroy>;

std::string property(mpv_handle *mpv, const char *name) {
    std::unique_ptr<char, mpv_string_free> value(mpv_get_property_string(mpv, name));
    return value ? std::string(value.get()) : std::string();
}

}  // namespace

// The catalog call site: a local tagged MP3 path through loadfile, FILE_LOADED,
// then the ID3v2 title, the first track's codec and the duration. Options match
// projects/mp3_id3v2/c/mpv: no config, null audio/video outputs, paused
// playback, so only loading is observed.
bool parsarium_parse_mp3(const std::uint8_t *data, std::size_t size, parsarium_mp3_result &result) {
    result = parsarium_mp3_result{};
    if (!data || !size || size > max_input) return false;
    temp_file file(data, size);
    if (!file.ok()) return false;
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
    fuzz_fd input(file.path());
    if (!input.ok()) return false;
#endif
    player mpv(mpv_create());
    if (!mpv) return false;
    for (const auto &option : {std::make_pair("config", "no"), std::make_pair("ao", "null"),
                               std::make_pair("vo", "null"), std::make_pair("pause", "yes"),
                               std::make_pair("vid", "no"), std::make_pair("aid", "no"),
                               std::make_pair("track-auto-selection", "no"),
                               std::make_pair("video-osd", "no"),
                               std::make_pair("input-builtin-bindings", "no")})
        if (mpv_set_option_string(mpv.get(), option.first, option.second) < 0) return false;
    if (mpv_initialize(mpv.get()) < 0) return false;
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
    const char *command[] = {"loadfile", "fd://42", nullptr};
#else
    const char *command[] = {"loadfile", file.path(), nullptr};
#endif
    if (mpv_command(mpv.get(), command) < 0) return false;
    bool loaded = false;
    for (int i = 0; i < 20 && !loaded; ++i) {
        const mpv_event *event = mpv_wait_event(mpv.get(), 0.5);
        if (event->event_id == MPV_EVENT_FILE_LOADED) loaded = true;
        else if (event->event_id == MPV_EVENT_END_FILE || event->event_id == MPV_EVENT_SHUTDOWN) break;
    }
    if (!loaded) return false;
    result.title = property(mpv.get(), "metadata/by-key/title");
    if (property(mpv.get(), "track-list/0/type") != "audio") return false;
    result.codec = property(mpv.get(), "track-list/0/codec");
    double duration = 0;
    if (mpv_get_property(mpv.get(), "duration", MPV_FORMAT_DOUBLE, &duration) < 0) return false;
    // Range check first: converting an out-of-range double is undefined and
    // would be reported by UBSan as a harness fault, not a parser result.
    if (!std::isfinite(duration) || duration <= 0 || duration > 1e9) return false;
    result.duration_ms = std::llround(duration * 1000.0);
    return !result.codec.empty();
}
