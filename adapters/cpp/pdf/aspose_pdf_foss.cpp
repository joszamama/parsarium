#include <aspose/pdf/document.hpp>
#include <aspose/pdf/page_collection.hpp>
#include <cstdio>
#include <exception>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    Aspose::Pdf::Document document(argv[1]);
    const auto count = document.Pages().Count();
    if (count == 0) return 1;
    std::printf("{\"pages\":%zu}\n", static_cast<size_t>(count));
    return 0;
  } catch (const std::exception &error) {
    std::fprintf(stderr, "%s\n", error.what());
    return 1;
  }
}
