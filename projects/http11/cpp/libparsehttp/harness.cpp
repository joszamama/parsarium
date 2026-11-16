#include "harness.h"
#include <assert.h>
extern "C" {
#include <parsehttp.h>
}
#include <stdlib.h>
#include <string.h>
struct state { struct parsarium_http_result *result; int complete,error; };
static void save(char *to,size_t cap,const char *from,struct state *s){
 size_t n=strlen(from);if(n>=cap){s->error=1;return;}memcpy(to,from,n+1);
}
static void method(const char *v,void *p){struct state *s=(struct state *)p;save(s->result->method,sizeof(s->result->method),v,s);}
static void path(const char *v,void *p){struct state *s=(struct state *)p;save(s->result->path,sizeof(s->result->path),v,s);}
static void query(const char *v,void *p){struct state *s=(struct state *)p;save(s->result->query,sizeof(s->result->query),v,s);}
static void version(const char *v,void *p){struct state *s=(struct state *)p;save(s->result->version,sizeof(s->result->version),v,s);}
static void host(const char *v,int port,void *p){struct state *s=(struct state *)p;if(port!=0)s->error=1;save(s->result->host,sizeof(s->result->host),v,s);}
static void complete(void *p){((struct state *)p)->complete=1;}
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 memset(result,0,sizeof(*result));struct state state={result,0,0};
 char *copy=(char *)malloc(size+1);if(!copy)return 0;memcpy(copy,data,size);copy[size]=0;
 parsehttp_t parser;if(parse_init(&parser)!=&parser||parse_version()!=LIBPARSEHTTP_VERSION){free(copy);return 0;}
 parse_setarg(&parser,&state);parse_setcb_method(&parser,method);parse_setcb_path(&parser,path);
 parse_setcb_params(&parser,query);parse_setcb_version(&parser,version);
 parse_setcb_host(&parser,host);parse_setcb_complete(&parser,complete);
 int remaining=parse_process(&parser,copy,(int)size);parse_free(&parser);free(copy);
 return remaining==0&&state.complete&&!state.error;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
