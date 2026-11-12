#include <cstdio>
#include <vanillapdf/c_vanillapdf_api.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  DocumentHandle *document = nullptr;
  CatalogHandle *catalog = nullptr;
  PageTreeHandle *tree = nullptr;
  PageObjectHandle *page = nullptr;
  size_type count = 0;
  int status = 1;

  if (Logging_SetSeverity(LoggingSeverity_Off) != VANILLAPDF_ERROR_SUCCESS) goto done;
  if (Document_Open(argv[1], &document) != VANILLAPDF_ERROR_SUCCESS) goto done;
  if (Document_GetCatalog(document, &catalog) != VANILLAPDF_ERROR_SUCCESS) goto done;
  if (Catalog_GetPages(catalog, &tree) != VANILLAPDF_ERROR_SUCCESS) goto done;
  if (PageTree_GetPageCount(tree, &count) != VANILLAPDF_ERROR_SUCCESS) goto done;
  if (count == 0 || PageTree_GetPage(tree, 1, &page) != VANILLAPDF_ERROR_SUCCESS) goto done;
  std::printf("{\"pages\":%zu}\n", static_cast<size_t>(count));
  status = 0;

done:
  if (page) PageObject_Release(page);
  if (tree) PageTree_Release(tree);
  if (catalog) Catalog_Release(catalog);
  if (document) Document_Release(document);
  return status;
}
