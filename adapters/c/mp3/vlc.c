#include <vlc/vlc.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  const char *args[] = {"--intf=dummy", "--no-video", "--no-audio", "--ignore-config"};
  libvlc_instance_t *vlc = libvlc_new(4, args);
  if (!vlc) return 1;
  libvlc_media_t *media = libvlc_media_new_path(vlc, argv[1]);
  if (!media) { libvlc_release(vlc); return 1; }
  if (libvlc_media_parse_with_options(media, libvlc_media_parse_local, 5000) != 0) return 1;
  libvlc_media_parsed_status_t status = libvlc_media_parsed_status_skipped;
  for (int i = 0; i < 100; i++) {
    status = libvlc_media_get_parsed_status(media);
    if (status == libvlc_media_parsed_status_done ||
        status == libvlc_media_parsed_status_failed ||
        status == libvlc_media_parsed_status_timeout) break;
    usleep(50000);
  }
  if (status != libvlc_media_parsed_status_done) return 1;
  char *title = libvlc_media_get_meta(media, libvlc_meta_Title);
  libvlc_media_track_t **tracks = NULL;
  unsigned count = libvlc_media_tracks_get(media, &tracks);
  unsigned audio_tracks = 0;
  unsigned mp3_tracks = 0;
  for (unsigned i = 0; i < count; i++) {
    if (tracks[i]->i_type == libvlc_track_audio) audio_tracks++;
    if (tracks[i]->i_type == libvlc_track_audio &&
        tracks[i]->i_codec == 0x2033706d) mp3_tracks++;
  }
  if (!title || audio_tracks != 1 || mp3_tracks != 1) return 1;
  printf("{\"title\":\"%s\",\"audio_tracks\":%u,\"mp3_tracks\":%u}\n",
         title, audio_tracks, mp3_tracks);
  if (count) libvlc_media_tracks_release(tracks, count);
  libvlc_free(title);
  libvlc_media_release(media);
  libvlc_release(vlc);
  return 0;
}
