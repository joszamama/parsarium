#define _GNU_SOURCE
#include "harness.h"
#include <audiofile.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-audiofile-XXXXXX.wav";
  int fd = mkstemps(path, 4);
  if (fd < 0) return 0;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return 0; }
    written += (size_t)n;
  }
  close(fd);
  AFfilehandle file = afOpenFile(path, "r", NULL);
  unlink(path);
  if (!file) return 0;
  int ok = afGetFileFormat(file, NULL) == AF_FILE_WAVE &&
           afSetVirtualSampleFormat(file, AF_DEFAULT_TRACK, AF_SAMPFMT_TWOSCOMP, 16) == 0;
  if (ok) ok = afReadFrames(file, AF_DEFAULT_TRACK, result->samples, 4) == 4;
  if (ok) {
    result->sample_rate = (unsigned int)afGetRate(file, AF_DEFAULT_TRACK);
    result->channels = (unsigned int)afGetChannels(file, AF_DEFAULT_TRACK);
    result->frames = (unsigned long long)afGetFrameCount(file, AF_DEFAULT_TRACK);
  }
  afCloseFile(file);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
