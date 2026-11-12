#include <podofo/podofo.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    PoDoFo::PdfMemDocument pdf;
    pdf.Load(argv[1]);
    std::cout << "{\"pages\":" << pdf.GetPages().GetCount() << "}\n";
}
