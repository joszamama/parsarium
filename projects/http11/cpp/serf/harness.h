#ifndef PARSARIUM_SERF_CPP_HTTP11_HARNESS_H
#define PARSARIUM_SERF_CPP_HTTP11_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <string>

struct ParsariumHttpResponse {
    int major;
    int minor;
    int status;
    std::string reason;
    bool has_content_type;
    std::string content_type;
    std::string body;
};

bool parsarium_parse_http_response(const std::uint8_t *data, std::size_t size,
                                   ParsariumHttpResponse *result);

#endif
