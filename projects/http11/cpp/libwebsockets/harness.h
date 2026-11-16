#ifndef PARSARIUM_LIBWEBSOCKETS_CPP_HTTP11_HARNESS_H
#define PARSARIUM_LIBWEBSOCKETS_CPP_HTTP11_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <string>

struct ParsariumHttpResult {
    std::string method;
    std::string path;
    std::string host;
};

bool parsarium_parse_http(const std::uint8_t *data, std::size_t size,
                          ParsariumHttpResult *result);

#endif
