#include <SFML/Graphics/Image.hpp>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    sf::Image image;
    if (!image.loadFromFile(argv[1])) return 1;
    const auto size = image.getSize();
    if (size.x != 2 || size.y != 1) return 1;
    const auto first = image.getPixel({0, 0});
    const auto second = image.getPixel({1, 0});
    std::printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
                size.x, size.y, first.r, first.g, first.b, first.a,
                second.r, second.g, second.b, second.a);
    return 0;
}
