#include "harness.h"
#include <iostream>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::size_t pages = 0;
    if (!parsarium_parse_pdf_file(argv[1], pages)) return 1;
    std::cout << "{\"pages\":" << pages << "}\n";
    return 0;
}
