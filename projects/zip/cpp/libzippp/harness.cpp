#include "harness.hpp"
#include <libzippp.h>
#include <string>
#include <cstring>
#include <unistd.h>
#include <cstdlib>
bool parsarium_parse_zip(const std::uint8_t *data,std::size_t size,parsarium_zip_result *result) {
 if(!data||!result||!size||size>(1u<<20))return false;
 *result={};char path[]="/tmp/parsarium-libzippp-XXXXXX";
 int fd=mkstemp(path);if(fd<0)return false;
 std::size_t written=0;
 while(written<size){ssize_t n=write(fd,data+written,size-written);if(n<=0){close(fd);unlink(path);return false;}written+=(std::size_t)n;}
 close(fd);
 bool ok=false;
 try {
  libzippp::ZipArchive archive(path);
  if(archive.open(libzippp::ZipArchive::ReadOnly)) {
   const auto entries=archive.getEntries();
   if(!entries.empty()) {
    const std::string name=entries[0].getName();
    const std::string content=entries[0].readAsText();
    if(!name.empty()&&name.size()<sizeof(result->name)&&content.size()<=sizeof(result->content)) {
     result->entries=entries.size();result->name_len=name.size();result->content_len=content.size();
     std::memcpy(result->name,name.data(),name.size());
     std::memcpy(result->content,content.data(),content.size());ok=true;
    }
   }
   archive.close();
  }
 } catch (...) { ok=false; }
 unlink(path);return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data,std::size_t size) {
 parsarium_zip_result result;(void)parsarium_parse_zip(data,size,&result);return 0;
}
