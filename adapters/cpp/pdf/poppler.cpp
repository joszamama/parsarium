#include <poppler-document.h>

#include <iostream>
#include <memory>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    std::unique_ptr<poppler::document> pdf(poppler::document::load_from_file(argv[1]));
    if (!pdf || pdf->is_locked()) return 2;
    std::cout << "{\"pages\":" << pdf->pages() << "}\n";
}
