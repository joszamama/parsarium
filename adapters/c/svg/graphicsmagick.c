#include <wand/wand_api.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  InitializeMagick(argv[0]);
  MagickWand *wand = NewMagickWand();
  if (!wand) return 1;
  if (!MagickReadImage(wand, argv[1])) return 1;
  unsigned char pixels[6];
  if (!MagickGetImagePixels(wand, 0, 0, 2, 1, "RGB", CharPixel, pixels)) return 1;
  printf("{\"width\":%lu,\"height\":%lu,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         MagickGetImageWidth(wand), MagickGetImageHeight(wand),
         pixels[0], pixels[1], pixels[2], pixels[3], pixels[4], pixels[5]);
  DestroyMagickWand(wand);
  DestroyMagick();
  return 0;
}
