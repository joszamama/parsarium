#ifndef PARSARIUM_EXIV2_MP4_HARNESS_H
#define PARSARIUM_EXIV2_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
#include <string>
struct parsarium_mp4_result {
 // Each field is set only when Exiv2 reported it (has_* is nonzero).
 int has_brand; std::string brand;
 int has_width; long width;
 int has_height; long height;
 // Exiv2's reason, or the call that failed, when the file is rejected.
 std::string error;
};
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
#endif
