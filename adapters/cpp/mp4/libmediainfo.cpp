#include <MediaInfo/MediaInfo.h>
#include <cstring>
#include <iostream>
#include <string>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  MediaInfoLib::MediaInfo info;
  const std::wstring path(argv[1], argv[1] + std::strlen(argv[1]));
  if (!info.Open(path)) return 1;
  const std::wstring container = info.Get(MediaInfoLib::Stream_General, 0, L"Format");
  const std::wstring title = info.Get(MediaInfoLib::Stream_General, 0, L"Title");
  const std::wstring video = info.Get(MediaInfoLib::Stream_Video, 0, L"Format");
  const std::wstring audio = info.Get(MediaInfoLib::Stream_Audio, 0, L"Format");
  const std::wstring width = info.Get(MediaInfoLib::Stream_Video, 0, L"Width");
  const std::wstring height = info.Get(MediaInfoLib::Stream_Video, 0, L"Height");
  if (container.empty() || title.empty() || video.empty() || audio.empty() || width.empty() || height.empty()) return 1;
  std::wcout << L"{\"container\":\"" << container << L"\",\"title\":\"" << title
             << L"\",\"video\":\"" << video << L"\",\"audio\":\"" << audio
             << L"\",\"width\":" << width << L",\"height\":" << height << L"}\n";
  info.Close();
  return 0;
}
