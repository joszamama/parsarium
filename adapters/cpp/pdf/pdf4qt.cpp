#include <pdfdocumentreader.h>

#include <QCoreApplication>

#include <iostream>

int main(int argc, char** argv) {
    QCoreApplication app(argc, argv);
    if (argc != 2) return 1;
    pdf::PDFDocumentReader reader(nullptr, [](bool* ok) {
        *ok = false;
        return QString();
    }, false, false);
    pdf::PDFDocument document = reader.readFromFile(QString::fromUtf8(argv[1]));
    if (reader.getReadingResult() != pdf::PDFDocumentReader::Result::OK) return 2;
    const size_t pages = document.getCatalog()->getPageCount();
    if (pages == 0) return 3;
    std::cout << "{\"pages\":" << pages << "}\n";
}
