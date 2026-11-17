#include <sndfile.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  SF_INFO info;
  memset(&info, 0, sizeof(info));
  SNDFILE *file = sf_open(argv[1], SFM_READ, &info);
  if (!file || (info.format & SF_FORMAT_TYPEMASK) != SF_FORMAT_MPEG ||
      (info.format & SF_FORMAT_SUBMASK) != SF_FORMAT_MPEG_LAYER_III) return 1;
  const char *title = sf_get_string(file, SF_STR_TITLE);
  if (!title) return 1;
  float sample[2] = {0};
  sf_count_t decoded = sf_readf_float(file, sample, 1);
  printf("{\"title\":\"%s\",\"sample_rate\":%d,\"channels\":%d,\"frames\":%lld,\"decoded_frames\":%lld}\n",
         title, info.samplerate, info.channels, (long long)info.frames, (long long)decoded);
  sf_close(file);
  return 0;
}
