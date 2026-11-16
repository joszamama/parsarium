#include "harness.h"
#include <mongoose.h>
#include <string.h>
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));struct mg_http_message msg;
 int consumed=mg_http_parse((const char *)data,size,&msg);
 if(consumed!=(int)size || msg.method.len==0 || msg.method.len>=sizeof(result->method) ||
    msg.uri.len==0 || msg.uri.len+msg.query.len+1>=sizeof(result->path) ||
    msg.proto.len!=8 || memcmp(msg.proto.buf,"HTTP/",5)!=0)return 0;
 memcpy(result->method,msg.method.buf,msg.method.len);
 memcpy(result->path,msg.uri.buf,msg.uri.len);
 if(msg.query.len){result->path[msg.uri.len]='?';memcpy(result->path+msg.uri.len+1,msg.query.buf,msg.query.len);}
 if(msg.proto.buf[5]<'0'||msg.proto.buf[5]>'9'||msg.proto.buf[6]!='.'||msg.proto.buf[7]<'0'||msg.proto.buf[7]>'9')return 0;
 result->major=msg.proto.buf[5]-'0';result->minor=msg.proto.buf[7]-'0';return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
