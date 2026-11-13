#define DR_MP3_IMPLEMENTATION
#include <dr_mp3.h>
#include <stdio.h>

struct tag_state { size_t id3v2_bytes; };

static void on_meta(void *ctx, const drmp3_metadata *meta) {
  struct tag_state *state = (struct tag_state *)ctx;
  if (meta->type == DRMP3_METADATA_TYPE_ID3V2) state->id3v2_bytes = meta->rawDataSize;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  struct tag_state state = {0};
  drmp3 mp3;
  if (!drmp3_init_file_with_metadata(&mp3, argv[1], on_meta, &state, NULL)) return 1;
  drmp3_int16 pcm[2] = {0};
  drmp3_uint64 frames = drmp3_read_pcm_frames_s16(&mp3, 1, pcm);
  if (frames != 1 || state.id3v2_bytes == 0) {
    drmp3_uninit(&mp3);
    return 1;
  }
  printf("{\"sample_rate\":%u,\"channels\":%u,\"decoded_frames\":%llu,\"id3v2_bytes\":%zu}\n",
         mp3.sampleRate, mp3.channels, (unsigned long long)frames, state.id3v2_bytes);
  drmp3_uninit(&mp3);
  return 0;
}
