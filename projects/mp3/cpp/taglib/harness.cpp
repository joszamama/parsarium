#include "harness.h"
#include <string.h>
#include <mpegfile.h>
#include <mpegproperties.h>
#include <tbytevector.h>
#include <tbytevectorstream.h>
// Read the whole byte buffer through TagLib's in-memory stream and report the
// MPEG frame-header properties of an untagged Layer III stream.
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    TagLib::ByteVector bytes(reinterpret_cast<const char *>(data), static_cast<unsigned int>(size));
    TagLib::ByteVectorStream stream(bytes);
    TagLib::MPEG::File file(&stream, true, TagLib::AudioProperties::Accurate);
    if (!file.isValid() || file.hasID3v2Tag() || file.hasID3v1Tag() || file.hasAPETag()) return 0;
    const TagLib::MPEG::Properties *p = file.audioProperties();
    if (!p || p->layer() != 3 || p->sampleRate() <= 0 || p->channels() <= 0) return 0;
    switch (p->version()) {
    case TagLib::MPEG::Header::Version1: result->version = 1; break;
    case TagLib::MPEG::Header::Version2: result->version = 2; break;
    default: return 0;
    }
    result->layer = static_cast<unsigned>(p->layer());
    result->sample_rate = static_cast<unsigned>(p->sampleRate());
    result->channels = static_cast<unsigned>(p->channels());
    result->bitrate_kbps = static_cast<unsigned>(p->bitrate());
    result->length_ms = static_cast<unsigned>(p->lengthInMilliseconds());
    return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result; (void)parsarium_parse_mp3(data, size, &result); return 0;
}
