#include <Magick++.h>
#include <cstdio>
#include <exception>
#include <vector>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    Magick::InitializeMagick(argv[0]);
    std::vector<Magick::Image> pages;
    Magick::readImages(&pages, argv[1]);
    if (pages.empty()) return 1;
    std::printf("{\"pages\":%zu,\"width\":%zu,\"height\":%zu}\n",
                pages.size(), static_cast<size_t>(pages[0].columns()),
                static_cast<size_t>(pages[0].rows()));
    return 0;
  } catch (const std::exception &error) {
    std::fprintf(stderr, "%s\n", error.what());
    return 1;
  }
}
