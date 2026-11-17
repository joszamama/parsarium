#include <miniaudio/miniaudio.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  ma_decoder_config config = ma_decoder_config_init(ma_format_f32, 0, 0);
  ma_decoder decoder;
  if (ma_decoder_init_file(argv[1], &config, &decoder) != MA_SUCCESS) return 1;
  float frame[2] = {0};
  ma_uint64 decoded = 0, length = 0;
  if (decoder.outputChannels > 2 ||
      ma_decoder_read_pcm_frames(&decoder, frame, 1, &decoded) != MA_SUCCESS ||
      ma_decoder_get_length_in_pcm_frames(&decoder, &length) != MA_SUCCESS ||
      decoded != 1) return 1;
  printf("{\"sample_rate\":%u,\"channels\":%u,\"frames\":%llu,\"decoded_frames\":%llu}\n",
         decoder.outputSampleRate, decoder.outputChannels,
         (unsigned long long)length, (unsigned long long)decoded);
  ma_decoder_uninit(&decoder);
  return 0;
}
