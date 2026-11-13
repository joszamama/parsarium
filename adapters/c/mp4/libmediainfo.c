#include <MediaInfoDLL/MediaInfoDLL_Static.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  void *handle = MediaInfoA_New();
  if (!handle || !MediaInfoA_Open(handle, argv[1])) return 1;
  char container[64], title[256], video[64], audio[64];
  const char *value = MediaInfoA_Get(handle, MediaInfo_Stream_General, 0,
                                     "Format", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || !*value) return 1;
  snprintf(container, sizeof(container), "%s", value);
  value = MediaInfoA_Get(handle, MediaInfo_Stream_General, 0,
                         "Title", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || !*value) return 1;
  snprintf(title, sizeof(title), "%s", value);
  value = MediaInfoA_Get(handle, MediaInfo_Stream_Video, 0,
                         "Format", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || !*value) return 1;
  snprintf(video, sizeof(video), "%s", value);
  value = MediaInfoA_Get(handle, MediaInfo_Stream_Audio, 0,
                         "Format", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || !*value) return 1;
  snprintf(audio, sizeof(audio), "%s", value);
  int width = atoi(MediaInfoA_Get(handle, MediaInfo_Stream_Video, 0,
                                  "Width", MediaInfo_Info_Text, MediaInfo_Info_Name));
  int height = atoi(MediaInfoA_Get(handle, MediaInfo_Stream_Video, 0,
                                   "Height", MediaInfo_Info_Text, MediaInfo_Info_Name));
  printf("{\"container\":\"%s\",\"title\":\"%s\",\"video\":\"%s\",\"audio\":\"%s\",\"width\":%d,\"height\":%d}\n",
         container, title, video, audio, width, height);
  MediaInfoA_Close(handle);
  MediaInfoA_Delete(handle);
  return 0;
}
