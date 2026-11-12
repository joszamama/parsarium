#include <QCoreApplication>
#include <QImageReader>
#include <QImage>
#include <QColor>
#include <cstdio>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    QCoreApplication app(argc, argv);
    QImageReader reader(QString::fromUtf8(argv[1]), "ppm");
    const QImage image = reader.read();
    if (image.isNull() || image.width() != 2 || image.height() != 1) return 1;
    const QColor first = image.pixelColor(0, 0);
    const QColor second = image.pixelColor(1, 0);
    std::printf("{\"width\":%d,\"height\":%d,\"first\":[%d,%d,%d,%d],"
                "\"second\":[%d,%d,%d,%d]}\n",
                image.width(), image.height(),
                first.red(), first.green(), first.blue(), first.alpha(),
                second.red(), second.green(), second.blue(), second.alpha());
    return 0;
}
