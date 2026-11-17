#include <mad.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb");
  if (!file) return 1;
  if (fseek(file, 0, SEEK_END) != 0) return 1;
  long length = ftell(file);
  if (length < 16 || length > 1000000) return 1;
  rewind(file);
  unsigned char *bytes = (unsigned char *)calloc((size_t)length + MAD_BUFFER_GUARD, 1);
  if (!bytes) return 1;
  if (fread(bytes, 1, (size_t)length, file) != (size_t)length) return 1;
  fclose(file);

  // libmad consumes MPEG frames; skip the control's ID3v2 header and tag body.
  if (memcmp(bytes, "ID3", 3) != 0) return 1;
  size_t offset = 10 + (((size_t)bytes[6] & 127) << 21)
                     + (((size_t)bytes[7] & 127) << 14)
                     + (((size_t)bytes[8] & 127) << 7)
                     + ((size_t)bytes[9] & 127);
  if (offset >= (size_t)length) return 1;

  struct mad_stream stream;
  struct mad_frame frame;
  struct mad_synth synth;
  mad_stream_init(&stream);
  mad_frame_init(&frame);
  mad_synth_init(&synth);
  mad_stream_buffer(&stream, bytes, (unsigned long)length + MAD_BUFFER_GUARD);
  mad_stream_skip(&stream, (unsigned long)offset);
  if (mad_frame_decode(&frame, &stream) != 0 || frame.header.layer != MAD_LAYER_III) return 1;
  mad_synth_frame(&synth, &frame);
  printf("{\"layer\":%d,\"sample_rate\":%u,\"bit_rate\":%lu,\"channels\":%u,\"decoded_samples\":%u}\n",
         frame.header.layer, frame.header.samplerate, frame.header.bitrate,
         synth.pcm.channels, synth.pcm.length);
  mad_synth_finish(&synth);
  mad_frame_finish(&frame);
  mad_stream_finish(&stream);
  free(bytes);
  return 0;
}
