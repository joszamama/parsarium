#include <engine.h>
#include <scene.h>
#include <types.h>

#include <iostream>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    f3d::engine::autoloadPlugins();
    auto engine = f3d::engine::createNone();
    engine.getScene().add(argv[1]);
    const auto info = engine.getScene().getSceneInfo();
    std::cout << "{\"files\":" << info.numberOfFiles
              << ",\"actors\":" << info.numberOfActors
              << ",\"points\":" << info.numberOfPoints
              << ",\"cells\":" << info.numberOfCells << "}\n";
}
