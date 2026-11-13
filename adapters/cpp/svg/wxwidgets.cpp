#include <wx/wx.h>
#include <wx/bmpbndl.h>
#include <cstdio>

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  wxInitializer initializer;
  if (!initializer.IsOk()) return 1;
  auto bundle = wxBitmapBundle::FromSVGFile(wxString::FromUTF8(argv[1]), wxSize(2, 1));
  if (!bundle.IsOk()) return 1;
  auto image = bundle.GetBitmap(wxSize(2, 1)).ConvertToImage();
  if (!image.IsOk()) return 1;
  std::printf("{\"width\":%d,\"height\":%d,\"left_rgb\":[%u,%u,%u],\"right_rgb\":[%u,%u,%u]}\n",
              image.GetWidth(), image.GetHeight(), image.GetRed(0, 0),
              image.GetGreen(0, 0), image.GetBlue(0, 0), image.GetRed(1, 0),
              image.GetGreen(1, 0), image.GetBlue(1, 0));
  return 0;
}
