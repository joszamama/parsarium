#include "parse.h"

#include <iostream>
#include <optional>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    loguru::init(argc, argv);
    std::string filename = argv[1];
    std::optional<std::string> password;
    pdflib::pdf_decoder<pdflib::DOCUMENT> document;
    if (!document.process_document_from_file(filename, password)) return 2;
    int pages = document.get_number_of_pages();
    if (pages < 1) return 3;
    std::cout << "{\"pages\":" << pages << "}\n";
}
