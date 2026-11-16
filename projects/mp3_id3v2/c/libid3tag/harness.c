#include "harness.h"
#include <id3tag.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int parsarium_parse_id3(const uint8_t *data,size_t size,struct parsarium_id3_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));
 char path[]="/tmp/parsarium-id3-XXXXXX";
 int fd=mkstemp(path);if(fd<0)return 0;
 size_t offset=0;
 while(offset<size){ssize_t n=write(fd,data+offset,size-offset);if(n<=0){close(fd);unlink(path);return 0;}offset+=(size_t)n;}
 close(fd);
 struct id3_file *file=id3_file_open(path,ID3_FILE_MODE_READONLY);
 unlink(path);
 if(!file)return 0;
 struct id3_tag *tag=id3_file_tag(file);
 struct id3_frame *frame=tag?id3_tag_findframe(tag,ID3_FRAME_TITLE,0):NULL;
 if(!frame){id3_file_close(file);return 0;}
 union id3_field *field=id3_frame_field(frame,1);
 if(!field||!id3_field_getnstrings(field)){id3_file_close(file);return 0;}
 const id3_ucs4_t *ucs4=id3_field_getstrings(field,0);
 if(!ucs4){id3_file_close(file);return 0;}
 id3_utf8_t *title=id3_ucs4_utf8duplicate(ucs4);
 if(!title){id3_file_close(file);return 0;}
 size_t length=strlen((const char*)title);int ok=length<sizeof(result->title);
 if(ok){memcpy(result->title,title,length+1);result->normalized_id3_major=ID3_TAG_VERSION_MAJOR(id3_tag_version(tag));result->frames=tag->nframes;}
 free(title);id3_file_close(file);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_id3_result r;(void)parsarium_parse_id3(data,size,&r);return 0;}
