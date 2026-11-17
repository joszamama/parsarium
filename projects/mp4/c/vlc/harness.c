#include "harness.h"
#include <vlc/vlc.h>
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

/* libvlccore is linked statically with dynamic plugins disabled, so it
   registers plugins from this table instead of loading them from disk. Only
   the file access and VLC's own MP4 demuxer are present; no other demuxer can
   claim the input. */
typedef int (*parsarium_vlc_plugin_cb)(int (*)(void *, void *, int, ...), void *);
int vlc_entry__filesystem(int (*)(void *, void *, int, ...), void *);
int vlc_entry__mp4(int (*)(void *, void *, int, ...), void *);
__attribute__((visibility("default")))
parsarium_vlc_plugin_cb vlc_static_modules[] = { vlc_entry__filesystem, vlc_entry__mp4, NULL };

struct parse_wait {
    pthread_mutex_t lock;
    pthread_cond_t done;
    int status;
};

static void parsed_changed(const libvlc_event_t *event, void *opaque) {
    struct parse_wait *wait = opaque;
    pthread_mutex_lock(&wait->lock);
    wait->status = event->u.media_parsed_changed.new_status;
    pthread_cond_signal(&wait->done);
    pthread_mutex_unlock(&wait->lock);
}

static void fourcc(uint32_t codec, char out[5]) {
    for (int i = 0; i < 4; i++) {
        unsigned char c = (unsigned char)(codec >> (8 * i));
        out[i] = c >= 32 && c < 127 ? (char)c : '?';
    }
    out[4] = '\0';
}

static libvlc_instance_t *instance(void) {
    static libvlc_instance_t *vlc;
    if (!vlc) {
        /* No configuration file, no network metadata lookups, no outputs. */
        const char *args[] = {"--ignore-config", "--no-metadata-network-access",
                              "--no-video", "--no-audio", "--no-stats"};
        vlc = libvlc_new(sizeof(args) / sizeof(args[0]), args);
    }
    return vlc;
}

int parsarium_parse(const uint8_t *data, size_t size, struct parsarium_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    libvlc_instance_t *vlc = instance();
    if (!vlc) return 0;
    char path[] = "/tmp/parsarium-XXXXXX.mp4";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    libvlc_media_t *media = libvlc_media_new_path(vlc, path);
    if (!media) { unlink(path); return 0; }
    struct parse_wait wait = {PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, 0};
    libvlc_event_manager_t *events = libvlc_media_event_manager(media);
    libvlc_event_attach(events, libvlc_MediaParsedChanged, parsed_changed, &wait);
    int ok = 0;
    if (libvlc_media_parse_with_options(media, libvlc_media_parse_local, 5000) == 0) {
        struct timespec deadline;
        clock_gettime(CLOCK_REALTIME, &deadline);
        deadline.tv_sec += 6;
        pthread_mutex_lock(&wait.lock);
        while (!wait.status && pthread_cond_timedwait(&wait.done, &wait.lock, &deadline) != ETIMEDOUT) {}
        int status = wait.status;
        pthread_mutex_unlock(&wait.lock);
        if (status == libvlc_media_parsed_status_done) {
            /* Without title metadata libVLC returns the item name, which here
               is the random temporary file name; report no title instead. */
            char *title = libvlc_media_get_meta(media, libvlc_meta_Title);
            if (title && strcmp(title, strrchr(path, '/') + 1) && strlen(title) < sizeof(result->title))
                memcpy(result->title, title, strlen(title) + 1);
            libvlc_free(title);
            libvlc_media_track_t **tracks = NULL;
            unsigned count = libvlc_media_tracks_get(media, &tracks);
            for (unsigned i = 0; i < count; i++) {
                if (tracks[i]->i_type == libvlc_track_video && !result->video_tracks++) {
                    fourcc(tracks[i]->i_codec, result->video_codec);
                    result->width = tracks[i]->video->i_width;
                    result->height = tracks[i]->video->i_height;
                } else if (tracks[i]->i_type == libvlc_track_audio && !result->audio_tracks++) {
                    fourcc(tracks[i]->i_codec, result->audio_codec);
                }
            }
            if (count) libvlc_media_tracks_release(tracks, count);
            result->duration_ms = libvlc_media_get_duration(media);
            ok = count > 0;
        }
    }
    /* Parsing runs on libVLC's preparser thread; stop it before the event
       target leaves scope. */
    libvlc_media_parse_stop(media);
    libvlc_event_detach(events, libvlc_MediaParsedChanged, parsed_changed, &wait);
    libvlc_media_release(media);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_result result;
    (void)parsarium_parse(data, size, &result);
    return 0;
}
