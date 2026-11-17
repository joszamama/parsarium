#include "harness.h"
#include <Poco/Net/HTTPRequest.h>

#include <sstream>
#include <string>

bool parse_http_request(const uint8_t* data, std::size_t size, ParseResult& out) {
  if (!data || !size || size > (1u << 20)) return false;
  const std::string bytes(reinterpret_cast<const char*>(data), size);
  std::istringstream input(bytes, std::ios::in | std::ios::binary);
  try {
    Poco::Net::HTTPRequest request;
    request.read(input);
    const std::string version = request.getVersion();
    if (version.rfind("HTTP/", 0) != 0) return false;
    out = {request.getMethod(), request.getURI(), version.substr(5), request.getHost()};
    return !out.method.empty() && !out.path.empty();
  } catch (const std::exception&) {
    return false;
  }
}
