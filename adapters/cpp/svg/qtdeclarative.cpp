#include <QGuiApplication>
#include <QFileInfo>
#include <QQmlComponent>
#include <QQmlEngine>
#include <QQuickItem>
#include <QUrl>
#include <cstdio>
#include <memory>

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  QGuiApplication app(argc, argv);
  QQmlEngine engine;
  QQmlComponent component(&engine);
  component.setData("import QtQuick\nimport QtQuick.VectorImage\nVectorImage {}", QUrl());
  std::unique_ptr<QObject> object(component.create());
  if (!object) return 1;
  const auto path = QFileInfo(QString::fromLocal8Bit(argv[1])).absoluteFilePath();
  if (!object->setProperty("source", QUrl::fromLocalFile(path))) return 1;
  for (int i = 0; i < 100 && object->property("status").toInt() != 1; ++i)
    app.processEvents();
  auto* item = qobject_cast<QQuickItem*>(object.get());
  if (!item || object->property("status").toInt() != 1) return 1;
  std::printf("{\"width\":%.0f,\"height\":%.0f,\"ready\":true}\n",
              item->implicitWidth(), item->implicitHeight());
  return 0;
}
