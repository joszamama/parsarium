#include <Bento4C.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  AP4_Result result = AP4_SUCCESS;
  AP4_ByteStream *stream = AP4_FileByteStream_Create(
      argv[1], AP4_FILE_BYTE_STREAM_MODE_READ, &result);
  if (!stream || result != AP4_SUCCESS) return 1;
  AP4_File *file = AP4_File_FromStream(stream, 1);
  if (!file) return 1;
  AP4_Movie *movie = AP4_File_GetMovie(file);
  if (!movie) return 1;
  AP4_UI32 brand = 0;
  if (AP4_File_GetFileType(file, &brand, NULL, NULL) != AP4_SUCCESS) return 1;
  AP4_Cardinal tracks = AP4_Movie_GetTrackCount(movie);
  unsigned video = 0, audio = 0;
  for (AP4_Ordinal i = 0; i < tracks; i++) {
    AP4_Track *track = AP4_Movie_GetTrackByIndex(movie, i);
    if (!track) return 1;
    if (AP4_Track_GetType(track) == AP4_TRACK_TYPE_VIDEO) video++;
    if (AP4_Track_GetType(track) == AP4_TRACK_TYPE_AUDIO) audio++;
  }
  printf("{\"brand\":\"%c%c%c%c\",\"tracks\":%u,\"video_tracks\":%u,\"audio_tracks\":%u,\"duration_ms\":%u}\n",
         (char)(brand >> 24), (char)(brand >> 16), (char)(brand >> 8),
         (char)brand, tracks, video, audio, AP4_Movie_GetDurationMs(movie));
  AP4_File_Destroy(file);
  AP4_ByteStream_Release(stream);
  return 0;
}
