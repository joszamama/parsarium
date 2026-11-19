#include "harness.h"
#include <mongoose.h>
#include <string.h>
/* mg_http_parse returns the length of the request head; any message body that
   follows it is left to the caller, so trailing body bytes are not an error. */
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));struct mg_http_message msg;
 int consumed=mg_http_parse((const char *)data,size,&msg);
 if(consumed<=0 || msg.proto.len!=8 || memcmp(msg.proto.buf,"HTTP/",5)!=0)return 0;
 if(msg.proto.buf[5]<'0'||msg.proto.buf[5]>'9'||msg.proto.buf[6]!='.'||msg.proto.buf[7]<'0'||msg.proto.buf[7]>'9')return 0;
 result->method=msg.method.buf;result->method_len=msg.method.len;
 result->uri=msg.uri.buf;result->uri_len=msg.uri.len;
 result->query=msg.query.buf;result->query_len=msg.query.len;
 result->major=msg.proto.buf[5]-'0';result->minor=msg.proto.buf[7]-'0';return 1;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
