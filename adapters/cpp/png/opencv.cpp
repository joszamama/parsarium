#include <opencv2/imgcodecs.hpp>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    const cv::Mat image = cv::imread(argv[1], cv::IMREAD_UNCHANGED);
    if (image.empty() || image.type() != CV_8UC4 || image.cols < 2 || image.rows < 1) return 3;
    const auto first = image.at<cv::Vec4b>(0, 0);
    const auto second = image.at<cv::Vec4b>(0, 1);
    std::cout << "{\"width\":" << image.cols << ",\"height\":" << image.rows
              << ",\"first\":[" << +first[2] << ',' << +first[1] << ',' << +first[0] << ',' << +first[3]
              << "],\"second\":[" << +second[2] << ',' << +second[1] << ',' << +second[0] << ',' << +second[3]
              << "]}\n";
}
