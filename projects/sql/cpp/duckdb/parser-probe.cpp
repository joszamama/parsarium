// Parser-only probe: duckdb::Parser::ParseQuery on the local bytes; no printing, no database.
#include <cstdio>
#include <cstring>
#include <exception>
#include <string>
#include <vector>

#include "duckdb/parser/parser.hpp"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 2;
    std::vector<char> data(1u << 20);
    size_t size = std::fread(data.data(), 1, data.size(), file);
    std::fclose(file);
    if (size == 0 || size == data.size() || std::memchr(data.data(), 0, size)) return 2;
    try {
        duckdb::Parser parser = duckdb::Parser::GetBuiltinParser();
        parser.ParseQuery(std::string(data.data(), size));
        return parser.statements.empty() ? 1 : 0;
    } catch (std::exception &) {
        return 1;
    }
}
