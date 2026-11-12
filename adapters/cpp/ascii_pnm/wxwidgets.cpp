#include <wx/init.h>
#include <wx/image.h>
#include <wx/imagpnm.h>
#include <cstdio>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    wxInitializer initializer;
    if (!initializer.IsOk()) return 1;
    wxImage::AddHandler(new wxPNMHandler);
    wxImage image;
    if (!image.LoadFile(wxString::FromUTF8(argv[1]), wxBITMAP_TYPE_PNM)) return 1;
    if (image.GetWidth() != 2 || image.GetHeight() != 1) return 1;
    const unsigned char* pixels = image.GetData();
    if (!pixels) return 1;
    std::printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,255],"
                "\"second\":[%u,%u,%u,255]}\n",
                image.GetWidth(), image.GetHeight(),
                pixels[0], pixels[1], pixels[2], pixels[3], pixels[4], pixels[5]);
    return 0;
}
