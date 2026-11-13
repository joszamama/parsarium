#include <quicktime.h>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    quicktime_t *file = quicktime_open(argv[1], 1, 0);
    if (file == nullptr) return 1;
    int video = quicktime_video_tracks(file);
    int audio = quicktime_audio_tracks(file);
    if (video < 1 || audio < 1) {
        quicktime_close(file);
        return 1;
    }
    std::printf("{\"video_tracks\":%d,\"audio_tracks\":%d,\"width\":%d,\"height\":%d}\n",
                video, audio, quicktime_video_width(file, 0), quicktime_video_height(file, 0));
    quicktime_close(file);
    return 0;
}
