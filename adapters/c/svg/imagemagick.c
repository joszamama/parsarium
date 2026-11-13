#include <MagickWand/MagickWand.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  MagickWandGenesis();
  MagickWand *wand = NewMagickWand();
  if (!wand) return 1;
  size_t len = strlen(argv[1]) + 6;
  char *input = malloc(len);
  if (!input) return 1;
  snprintf(input, len, "MSVG:%s", argv[1]);
  MagickBooleanType loaded = MagickReadImage(wand, input);
  free(input);
  if (loaded == MagickFalse) return 1;
  unsigned char pixels[6];
  if (MagickExportImagePixels(wand, 0, 0, 2, 1, "RGB", CharPixel, pixels) == MagickFalse) return 1;
  printf("{\"width\":%zu,\"height\":%zu,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         MagickGetImageWidth(wand), MagickGetImageHeight(wand),
         pixels[0], pixels[1], pixels[2], pixels[3], pixels[4], pixels[5]);
  DestroyMagickWand(wand);
  MagickWandTerminus();
  return 0;
}
