#include <stdio.h>

/* These C ABI declarations mirror the exported functions in unpdf 0.54.0. */
typedef struct UnpdfDocument UnpdfDocument;
extern UnpdfDocument *unpdf_parse_file(const char *path);
extern int unpdf_page_count(const UnpdfDocument *document);
extern void unpdf_free_document(UnpdfDocument *document);

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  UnpdfDocument *document = unpdf_parse_file(argv[1]);
  if (document == NULL) return 3;
  int pages = unpdf_page_count(document);
  unpdf_free_document(document);
  if (pages < 1) return 4;
  printf("{\"pages\":%d}\n", pages);
  return 0;
}
