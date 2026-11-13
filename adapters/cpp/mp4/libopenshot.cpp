#include <libopenshot/FFmpegReader.h>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    openshot::FFmpegReader reader(argv[1]);
    reader.Open();
    std::printf("{\"video\":%d,\"audio\":%d,\"width\":%d,\"height\":%d,\"video_codec\":\"%s\",\"audio_codec\":\"%s\"}\n",
                reader.info.has_video ? 1 : 0, reader.info.has_audio ? 1 : 0,
                reader.info.width, reader.info.height,
                reader.info.vcodec.c_str(), reader.info.acodec.c_str());
    reader.Close();
    return 0;
}
