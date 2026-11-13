/* Host shim for the documented zathura-pdf-poppler document_open callback.
 * The released plugin's document.c is compiled unchanged beside this file.
 */
#include <stdio.h>
#include <glib.h>

#include "plugin.h"

struct zathura_document_s {
  const char* path;
  const char* password;
  unsigned int pages;
  void* data;
};

const char* zathura_document_get_path(zathura_document_t* document) { return document->path; }
const char* zathura_document_get_password(zathura_document_t* document) { return document->password; }
void zathura_document_set_data(zathura_document_t* document, void* data) { document->data = data; }
void zathura_document_set_number_of_pages(zathura_document_t* document, unsigned int pages) { document->pages = pages; }
unsigned int zathura_document_get_number_of_pages(zathura_document_t* document) { return document->pages; }

int main(int argc, char** argv) {
  if (argc != 2) {
    fprintf(stderr, "expected one local PDF path\n");
    return 2;
  }
  char* path = g_canonicalize_filename(argv[1], NULL);
  zathura_document_t document = {.path = path};
  zathura_error_t error = pdf_document_open(&document);
  if (error != ZATHURA_ERROR_OK) {
    fprintf(stderr, "zathura-pdf-poppler document_open error %d\n", error);
    g_free(path);
    return 1;
  }
  printf("{\"pages\":%u,\"has_parser_data\":%s}\n",
         zathura_document_get_number_of_pages(&document), document.data ? "true" : "false");
  error = pdf_document_free(&document, document.data);
  g_free(path);
  return error == ZATHURA_ERROR_OK ? 0 : 1;
}
