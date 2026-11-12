#include "PDFDoc.h"
#include "GlobalParams.h"
#include <iostream>
int main(int argc, char** argv) {
    if (argc != 2) return 1;
    globalParams = new GlobalParams("");
    PDFDoc doc(argv[1]);
    if (!doc.isOk()) return 2;
    int pages = doc.getNumPages();
    if (pages < 1) return 3;
    std::cout << "{\"pages\":" << pages << "}\n";
    delete globalParams;
}
