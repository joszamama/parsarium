#include <resvg.h>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  resvg_options *options = resvg_options_create();
  if (!options) return 1;
  resvg_render_tree *tree = nullptr;
  if (resvg_parse_tree_from_file(argv[1], options, &tree) != RESVG_OK || !tree) return 1;
  resvg_size size = resvg_get_image_size(tree);
  if (size.width != 2 || size.height != 1 || resvg_is_image_empty(tree)) return 1;
  unsigned char pixels[8] = {0};
  resvg_render(tree, resvg_transform_identity(), 2, 1, reinterpret_cast<char *>(pixels));
  std::cout << "{\"width\":" << (int)size.width << ",\"height\":" << (int)size.height
            << ",\"first\":[" << (unsigned)pixels[0] << ',' << (unsigned)pixels[1]
            << ',' << (unsigned)pixels[2] << "],\"second\":["
            << (unsigned)pixels[4] << ',' << (unsigned)pixels[5] << ','
            << (unsigned)pixels[6] << "]}\n";
  resvg_tree_destroy(tree);
  resvg_options_destroy(options);
  return 0;
}
