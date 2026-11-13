#include <aubio/aubio.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  aubio_source_t *source = new_aubio_source(argv[1], 0, 256);
  if (!source) return 1;
  fvec_t *samples = new_fvec(256);
  if (!samples) return 1;
  uint_t decoded = 0;
  aubio_source_do(source, samples, &decoded);
  if (decoded != 256) return 1;
  printf("{\"sample_rate\":%u,\"channels\":%u,\"decoded_samples\":%u}\n",
         aubio_source_get_samplerate(source), aubio_source_get_channels(source), decoded);
  del_fvec(samples);
  del_aubio_source(source);
  aubio_cleanup();
  return 0;
}
