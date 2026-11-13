#define mp4parse_rust_mp4parse_h 1
#define MP4PARSE_UNSTABLE_API 1
#include "mp4parse_capi.h"
#include <stdint.h>
#include <stdio.h>

static intptr_t read_bytes(uint8_t *buffer, uintptr_t size, void *context) {
  FILE *file = context;
  size_t count = fread(buffer, 1, size, file);
  return ferror(file) ? -1 : (intptr_t)count;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb");
  if (!file) return 3;
  Mp4parseIo io = {read_bytes, file};
  Mp4parseParser *parser = NULL;
  Mp4parseStatus status = mp4parse_new(&io, &parser);
  if (status != MP4PARSE_STATUS_OK || !parser) {
    fprintf(stderr, "mp4parse_new: %d\n", status);
    fclose(file);
    return 4;
  }
  uint32_t tracks = 0, video = 0, audio = 0, width = 0, height = 0;
  status = mp4parse_get_track_count(parser, &tracks);
  if (status != MP4PARSE_STATUS_OK) return 5;
  for (uint32_t index = 0; index < tracks; index++) {
    Mp4parseTrackInfo info = {0};
    status = mp4parse_get_track_info(parser, index, &info);
    if (status != MP4PARSE_STATUS_OK) return 6;
    if (info.track_type == MP4PARSE_TRACK_TYPE_VIDEO) {
      Mp4parseTrackVideoInfo details = {0};
      status = mp4parse_get_track_video_info(parser, index, &details);
      if (status != MP4PARSE_STATUS_OK) return 7;
      video++;
      width = details.display_width;
      height = details.display_height;
    } else if (info.track_type == MP4PARSE_TRACK_TYPE_AUDIO) {
      audio++;
    }
  }
  printf("{\"tracks\":%u,\"video\":%u,\"audio\":%u,\"width\":%u,\"height\":%u}\n",
         tracks, video, audio, width, height);
  mp4parse_free(parser);
  fclose(file);
  return 0;
}
