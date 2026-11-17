#include <Poco/JSON/Array.h>
#include <Poco/JSON/Object.h>
#include <Poco/JSON/ParseHandler.h>
#include <Poco/JSON/Parser.h>

#include <fstream>
#include <iterator>
#include <string>
#include <typeinfo>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string buffer(std::istreambuf_iterator<char>{file}, {});
    if (buffer.empty() || buffer.size() > (1u << 20)) return 2;
    try {
        Poco::JSON::Parser parser(new Poco::JSON::ParseHandler(true));
        const Poco::Dynamic::Var root = parser.parse(buffer);
        return root.type() == typeid(Poco::JSON::Object::Ptr) ||
               root.type() == typeid(Poco::JSON::Array::Ptr) ? 0 : 1;
    } catch (...) {
        return 1;
    }
}
