#include "harness.h"
#include <pnm.hpp>
#include <unistd.h>
#include <cstring>
#include <cstdio>

bool parsarium_parse_pnm(const uint8_t *data,size_t size,struct parsarium_pnm_result *result) {
 if (!data || !result || !size || size>(1u<<20)) return false;
 *result={};
 char path[]="/tmp/parsarium-pnmpp-XXXXXX";
 int fd=mkstemp(path);
 if (fd<0) return false;
 size_t written=0;
 while (written<size) {
  ssize_t n=write(fd,data+written,size-written);
  if (n<=0) {close(fd);unlink(path);return false;}
  written+=(size_t)n;
 }
 close(fd);
 try {
  const pnm::image<pnm::rgb_pixel> image=pnm::read(path);
  unlink(path);
  if (image.width()<2 || image.height()<1) return false;
  auto first=image[0][0],second=image[0][1];
  result->width=image.width();result->height=image.height();
  result->first[0]=first.red;result->first[1]=first.green;
  result->first[2]=first.blue;result->first[3]=255;
  result->second[0]=second.red;result->second[1]=second.green;
  result->second[2]=second.blue;result->second[3]=255;
  return true;
 } catch (...) { unlink(path); return false; }
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_pnm_result result;
 (void)parsarium_parse_pnm(data,size,&result);
 return 0;
}
