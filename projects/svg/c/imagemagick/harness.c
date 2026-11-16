#include "harness.h"
#include <MagickWand/MagickWand.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
int parsarium_parse_svg(const uint8_t*data,size_t size,struct parsarium_svg_result*result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));MagickWandGenesis();MagickWand*wand=NewMagickWand();
 if(!wand){MagickWandTerminus();return 0;}
 char path[]="/tmp/parsarium-svg-XXXXXX.svg";int fd=mkstemps(path,4);
 if(fd<0){DestroyMagickWand(wand);MagickWandTerminus();return 0;}
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);DestroyMagickWand(wand);MagickWandTerminus();return 0;}off+=(size_t)n;}close(fd);
 char spec[128];snprintf(spec,sizeof(spec),"MSVG:%s",path);
 int ok=MagickReadImage(wand,spec)!=MagickFalse;unlink(path);
 if(ok)ok=MagickGetImageWidth(wand)==2&&MagickGetImageHeight(wand)==1;
 unsigned char pixels[6]={0};
 if(ok)ok=MagickExportImagePixels(wand,0,0,2,1,"RGB",CharPixel,pixels)!=MagickFalse;
 if(ok){result->width=2;result->height=1;memcpy(result->first,pixels,3);memcpy(result->second,pixels+3,3);}
 DestroyMagickWand(wand);MagickWandTerminus();return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t*data,size_t size){struct parsarium_svg_result r;(void)parsarium_parse_svg(data,size,&r);return 0;}
