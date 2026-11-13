#include <avcpp/av.h>
#include <avcpp/formatcontext.h>
#include <cstdio>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    av::init();
    av::FormatContext input;
    input.openInput(argv[1]);
    input.findStreamInfo();
    const char *format = input.inputFormat().name();
    if (format == nullptr || std::string(format).find("mp4") == std::string::npos) return 1;
    int video = 0;
    int audio = 0;
    for (size_t i = 0; i < input.streamsCount(); ++i) {
        auto stream = input.stream(i);
        video += stream.isVideo() ? 1 : 0;
        audio += stream.isAudio() ? 1 : 0;
    }
    std::printf("{\"format\":\"mp4\",\"streams\":%zu,\"video\":%d,\"audio\":%d}\n",
                input.streamsCount(), video, audio);
    return 0;
}
