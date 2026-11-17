#include <MediaInfoDLL/MediaInfoDLL_Static.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  void *handle = MediaInfoA_New();
  if (!handle) return 1;
  if (!MediaInfoA_Open(handle, argv[1])) {
    MediaInfoA_Delete(handle);
    return 1;
  }
  char format[64], title[256], sample_rate[32];
  const char *value = MediaInfoA_Get(handle, MediaInfo_Stream_Audio, 0,
                                     "Format", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || strcmp(value, "MPEG Audio") != 0) return 1;
  snprintf(format, sizeof(format), "%s", value);
  value = MediaInfoA_Get(handle, MediaInfo_Stream_General, 0,
                          "Title", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || !*value) return 1;
  snprintf(title, sizeof(title), "%s", value);
  value = MediaInfoA_Get(handle, MediaInfo_Stream_Audio, 0,
                          "SamplingRate", MediaInfo_Info_Text, MediaInfo_Info_Name);
  if (!value || !*value) return 1;
  snprintf(sample_rate, sizeof(sample_rate), "%s", value);
  printf("{\"title\":\"%s\",\"format\":\"%s\",\"sample_rate\":%s}\n",
         title, format, sample_rate);
  MediaInfoA_Close(handle);
  MediaInfoA_Delete(handle);
  return 0;
}
