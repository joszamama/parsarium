#include <opencv2/videoio.hpp>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    cv::VideoCapture video(argv[1], cv::CAP_FFMPEG);
    if (!video.isOpened()) return 1;
    std::printf("{\"width\":%.0f,\"height\":%.0f,\"frames\":%.0f,\"fps\":%.0f}\n",
                video.get(cv::CAP_PROP_FRAME_WIDTH), video.get(cv::CAP_PROP_FRAME_HEIGHT),
                video.get(cv::CAP_PROP_FRAME_COUNT), video.get(cv::CAP_PROP_FPS));
    return 0;
}
