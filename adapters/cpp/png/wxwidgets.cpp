#include <wx/image.h>
#include <wx/imagpng.h>
#include <wx/init.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    wxInitializer initializer;
    if (!initializer) return 3;
    wxImage::AddHandler(new wxPNGHandler());
    wxImage image;
    if (!image.LoadFile(argv[1], wxBITMAP_TYPE_PNG) || !image.IsOk()) return 4;
    if (image.GetWidth() < 2 || image.GetHeight() < 1) return 5;
    std::cout << "{\"width\":" << image.GetWidth() << ",\"height\":" << image.GetHeight()
              << ",\"first\":[" << +image.GetRed(0, 0) << ',' << +image.GetGreen(0, 0)
              << ',' << +image.GetBlue(0, 0)
              << "],\"second\":[" << +image.GetRed(1, 0) << ',' << +image.GetGreen(1, 0)
              << ',' << +image.GetBlue(1, 0)
              << "]}\n";
}
