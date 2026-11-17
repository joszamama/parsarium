#include "harness.h"
#include <boost/asio/buffer.hpp>
#include <boost/beast/http.hpp>
namespace http = boost::beast::http;
int parsarium_parse_http(const uint8_t *data,size_t size,struct parsarium_http_result *result){
 if(!data||!result||!size||size>(1u<<20))return 0;
 http::request_parser<http::empty_body> parser;
 parser.header_limit(1u<<20);
 boost::system::error_code error;
 size_t consumed=parser.put(boost::asio::buffer(data,size),error);
 if(error||consumed!=size||!parser.is_done())return 0;
 const auto &request=parser.get();
 result->method=std::string(request.method_string());
 result->path=std::string(request.target());
 result->major=request.version()/10;result->minor=request.version()%10;
 result->host=std::string(request[http::field::host]);
 return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size){struct parsarium_http_result r;(void)parsarium_parse_http(data,size,&r);return 0;}
