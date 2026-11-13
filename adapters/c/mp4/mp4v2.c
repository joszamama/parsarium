#include <mp4v2/mp4v2.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  MP4FileHandle file = MP4Read(argv[1]);
  if (file == MP4_INVALID_FILE_HANDLE) return 1;
  uint32_t tracks = MP4GetNumberOfTracks(file, NULL, 0);
  uint32_t video = MP4GetNumberOfTracks(file, MP4_VIDEO_TRACK_TYPE, 0);
  uint32_t audio = MP4GetNumberOfTracks(file, MP4_AUDIO_TRACK_TYPE, 0);
  MP4TrackId video_id = MP4FindTrackId(file, 0, MP4_VIDEO_TRACK_TYPE, 0);
  if (!video || !audio || video_id == MP4_INVALID_TRACK_ID) return 1;
  uint16_t width = MP4GetTrackVideoWidth(file, video_id);
  uint16_t height = MP4GetTrackVideoHeight(file, video_id);
  printf("{\"tracks\":%u,\"video_tracks\":%u,\"audio_tracks\":%u,\"width\":%u,\"height\":%u}\n",
         tracks, video, audio, width, height);
  MP4Close(file, 0);
  return 0;
}
