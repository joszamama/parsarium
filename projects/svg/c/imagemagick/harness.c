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
 size_t width=ok?MagickGetImageWidth(wand):0,height=ok?MagickGetImageHeight(wand):0;
 if(ok)ok=width>0&&height>0;
 if(ok)ok=MagickExportImagePixels(wand,0,0,1,1,"RGB",CharPixel,result->first)!=MagickFalse;
 /* The second sample is the next pixel in row-major order and is absent for a 1x1 image. */
 result->second_present=ok&&width*height>1;
 if(result->second_present)
  ok=MagickExportImagePixels(wand,width>1?1:0,width>1?0:1,1,1,"RGB",CharPixel,result->second)!=MagickFalse;
 if(ok){result->width=(unsigned)width;result->height=(unsigned)height;}
 DestroyMagickWand(wand);MagickWandTerminus();return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t*data,size_t size){struct parsarium_svg_result r;(void)parsarium_parse_svg(data,size,&r);return 0;}
