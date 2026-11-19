#include "harness.h"
#include <boost/asio/buffer.hpp>
#include <boost/beast/http.hpp>
namespace http = boost::beast::http;
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 // A string body lets Beast read a message body the request declares, the way
 // http::read does (eager parsing until the message is complete).
 http::request_parser<http::string_body> parser;
 parser.header_limit(1u<<20);
 parser.eager(true);
 boost::system::error_code error;
 size_t offset=0;
 while(!parser.is_done()&&offset<size){
  size_t consumed=parser.put(boost::asio::buffer(data+offset,size-offset),error);
  if(error)return 0;
  if(consumed==0)break;
  offset+=consumed;
 }
 if(!parser.is_done()){
  parser.put_eof(error);
  if(error||!parser.is_done())return 0;
 }
 const auto &request=parser.get();
 result->method=std::string(request.method_string());
 result->path=std::string(request.target());
 result->major=request.version()/10;result->minor=request.version()%10;
 result->host=std::string(request[http::field::host]);
 return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
