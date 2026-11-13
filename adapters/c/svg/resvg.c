#include <resvg.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  resvg_options *options = resvg_options_create();
  if (!options) return 1;
  resvg_render_tree *tree = NULL;
  if (resvg_parse_tree_from_file(argv[1], options, &tree) != RESVG_OK || !tree) return 1;
  resvg_size size = resvg_get_image_size(tree);
  if (size.width != 2 || size.height != 1 || resvg_is_image_empty(tree)) return 1;
  unsigned char pixels[8] = {0};
  resvg_render(tree, resvg_transform_identity(), 2, 1, (char *)pixels);
  printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         (int)size.width, (int)size.height,
         pixels[0], pixels[1], pixels[2], pixels[4], pixels[5], pixels[6]);
  resvg_tree_destroy(tree);
  resvg_options_destroy(options);
  return 0;
}
