#include <MediaInfo/MediaInfo.h>
#include <cstring>
#include <iostream>
#include <string>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  MediaInfoLib::MediaInfo info;
  const std::wstring path(argv[1], argv[1] + std::strlen(argv[1]));
  if (!info.Open(path)) return 1;
  const std::wstring format = info.Get(MediaInfoLib::Stream_Audio, 0, L"Format");
  const std::wstring title = info.Get(MediaInfoLib::Stream_General, 0, L"Title");
  const std::wstring sample_rate = info.Get(MediaInfoLib::Stream_Audio, 0, L"SamplingRate");
  if (format != L"MPEG Audio" || title.empty() || sample_rate.empty()) return 1;
  std::wcout << L"{\"title\":\"" << title << L"\",\"format\":\"" << format
             << L"\",\"sample_rate\":" << sample_rate << L"}\n";
  info.Close();
  return 0;
}
