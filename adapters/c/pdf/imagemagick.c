#include <stdio.h>
#include <MagickWand/MagickWand.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  MagickWandGenesis();
  MagickWand *wand = NewMagickWand();
  if (!wand) return 1;
  if (MagickReadImage(wand, argv[1]) == MagickFalse) {
    DestroyMagickWand(wand);
    MagickWandTerminus();
    return 1;
  }
  printf("{\"pages\":%zu,\"width\":%zu,\"height\":%zu}\n",
         MagickGetNumberImages(wand), MagickGetImageWidth(wand),
         MagickGetImageHeight(wand));
  DestroyMagickWand(wand);
  MagickWandTerminus();
  return 0;
}
