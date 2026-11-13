#include <gtk/gtk.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  gtk_init();
  char *data = NULL;
  gsize length = 0;
  if (!g_file_get_contents(argv[1], &data, &length, NULL)) return 3;
  GBytes *bytes = g_bytes_new_take(data, length);
  GtkSvg *svg = gtk_svg_new_from_bytes(bytes);
  if (!svg) return 4;
  printf("{\"width\":%d,\"height\":%d}\n",
         gdk_paintable_get_intrinsic_width(GDK_PAINTABLE(svg)),
         gdk_paintable_get_intrinsic_height(GDK_PAINTABLE(svg)));
  g_object_unref(svg);
  g_bytes_unref(bytes);
  return 0;
}
