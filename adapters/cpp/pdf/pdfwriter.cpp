#include <InputFile.h>
#include <PDFParser.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    InputFile file;
    if (file.OpenFile(argv[1]) != PDFHummus::eSuccess) return 2;
    PDFParser parser;
    if (parser.StartPDFParsing(file.GetInputStream()) != PDFHummus::eSuccess) return 3;
    const unsigned long pages = parser.GetPagesCount();
    if (pages == 0) return 4;
    std::cout << "{\"pages\":" << pages << "}\n";
}
