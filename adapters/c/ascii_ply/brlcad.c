#include "common.h"
#include "gcv/api.h"
#include <unistd.h>
/* BRL-CAD's POSIX stub collides with Darwin's unrelated setmode(3). */
#define setmode brlcad_setmode
#include "raytrace.h"
#undef setmode

#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  const char *base = strrchr(argv[1], '/');
  base = base ? base + 1 : argv[1];
  const char *suffix = strrchr(base, '.');
  if (!suffix || strcmp(suffix, ".ply")) return 2;
  size_t stem_length = (size_t)(suffix - base);
  if (stem_length + sizeof(".bot") > 256) return 2;
  char object_name[256];
  memcpy(object_name, base, stem_length);
  memcpy(object_name + stem_length, ".bot", sizeof(".bot"));

  struct gcv_context context;
  gcv_context_init(&context);
  const struct gcv_filter *reader =
      find_filter(GCV_FILTER_READ, BU_MIME_MODEL_PLY, argv[1], &context);
  if (!reader) {
    fputs("BRL-CAD PLY reader not registered\n", stderr);
    gcv_context_destroy(&context);
    return 1;
  }
  struct gcv_opts options;
  gcv_opts_default(&options);
  options.scale_factor = 1.0;
  if (!gcv_execute(&context, reader, &options, 0, NULL, argv[1])) {
    fputs("BRL-CAD PLY reader failed\n", stderr);
    gcv_context_destroy(&context);
    return 1;
  }

  struct directory *entry = db_lookup(context.dbip, object_name, LOOKUP_QUIET);
  if (!entry) {
    fputs("parsed BOT object missing\n", stderr);
    gcv_context_destroy(&context);
    return 1;
  }
  struct rt_db_internal internal;
  RT_DB_INTERNAL_INIT(&internal);
  if (rt_db_get_internal(&internal, entry, context.dbip, NULL) < 0 ||
      internal.idb_minor_type != ID_BOT) {
    fputs("parsed BOT object unavailable\n", stderr);
    gcv_context_destroy(&context);
    return 1;
  }
  const struct rt_bot_internal *bot = (const struct rt_bot_internal *)internal.idb_ptr;
  if (bot->num_vertices != 3 || bot->num_faces != 1) {
    fputs("unexpected parsed mesh size\n", stderr);
    rt_db_free_internal(&internal);
    gcv_context_destroy(&context);
    return 1;
  }
  printf("{\"vertices\":%zu,\"faces\":%zu,\"second_x\":%.1f,\"face\":[%d,%d,%d]}\n",
         bot->num_vertices, bot->num_faces, bot->vertices[3],
         bot->faces[0], bot->faces[1], bot->faces[2]);
  rt_db_free_internal(&internal);
  gcv_context_destroy(&context);
  return 0;
}
