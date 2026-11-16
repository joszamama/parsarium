#include "harness.h"
#include <string.h>
#include <stdlib.h>
#define HTTPP_IMPLEMENTATION
#include <httpp.h>
static int parse_copy(char *copy,size_t size,struct parsarium_http_result *result){
 memset(result,0,sizeof(*result));httpp_req_t request;
 httpp_header_t headers[HTTPP_DEFAULT_HEADERS_ARR_CAP];
 httpp_init_req(&request,headers,HTTPP_DEFAULT_HEADERS_ARR_CAP);
 if(httpp_parse_request(copy,size,&request)<0)return 0;
 const char *method=httpp_method_to_string(request.method);
 if(!method||strlen(method)>=sizeof(result->method)||!request.route.ptr||
    request.route.length==0||request.route.length>=sizeof(result->path)||
    request.version.length!=8||memcmp(request.version.ptr,"HTTP/",5)!=0)return 0;
 strcpy(result->method,method);memcpy(result->path,request.route.ptr,request.route.length);
 if(request.version.ptr[5]<'0'||request.version.ptr[5]>'9'||request.version.ptr[6]!='.'||
    request.version.ptr[7]<'0'||request.version.ptr[7]>'9')return 0;
 result->major=request.version.ptr[5]-'0';result->minor=request.version.ptr[7]-'0';return 1;
}
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 char *copy=(char *)malloc(size+1);if(!copy)return 0;
 memcpy(copy,data,size);copy[size]=0;
 int ok=parse_copy(copy,size,result);free(copy);return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
