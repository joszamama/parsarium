#include <mpv/client.h>
#include <stdio.h>

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
    if (event->event_id == MPV_EVENT_FILE_LOADED) { loaded = 1; break; }
  }
  if (!loaded) return 1;
  char *container = mpv_get_property_string(player, "file-format");
  char *title = mpv_get_property_string(player, "metadata/by-key/title");
  char *video = mpv_get_property_string(player, "track-list/0/codec");
  char *audio = mpv_get_property_string(player, "track-list/1/codec");
  if (!container || !title || !video || !audio) return 1;
  printf("{\"container\":\"%s\",\"title\":\"%s\",\"video_codec\":\"%s\",\"audio_codec\":\"%s\"}\n",
         container, title, video, audio);
  mpv_free(container);
  mpv_free(title);
  mpv_free(video);
  mpv_free(audio);
  mpv_terminate_destroy(player);
  return 0;
}
