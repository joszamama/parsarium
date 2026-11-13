#include <stdio.h>
#include <wand/wand_api.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  InitializeMagick(argv[0]);
  MagickWand *wand = NewMagickWand();
  if (!wand) return 1;
  if (!MagickReadImage(wand, argv[1])) {
    DestroyMagickWand(wand);
    DestroyMagick();
    return 1;
  }
  printf("{\"pages\":%zu,\"width\":%lu,\"height\":%lu}\n",
         MagickGetNumberImages(wand), MagickGetImageWidth(wand),
         MagickGetImageHeight(wand));
  DestroyMagickWand(wand);
  DestroyMagick();
  return 0;
}
