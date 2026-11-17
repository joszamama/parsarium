#include "harness.h"
#include <mpv/client.h>
#include <cstdio>
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
    char path_[32] = "/tmp/parsarium-mpv-XXXXXX.mp4";
    bool created_ = false, written_ = false;
};

#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
// mpv's upstream fuzzing build accepts file streams only through descriptor 42.
// Keep it open until after the player is destroyed; the same FFmpeg MOV parser
// receives the bytes through mpv's documented fd:// stream route.
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

std::string property(mpv_handle *mpv, const std::string &name) {
    std::unique_ptr<char, mpv_string_free> value(mpv_get_property_string(mpv, name.c_str()));
    return value ? std::string(value.get()) : std::string();
}

}  // namespace

// The catalog call site: a local MP4 path through loadfile, FILE_LOADED, then
// the demuxer, title and first video/audio codec properties. Options match
// projects/mp4/c/mpv: no config, null audio/video outputs, paused playback,
// so only loading is observed.
bool parsarium_parse_mp4(const std::uint8_t *data, std::size_t size, parsarium_mp4_result &result) {
    result = parsarium_mp4_result{};
    if (!data || !size || size > max_input) return false;
    temp_file file(data, size);
    if (!file.ok()) { if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "temp-file failed\n"); return false; }
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
    fuzz_fd input(file.path());
    if (!input.ok()) return false;
#endif
    player mpv(mpv_create());
    if (!mpv) { if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "mpv_create failed\n"); return false; }
    for (const auto &option : {std::make_pair("config", "no"), std::make_pair("ao", "null"),
                               std::make_pair("vo", "null"), std::make_pair("pause", "yes"),
                               std::make_pair("vid", "no"), std::make_pair("aid", "no"),
                               std::make_pair("track-auto-selection", "no"),
                               std::make_pair("video-osd", "no"),
                               std::make_pair("input-builtin-bindings", "no")})
        if (int rc = mpv_set_option_string(mpv.get(), option.first, option.second); rc < 0) {
            if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "option %s: %s\n", option.first, mpv_error_string(rc));
            return false;
        }
    if (int rc = mpv_initialize(mpv.get()); rc < 0) {
        if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "initialize: %s\n", mpv_error_string(rc));
        return false;
    }
    if (std::getenv("PARSARIUM_DEBUG")) mpv_request_log_messages(mpv.get(), "debug");
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
    const char *command[] = {"loadfile", "fd://42", nullptr};
#else
    const char *command[] = {"loadfile", file.path(), nullptr};
#endif
    if (int rc = mpv_command(mpv.get(), command); rc < 0) {
        if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "loadfile: %s\n", mpv_error_string(rc));
        return false;
    }
    bool loaded = false;
    for (int i = 0; i < (std::getenv("PARSARIUM_DEBUG") ? 200 : 20) && !loaded; ++i) {
        const mpv_event *event = mpv_wait_event(mpv.get(), std::getenv("PARSARIUM_DEBUG") ? 0.05 : 0.5);
        if (std::getenv("PARSARIUM_DEBUG")) {
            std::fprintf(stderr, "event: %d\n", event->event_id);
            if (event->event_id == MPV_EVENT_LOG_MESSAGE && event->data) {
                const auto *message = static_cast<const mpv_event_log_message *>(event->data);
                std::fprintf(stderr, "mpv %s: %s", message->prefix, message->text);
            }
            if (event->event_id == MPV_EVENT_END_FILE && event->data) {
                const auto *end = static_cast<const mpv_event_end_file *>(event->data);
                std::fprintf(stderr, "end-file reason=%d error=%s\n", end->reason, mpv_error_string(end->error));
            }
        }
        if (event->event_id == MPV_EVENT_FILE_LOADED) loaded = true;
        else if (event->event_id == MPV_EVENT_END_FILE || event->event_id == MPV_EVENT_SHUTDOWN) break;
    }
    if (!loaded) { if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "file not loaded\n"); return false; }
    result.container = property(mpv.get(), "file-format");
    result.title = property(mpv.get(), "metadata/by-key/title");
    std::int64_t count = 0;
    if (mpv_get_property(mpv.get(), "track-list/count", MPV_FORMAT_INT64, &count) < 0) {
        if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "track list unavailable\n");
        return false;
    }
    for (std::int64_t i = 0; i < count && i < 64; ++i) {
        const std::string track = "track-list/" + std::to_string(i) + "/";
        const std::string type = property(mpv.get(), track + "type");
        if (type == "video" && result.video_codec.empty())
            result.video_codec = property(mpv.get(), track + "codec");
        else if (type == "audio" && result.audio_codec.empty())
            result.audio_codec = property(mpv.get(), track + "codec");
    }
    if (std::getenv("PARSARIUM_DEBUG")) std::fprintf(stderr, "result: container=%s video=%s audio=%s\n", result.container.c_str(), result.video_codec.c_str(), result.audio_codec.c_str());
    return !result.container.empty() && !result.video_codec.empty() && !result.audio_codec.empty();
}
