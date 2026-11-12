#include <boost/gil.hpp>
#include <boost/gil/extension/io/pnm.hpp>
#include <cstdio>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    try {
        boost::gil::rgb8_image_t image;
        boost::gil::read_image(argv[1], image, boost::gil::pnm_tag());
        const auto view = boost::gil::const_view(image);
        if (view.width() != 2 || view.height() != 1) return 1;
        const auto first = view(0, 0);
        const auto second = view(1, 0);
        std::printf("{\"width\":%td,\"height\":%td,\"first\":[%u,%u,%u,255],"
                    "\"second\":[%u,%u,%u,255]}\n",
                    view.width(), view.height(),
                    static_cast<unsigned>(boost::gil::at_c<0>(first)),
                    static_cast<unsigned>(boost::gil::at_c<1>(first)),
                    static_cast<unsigned>(boost::gil::at_c<2>(first)),
                    static_cast<unsigned>(boost::gil::at_c<0>(second)),
                    static_cast<unsigned>(boost::gil::at_c<1>(second)),
                    static_cast<unsigned>(boost::gil::at_c<2>(second)));
        return 0;
    } catch (const std::exception&) {
        return 1;
    }
}
