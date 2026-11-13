#define LOK_USE_UNSTABLE_API
#include <LibreOfficeKit/LibreOfficeKitInit.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* LibreOfficeKitEnums.h in 26.8.3.1 uses C++ syntax in an inline helper, so
 * mirror only its documented LOK_DOCTYPE_DRAWING enum value for this C build. */
enum { LOK_DRAWING_DOCUMENT_TYPE = 3 };

int main(int argc, char **argv) {
    if (argc != 4 || argv[1][0] != '/') return 2;
    const char *path = argv[1];
    const char *frameworks = argv[2];
    const char *profile_url = argv[3];
    size_t length = strlen(path) + sizeof("file://");
    char *url = malloc(length);
    if (url == NULL) return 1;
    snprintf(url, length, "file://%s", path);

    LibreOfficeKit *kit = lok_init_2(frameworks, profile_url);
    if (kit == NULL) {
        free(url);
        return 1;
    }
    LibreOfficeKitDocument *document = kit->pClass->documentLoad(kit, url);
    free(url);
    if (document == NULL) {
        fprintf(stderr, "documentLoad: %s\n", kit->pClass->getError(kit));
        kit->pClass->destroy(kit);
        return 1;
    }
    int type = document->pClass->getDocumentType(document);
    int pages = document->pClass->getParts(document);
    document->pClass->destroy(document);
    kit->pClass->destroy(kit);
    if (type != LOK_DRAWING_DOCUMENT_TYPE || pages < 1) return 1;
    printf("{\"type\":\"drawing\",\"pages\":%d}\n", pages);
    return 0;
}
