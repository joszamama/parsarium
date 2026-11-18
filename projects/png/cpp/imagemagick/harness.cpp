#include "harness.h"
#include <MagickWand/MagickWand.h>
#include <string.h>
#include <stdio.h>
int parsarium_parse_png(const uint8_t *data,size_t size,struct parsarium_png_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));MagickWandGenesis();MagickWand *wand=NewMagickWand();
 if(!wand){MagickWandTerminus();return 0;}
 int ok=MagickReadImageBlob(wand,data,size)!=MagickFalse;
 size_t width=ok?MagickGetImageWidth(wand):0,height=ok?MagickGetImageHeight(wand):0;
 unsigned char pixels[8]={0};
 if(ok)ok=MagickExportImagePixels(wand,0,0,width>1?2:1,1,"RGBA",CharPixel,pixels)!=MagickFalse;
 if(ok){result->width=(unsigned)width;result->height=(unsigned)height;result->has_second=width>1;memcpy(result->first,pixels,4);if(result->has_second)memcpy(result->second,pixels+4,4);}
 else{ExceptionType severity;char *message=MagickGetException(wand,&severity);fprintf(stderr,"ImageMagick: %s\n",message&&*message?message:"read failed");if(message)MagickRelinquishMemory(message);}
 DestroyMagickWand(wand);MagickWandTerminus();return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_png_result r;(void)parsarium_parse_png(data,size,&r);return 0;}
