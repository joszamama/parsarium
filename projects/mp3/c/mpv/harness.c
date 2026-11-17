#define _GNU_SOURCE
#include "harness.h"
#include <math.h>
#include <mpv/client.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void copy_property(mpv_handle *mpv, const char *name, char *out, size_t size) {
  char *value = mpv_get_property_string(mpv, name);
  if (value) snprintf(out, size, "%s", value);
  mpv_free(value);
}

#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
/* AFL++ defines this macro. mpv's upstream stream_file.c then accepts local
   input only on descriptor 42; fd://42 is its own fuzzing stream route. */
static int install_fd42(const char *path) {
  int source = open(path, O_RDONLY | O_CLOEXEC);
  if (source < 0) return 0;
  if (source == 42) return 1;
  int duplicated = dup2(source, 42);
  close(source);
  return duplicated == 42;
}
#endif

/* The catalog call site: a local tagged MP3 path through loadfile,
   FILE_LOADED, then the ID3v2 title, the first track's codec and the duration.
   Audio and video outputs are null and playback stays paused, so only loading
   is observed. */
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-mpv-XXXXXX.mp3";
  int fd = mkstemps(path, 4);
  if (fd < 0) return 0;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return 0; }
    written += (size_t)n;
  }
  close(fd);
  mpv_handle *mpv = mpv_create();
  if (!mpv) { unlink(path); return 0; }
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
  if (!install_fd42(path)) { mpv_terminate_destroy(mpv); unlink(path); return 0; }
#endif
  int ok = 0;
  if (mpv_set_option_string(mpv, "config", "no") < 0 ||
      mpv_set_option_string(mpv, "ao", "null") < 0 ||
      mpv_set_option_string(mpv, "vo", "null") < 0 ||
      mpv_set_option_string(mpv, "pause", "yes") < 0 ||
      mpv_set_option_string(mpv, "vid", "no") < 0 ||
      mpv_set_option_string(mpv, "aid", "no") < 0 ||
      mpv_set_option_string(mpv, "track-auto-selection", "no") < 0 ||
      mpv_set_option_string(mpv, "video-osd", "no") < 0 ||
      mpv_set_option_string(mpv, "input-builtin-bindings", "no") < 0 ||
      mpv_initialize(mpv) < 0) goto done;
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
  const char *command[] = {"loadfile", "fd://42", NULL};
#else
  const char *command[] = {"loadfile", path, NULL};
#endif
  if (mpv_command(mpv, command) < 0) goto done;
  int loaded = 0;
  for (int i = 0; i < 20 && !loaded; ++i) {
    mpv_event *event = mpv_wait_event(mpv, 0.5);
    if (event->event_id == MPV_EVENT_FILE_LOADED) loaded = 1;
    else if (event->event_id == MPV_EVENT_END_FILE || event->event_id == MPV_EVENT_SHUTDOWN) break;
  }
  if (!loaded) goto done;
  copy_property(mpv, "metadata/by-key/title", result->title, sizeof(result->title));
  char *type = mpv_get_property_string(mpv, "track-list/0/type");
  int audio = type && !strcmp(type, "audio");
  mpv_free(type);
  if (!audio) goto done;
  copy_property(mpv, "track-list/0/codec", result->codec, sizeof(result->codec));
  double duration = 0;
  if (mpv_get_property(mpv, "duration", MPV_FORMAT_DOUBLE, &duration) < 0) goto done;
  /* Range check first: converting an out-of-range double is undefined and
     would be reported by UBSan as a harness fault, not a parser result. */
  if (!isfinite(duration) || duration <= 0 || duration > 1e9) goto done;
  result->duration_ms = (int64_t)llround(duration * 1000.0);
  ok = result->codec[0] != 0;
done:
  mpv_terminate_destroy(mpv);
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
  close(42);
#endif
  unlink(path);
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_mp3_result result;
  (void)parsarium_parse_mp3(data, size, &result);
  return 0;
}
