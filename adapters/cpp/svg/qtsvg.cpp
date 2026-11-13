#include <QImage>
#include <QPainter>
#include <QSvgRenderer>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  QSvgRenderer renderer(QString::fromLocal8Bit(argv[1]));
  if (!renderer.isValid()) return 1;
  const QSize size = renderer.defaultSize();
  if (size.width() != 2 || size.height() != 1) return 1;
  QImage image(size, QImage::Format_ARGB32);
  image.fill(Qt::transparent);
  QPainter painter(&image);
  renderer.render(&painter);
  painter.end();
  const QColor first = image.pixelColor(0, 0);
  const QColor second = image.pixelColor(1, 0);
  std::cout << "{\"width\":" << size.width() << ",\"height\":" << size.height()
            << ",\"first\":[" << first.red() << ',' << first.green() << ',' << first.blue()
            << "],\"second\":[" << second.red() << ',' << second.green() << ',' << second.blue()
            << "]}\n";
  return 0;
}
