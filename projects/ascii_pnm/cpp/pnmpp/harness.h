#ifndef PARSARIUM_PNMPP_HARNESS_H
#define PARSARIUM_PNMPP_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pnm_result { size_t width,height; int first[4],second[4]; };
bool parsarium_parse_pnm(const uint8_t *data,size_t size,struct parsarium_pnm_result *result);
#endif
