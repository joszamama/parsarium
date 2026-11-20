#include "harness.h"
#include <sndfile.h>
#include <stdio.h>
#include <string.h>
struct memfile { const uint8_t *data; sf_count_t size, pos; };
static sf_count_t length(void *p) { return ((struct memfile *)p)->size; }
static sf_count_t tell(void *p) { return ((struct memfile *)p)->pos; }
static sf_count_t seek(sf_count_t offset, int whence, void *p) {
 struct memfile *m=p; sf_count_t next=(whence==SEEK_SET?0:whence==SEEK_CUR?m->pos:m->size)+offset;
 if(next<0||next>m->size)return -1; m->pos=next; return next;
}
static sf_count_t readbytes(void *dst, sf_count_t count, void *p) {
 struct memfile *m=p;if(count<0)return 0;if(count>m->size-m->pos)count=m->size-m->pos;
 memcpy(dst,m->data+m->pos,(size_t)count);m->pos+=count;return count;
}
static sf_count_t writebytes(const void *src,sf_count_t count,void *p){(void)src;(void)count;(void)p;return 0;}
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 struct memfile input={data,(sf_count_t)size,0};SF_VIRTUAL_IO io={length,seek,readbytes,writebytes,tell};
 SF_INFO info={0};SNDFILE *file=sf_open_virtual(&io,SFM_READ,&info,&input);
 if(!file)return 0;
 int ok=(info.format&SF_FORMAT_TYPEMASK)==SF_FORMAT_MPEG &&
  (info.format&SF_FORMAT_SUBMASK)==SF_FORMAT_MPEG_LAYER_III;
 const char *title=ok?sf_get_string(file,SF_STR_TITLE):NULL;
 if(title&&strlen(title)>=sizeof(result->title))ok=0;
 float sample[2]={0};sf_count_t decoded=ok?sf_readf_float(file,sample,1):0;
 if(ok){result->has_title=title!=NULL;if(title)strcpy(result->title,title);result->sample_rate=info.samplerate;
 result->channels=info.channels;result->frames=info.frames;result->decoded_frames=decoded;}
 sf_close(file);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){
 struct parsarium_mp3_result result;(void)parsarium_parse_mp3(data,size,&result);return 0;
}
