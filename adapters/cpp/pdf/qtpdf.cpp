#include <QCoreApplication>
#include <QPdfDocument>
#include <QString>
#include <iostream>
int main(int argc, char** argv) {
    QCoreApplication app(argc, argv);
    if (argc != 2) return 1;
    QPdfDocument doc;
    auto error = doc.load(QString::fromUtf8(argv[1]));
    if (error != QPdfDocument::Error::None) return 2;
    int pages = doc.pageCount();
    if (pages < 1) return 3;
    std::cout << "{\"pages\":" << pages << "}\n";
}
