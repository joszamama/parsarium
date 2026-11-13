#include <QImageReader>
#include <QImage>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  QImageReader reader(QString::fromLocal8Bit(argv[1]), "svg");
  QImage image = reader.read();
  if (image.isNull() || image.width() != 2 || image.height() != 1) return 1;
  const QColor first = image.pixelColor(0, 0);
  const QColor second = image.pixelColor(1, 0);
  std::cout << "{\"width\":" << image.width() << ",\"height\":" << image.height()
            << ",\"first\":[" << first.red() << ',' << first.green() << ',' << first.blue()
            << "],\"second\":[" << second.red() << ',' << second.green() << ',' << second.blue()
            << "]}\n";
  return 0;
}
