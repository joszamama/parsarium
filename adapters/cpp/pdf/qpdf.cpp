#include <qpdf/QPDF.hh>
#include <qpdf/QPDFPageDocumentHelper.hh>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    QPDF pdf;
    pdf.processFile(argv[1]);
    std::cout << "{\"pages\":" << QPDFPageDocumentHelper(pdf).getAllPages().size() << "}\n";
}
