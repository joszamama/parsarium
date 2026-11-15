#include "harness.h"
#include <pdfio.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_pdf(const uint8_t *data,size_t size,struct parsarium_pdf_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char path[]="/tmp/parsarium-pdf-XXXXXX";int fd=mkstemp(path);if(fd<0)return 0;
 size_t off=0;while(off<size){ssize_t n=write(fd,data+off,size-off);if(n<=0){close(fd);unlink(path);return 0;}off+=(size_t)n;}
 close(fd);
 pdfio_file_t *pdf=pdfioFileOpen(path,NULL,NULL,NULL,NULL);
 unlink(path);
 if(!pdf)return 0;
 size_t pages=pdfioFileGetNumPages(pdf);
 int ok=pages>0&&pdfioFileGetPage(pdf,0)!=NULL;
 result->pages=pages;
 pdfioFileClose(pdf);
 return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_pdf_result result;(void)parsarium_parse_pdf(data,size,&result);return 0;
}
