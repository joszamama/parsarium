#include <qpdf/qpdf-c.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    qpdf_data pdf = qpdf_init();
    if (pdf == NULL) return 2;
    if ((qpdf_read(pdf, argv[1], NULL) & QPDF_ERRORS) != 0) {
        qpdf_cleanup(&pdf);
        return 3;
    }
    int pages = qpdf_get_num_pages(pdf);
    qpdf_cleanup(&pdf);
    if (pages <= 0) return 4;
    printf("{\"pages\":%d}\n", pages);
    return 0;
}
