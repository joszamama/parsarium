#include "harness.h"
#include "Exceptions.h"
#include "FFmpegReader.h"
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <string>

static void copy_codec(char out[64], const std::string &name) {
  if (!name.empty() && name.size() < 64) memcpy(out, name.c_str(), name.size() + 1);
}

int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-libopenshot-XXXXXX.mp4";
  int fd = mkstemps(path, 4);
  if (fd < 0) return 0;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return 0; }
    written += (size_t)n;
  }
  if (close(fd)) { unlink(path); return 0; }
  int ok = 0;
  // inspect_reader=false so the only Open() is the explicit call below. Open()
  // reopens the path through Seek(1), so the file stays until after Close().
  // openshot::ExceptionBase is the reader's documented failure contract; any
  // other exception escapes and is reported as a crash.
  try {
    openshot::FFmpegReader reader(path, false);
    reader.Open();
    const openshot::ReaderInfo &info = reader.info;
    result->video = info.has_video ? 1 : 0;
    result->audio = info.has_audio ? 1 : 0;
    result->width = info.width;
    result->height = info.height;
    copy_codec(result->video_codec, info.vcodec);
    copy_codec(result->audio_codec, info.acodec);
    reader.Close();
    ok = result->video || result->audio;
  } catch (const openshot::ExceptionBase &) {
    ok = 0;
  }
  unlink(path);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_mp4_result result;
  (void)parsarium_parse_mp4(data, size, &result);
  return 0;
}
