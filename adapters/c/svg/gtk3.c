#include <gtk/gtk.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  gtk_init(&argc, &argv);
  GtkWidget *widget = gtk_image_new_from_file(argv[1]);
  g_object_ref_sink(widget);
  if (gtk_image_get_storage_type(GTK_IMAGE(widget)) != GTK_IMAGE_PIXBUF) return 3;
  GdkPixbuf *pixbuf = gtk_image_get_pixbuf(GTK_IMAGE(widget));
  int scale = gtk_widget_get_scale_factor(widget);
  if (!pixbuf || scale < 1 || gdk_pixbuf_get_width(pixbuf) < 2 * scale ||
      gdk_pixbuf_get_height(pixbuf) < scale) return 4;
  const guchar *pixels = gdk_pixbuf_get_pixels(pixbuf);
  int channels = gdk_pixbuf_get_n_channels(pixbuf);
  printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         gdk_pixbuf_get_width(pixbuf) / scale, gdk_pixbuf_get_height(pixbuf) / scale,
         pixels[0], pixels[1], pixels[2],
         pixels[channels * scale], pixels[channels * scale + 1], pixels[channels * scale + 2]);
  g_object_unref(widget);
  return 0;
}
