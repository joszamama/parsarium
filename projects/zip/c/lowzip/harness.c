#include "harness.h"
#include <lowzip.h>
#include <string.h>
#include <limits.h>
typedef struct { const uint8_t *bytes; unsigned int length; } input_bytes;
static unsigned int read_byte(void *opaque,unsigned int offset) {
 const input_bytes *input=(const input_bytes *)opaque;
 return offset<input->length ? input->bytes[offset] : 0x100U;
}
int parsarium_parse_zip(const uint8_t *data,size_t size,struct parsarium_zip_result *result) {
 if(!data||!result||!size||size>(1u<<20)||size>UINT_MAX)return 0;
 memset(result,0,sizeof(*result));
 input_bytes input={data,(unsigned int)size};
 lowzip_state state={0};state.udata=&input;state.read_callback=read_byte;state.zip_length=input.length;
 lowzip_init_archive(&state);if(state.have_error)return 0;
 size_t count=0;while(count<1024 && lowzip_locate_file(&state,(int)count,NULL))++count;
 if(!count)return 0;
 lowzip_file *entry=lowzip_locate_file(&state,0,NULL);
 if(!entry||state.have_error||entry->uncompressed_size>sizeof(result->content))return 0;
 size_t name_len=strnlen(entry->filename,sizeof(entry->filename));
 if(!name_len||name_len>=sizeof(entry->filename)||name_len>=sizeof(result->name))return 0;
 memcpy(result->name,entry->filename,name_len);result->name_len=name_len;
 result->entries=count;result->content_len=entry->uncompressed_size;
 state.output_start=result->content;state.output_end=result->content+result->content_len;
 state.output_next=result->content;
 lowzip_get_data(&state);
 return !state.have_error && state.output_next==state.output_end;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
 struct parsarium_zip_result result;(void)parsarium_parse_zip(data,size,&result);return 0;
}
