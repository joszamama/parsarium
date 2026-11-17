#include <Poco/JSON/Array.h>
#include <Poco/JSON/Object.h>
#include <Poco/JSON/ParseHandler.h>
#include <Poco/JSON/Parser.h>

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <sstream>
#include <string>
#include <typeinfo>

static bool parse_json(const uint8_t* data, size_t size, bool print_tree) {
    if (!data || size == 0 || size > (1u << 20)) return false;
    try {
        Poco::JSON::Parser parser(new Poco::JSON::ParseHandler(true));
        const std::string buffer(reinterpret_cast<const char*>(data), size);
        const Poco::Dynamic::Var root = parser.parse(buffer);
        if (root.type() != typeid(Poco::JSON::Object::Ptr) &&
            root.type() != typeid(Poco::JSON::Array::Ptr)) return false;
        if (print_tree) {
            std::ostringstream output;
            if (root.type() == typeid(Poco::JSON::Object::Ptr))
                root.extract<Poco::JSON::Object::Ptr>()->stringify(output);
            else
                root.extract<Poco::JSON::Array::Ptr>()->stringify(output);
            const std::string text = output.str();
            std::fwrite(text.data(), 1, text.size(), stdout);
            std::putchar('\n');
        }
        return true;
    } catch (...) {
        return false;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    (void)parse_json(data, size, false);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    FILE* file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    auto* data = static_cast<uint8_t*>(std::malloc((1u << 20) + 1));
    if (!data) { std::fclose(file); return 4; }
    const size_t size = std::fread(data, 1, 1u << 20, file);
    if (std::ferror(file) || (size == (1u << 20) && std::fgetc(file) != EOF)) {
        std::free(data); std::fclose(file); return 4;
    }
    std::fclose(file);
    const bool parsed = parse_json(data, size, true);
    std::free(data);
    return parsed ? 0 : 5;
}
#endif
