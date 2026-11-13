#include <gpac/isomedia.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  GF_ISOFile *file = gf_isom_open(argv[1], GF_ISOM_OPEN_READ, NULL);
  if (!file) return 1;
  u32 tracks = gf_isom_get_track_count(file);
  u32 video = 0, audio = 0, width = 0, height = 0;
  for (u32 i = 1; i <= tracks; i++) {
    u32 type = gf_isom_get_media_type(file, i);
    if (type == GF_ISOM_MEDIA_VISUAL) {
      video++;
      if (gf_isom_get_visual_info(file, i, 1, &width, &height) != GF_OK) return 1;
    } else if (type == GF_ISOM_MEDIA_AUDIO) audio++;
  }
  u32 timescale = gf_isom_get_timescale(file);
  u64 duration = gf_isom_get_duration(file);
  if (!video || !audio || !timescale) return 1;
  printf("{\"tracks\":%u,\"video_tracks\":%u,\"audio_tracks\":%u,\"width\":%u,\"height\":%u,\"duration_ms\":%llu}\n",
         tracks, video, audio, width, height,
         (unsigned long long)(duration * 1000 / timescale));
  gf_isom_delete(file);
  return 0;
}
