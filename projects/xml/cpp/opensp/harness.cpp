#include "harness.h"

#include <ParserEventGeneratorKit.h>

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

// OpenSP parses XML through its SGML parser with the XML SGML declaration
// (pubtext/xml.soc -> xml.dcl), as doc/xml.htm documents: SP_CHARSET_FIXED=YES,
// SP_ENCODING=XML, the xml.soc catalog and the "xml" and "no-valid" warning
// options. SGML has no Namespaces in XML: element names (generic identifiers)
// and attribute names are reported as written, and xmlns/xmlns:* are ordinary
// attributes. This is a raw-name path; the adapter resolves nothing.

static const char *const catalog = "/work/source/pubtext/xml.soc";

static void append_utf8(std::string *out, SGMLApplication::Char c) {
    if (c < 0x80) {
        out->push_back(static_cast<char>(c));
    } else if (c < 0x800) {
        out->push_back(static_cast<char>(0xC0 | (c >> 6)));
        out->push_back(static_cast<char>(0x80 | (c & 0x3F)));
    } else if (c < 0x10000) {
        out->push_back(static_cast<char>(0xE0 | (c >> 12)));
        out->push_back(static_cast<char>(0x80 | ((c >> 6) & 0x3F)));
        out->push_back(static_cast<char>(0x80 | (c & 0x3F)));
    } else {
        out->push_back(static_cast<char>(0xF0 | (c >> 18)));
        out->push_back(static_cast<char>(0x80 | ((c >> 12) & 0x3F)));
        out->push_back(static_cast<char>(0x80 | ((c >> 6) & 0x3F)));
        out->push_back(static_cast<char>(0x80 | (c & 0x3F)));
    }
}

static std::string utf8(const SGMLApplication::CharString &text) {
    std::string out;
    for (size_t i = 0; i < text.len; i++) append_utf8(&out, text.ptr[i]);
    return out;
}

class Summary : public SGMLApplication {
public:
    explicit Summary(parsarium_xml_result *result) : result_(result) {}
    bool failed = false;

    void startElement(const StartElementEvent &event) override {
        flush();
        depth_++;
        result_->max_depth = std::max(result_->max_depth, depth_);
        result_->elements.push_back(utf8(event.gi));
        for (size_t i = 0; i < event.nAttributes; i++) {
            const Attribute &attribute = event.attributes[i];
            // Only attributes present in the start tag; the implied attribute
            // definitions OpenSP creates for other elements of the same type
            // are reported as implied and skipped.
            if (attribute.type == Attribute::implied || attribute.type == Attribute::invalid) continue;
            if (attribute.defaulted != Attribute::specified) continue;
            std::string value;
            if (attribute.type == Attribute::cdata) {
                for (size_t j = 0; j < attribute.nCdataChunks; j++) {
                    const Attribute::CdataChunk &chunk = attribute.cdataChunks[j];
                    if (chunk.isNonSgml) append_utf8(&value, chunk.nonSgmlChar);
                    else value += utf8(chunk.data);
                }
            } else {
                value = utf8(attribute.tokens);
            }
            result_->attributes.push_back(utf8(attribute.name) + "=" + value);
        }
    }
    void endElement(const EndElementEvent &) override {
        flush();
        depth_--;
    }
    void data(const DataEvent &event) override { text_ += utf8(event.data); }
    void pi(const PiEvent &) override { flush(); }
    void commentDecl(const CommentDeclEvent &) override { flush(); }
    void error(const ErrorEvent &event) override {
        if (event.type != ErrorEvent::info && event.type != ErrorEvent::warning) failed = true;
    }

private:
    void flush() {
        size_t first = text_.find_first_not_of(" \t\r\n");
        if (first != std::string::npos) {
            size_t last = text_.find_last_not_of(" \t\r\n");
            result_->text.push_back(text_.substr(first, last - first + 1));
        }
        text_.clear();
    }

    parsarium_xml_result *result_;
    std::string text_;
    int64_t depth_ = 0;
};

int parsarium_parse_xml(const uint8_t *data, size_t size, parsarium_xml_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    // OpenSP reads documents through its storage managers; the local bytes are
    // written to a private temporary file and parsed from there.
    char path[] = "/tmp/parsarium-opensp-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(fd, data + written, size - written);
        if (n <= 0) break;
        written += static_cast<size_t>(n);
    }
    close(fd);
    if (written != size) {
        unlink(path);
        return 0;
    }
    setenv("SP_CHARSET_FIXED", "YES", 1);
    setenv("SP_ENCODING", "XML", 1);
    ParserEventGeneratorKit kit;
    kit.setOption(ParserEventGeneratorKit::addCatalog, catalog);
    kit.setOption(ParserEventGeneratorKit::enableWarning, "xml");
    kit.setOption(ParserEventGeneratorKit::enableWarning, "no-valid");
    char *files[] = {path};
    EventGenerator *generator = kit.makeEventGenerator(1, files);
    Summary summary(result);
    unsigned errors = generator->run(summary);
    delete generator;
    unlink(path);
    if (errors || summary.failed || result->elements.empty()) {
        *result = parsarium_xml_result();
        return 0;
    }
    result->root = result->elements.front();
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_xml_result result;
    (void)parsarium_parse_xml(data, size, &result);
    return 0;
}
