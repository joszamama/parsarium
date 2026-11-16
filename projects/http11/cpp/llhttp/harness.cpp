#include "harness.h"
#include <llhttp.h>
#include <string.h>
struct state {struct parsarium_http_result *result;size_t path_length;int headers_complete;};
static int on_url(llhttp_t *parser,const char *bytes,size_t length){
 struct state *s=(struct state *)parser->data;
 if(s->path_length+length>=sizeof(s->result->path))return -1;
 memcpy(s->result->path+s->path_length,bytes,length);s->path_length+=length;
 s->result->path[s->path_length]=0;return 0;
}
static int on_headers_complete(llhttp_t *parser){((struct state *)parser->data)->headers_complete=1;return 0;}
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;memset(result,0,sizeof(*result));
 struct state state={result,0,0};llhttp_settings_t settings;llhttp_settings_init(&settings);
 settings.on_url=on_url;settings.on_headers_complete=on_headers_complete;
 llhttp_t parser;llhttp_init(&parser,HTTP_REQUEST,&settings);parser.data=&state;
 llhttp_errno_t error=llhttp_execute(&parser,(const char *)data,size);
 if(error!=HPE_OK||llhttp_finish(&parser)!=HPE_OK||!state.headers_complete||!state.path_length)return 0;
 const char *method=llhttp_method_name((llhttp_method_t)llhttp_get_method(&parser));
 if(!method||strlen(method)>=sizeof(result->method))return 0;
 strcpy(result->method,method);result->major=llhttp_get_http_major(&parser);
 result->minor=llhttp_get_http_minor(&parser);return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
