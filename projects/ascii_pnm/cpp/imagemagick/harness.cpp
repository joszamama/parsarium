#include "harness.h"
#include <MagickWand/MagickWand.h>
#include <string.h>
int parsarium_parse_pnm(const uint8_t *data,size_t size,struct parsarium_pnm_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));MagickWandGenesis();MagickWand *wand=NewMagickWand();
 if(!wand){MagickWandTerminus();return 0;}
 int ok=MagickReadImageBlob(wand,data,size)!=MagickFalse;
 size_t width=ok?MagickGetImageWidth(wand):0,height=ok?MagickGetImageHeight(wand):0;
 if(ok)ok=width>0&&height>0;
 /* The second pixel is the next one in raster order, if the image has one. */
 ssize_t second_x=width>1?1:0,second_y=width>1?0:1;
 int has_second=width>1||height>1;
 if(ok)ok=MagickExportImagePixels(wand,0,0,1,1,"RGBA",CharPixel,result->first)!=MagickFalse;
 if(ok&&has_second)ok=MagickExportImagePixels(wand,second_x,second_y,1,1,"RGBA",CharPixel,result->second)!=MagickFalse;
 if(ok){result->width=(unsigned)width;result->height=(unsigned)height;result->has_second=has_second;}
 DestroyMagickWand(wand);MagickWandTerminus();return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_pnm_result r;(void)parsarium_parse_pnm(data,size,&r);return 0;}
