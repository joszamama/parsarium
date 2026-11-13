#include <QCoreApplication>
#include <QFileInfo>
#include <QGuiApplication>
#include <QTimer>
#include <QUrl>
#include <QWebEnginePage>
#include <cstdio>

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  QGuiApplication app(argc, argv);
  QWebEnginePage page;
  bool passed = false;
  QObject::connect(&page, &QWebEnginePage::loadFinished, &app, [&](bool loaded) {
    if (!loaded) { app.quit(); return; }
    page.runJavaScript("JSON.stringify({root:document.documentElement.localName,"
                       "width:Number(document.documentElement.getAttribute('width')) ,"
                       "height:Number(document.documentElement.getAttribute('height')) ,"
                       "rectangles:document.querySelectorAll('rect').length})",
                       [&](const QVariant& result) {
      const auto json = result.toString().toUtf8();
      if (!json.isEmpty()) {
        std::printf("%s\n", json.constData());
        passed = true;
      }
      app.quit();
    });
  });
  QTimer::singleShot(15000, &app, &QCoreApplication::quit);
  page.load(QUrl::fromLocalFile(QFileInfo(QString::fromLocal8Bit(argv[1])).absoluteFilePath()));
  app.exec();
  return passed ? 0 : 1;
}
