#include <pdf_oxide_c/pdf_oxide.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  int32_t error = 0;
  PdfDocument *document = pdf_document_open(argv[1], &error);
  if (!document || error != 0) return 1;
  int32_t pages = pdf_document_get_page_count(document, &error);
  pdf_document_free(document);
  if (error != 0 || pages < 0) return 1;
  printf("{\"pages\":%d}\n", pages);
  return 0;
}
