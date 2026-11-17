#include <mpv/client.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  mpv_handle *player = mpv_create();
  if (!player) return 1;
  if (mpv_set_option_string(player, "config", "no") < 0 ||
      mpv_set_option_string(player, "ao", "null") < 0 ||
      mpv_set_option_string(player, "vo", "null") < 0 ||
      mpv_set_option_string(player, "pause", "yes") < 0 ||
      mpv_initialize(player) < 0) return 1;
  const char *command[] = {"loadfile", argv[1], NULL};
  if (mpv_command(player, command) < 0) return 1;
  int loaded = 0;
  for (int i = 0; i < 20; ++i) {
    mpv_event *event = mpv_wait_event(player, 0.5);
    if (event->event_id == MPV_EVENT_FILE_LOADED) {
      loaded = 1;
      break;
    }
  }
  if (!loaded) return 1;
  char *title = mpv_get_property_string(player, "metadata/by-key/title");
  char *codec = mpv_get_property_string(player, "track-list/0/codec");
  double duration = 0;
  if (!title || !codec || strcmp(codec, "mp3") != 0 ||
      mpv_get_property(player, "duration", MPV_FORMAT_DOUBLE, &duration) < 0 ||
      duration <= 0) return 1;
  printf("{\"title\":\"%s\",\"codec\":\"%s\",\"duration_ms\":%d}\n",
         title, codec, (int)(duration * 1000.0 + 0.5));
  mpv_free(title);
  mpv_free(codec);
  mpv_terminate_destroy(player);
  return 0;
}
