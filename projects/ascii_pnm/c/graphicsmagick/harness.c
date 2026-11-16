#include "harness.h"
#include <wand/wand_api.h>
#include <string.h>
int parsarium_parse_pnm(const uint8_t *data,size_t size,struct parsarium_pnm_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));InitializeMagick(NULL);MagickWand *wand=NewMagickWand();
 if(!wand){DestroyMagick();return 0;}
 int ok=MagickReadImageBlob(wand,data,size)!=MagickFalse;
 if(ok)ok=MagickGetImageWidth(wand)==2&&MagickGetImageHeight(wand)==1;
 unsigned char pixels[8]={0};
 if(ok)ok=MagickGetImagePixels(wand,0,0,2,1,"RGBA",CharPixel,pixels)!=MagickFalse;
 if(ok){result->width=2;result->height=1;memcpy(result->first,pixels,4);memcpy(result->second,pixels+4,4);result->has_second=1;}
 DestroyMagickWand(wand);DestroyMagick();return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_pnm_result r;(void)parsarium_parse_pnm(data,size,&r);return 0;}
