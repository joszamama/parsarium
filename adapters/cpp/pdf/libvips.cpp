#include <vips/vips8>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (VIPS_INIT(argv[0])) return 1;
  try {
    {
      vips::VImage image = vips::VImage::pdfload(argv[1]);
      const int pages = image.get_int("n-pages");
      std::printf("{\"pages\":%d,\"width\":%d,\"height\":%d}\n",
                  pages, image.width(), image.height());
    }
    vips_shutdown();
    return 0;
  } catch (const vips::VError &error) {
    std::fprintf(stderr, "%s\n", error.what());
    vips_shutdown();
    return 1;
  }
}
