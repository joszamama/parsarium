#include <cstdio>
#include "tspdf.h"

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  TspdfError error{};
  TspdfReader *document = tspdf_reader_open_file(argv[1], &error);
  if (!document) return 1;
  size_t count = tspdf_reader_page_count(document);
  if (!count || !tspdf_reader_get_page(document, 0)) {
    tspdf_reader_destroy(document);
    return 1;
  }
  std::printf("{\"pages\":%zu}\n", count);
  tspdf_reader_destroy(document);
  return 0;
}
