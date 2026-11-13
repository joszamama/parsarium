#include <pdf_oxide/pdf_oxide.hpp>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    auto document = pdf_oxide::Document::open(argv[1]);
    std::cout << "{\"pages\":" << document.page_count() << "}\n";
  } catch (const pdf_oxide::Error &) {
    return 1;
  }
  return 0;
}
