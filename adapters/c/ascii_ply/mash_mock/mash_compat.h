/* Mash 0.2.0 aliases the data-loader type to MashData. Correct only that
 * type alias before compiling the unchanged tagged source. The mock Cogl
 * functions observe geometry after parsing; they do not parse any input. */
#define MASH_COMPILATION 1
#include <glib-object.h>
#include "mash-data-loader.h"
#undef MASH_TYPE_DATA_LOADER
#define MASH_TYPE_DATA_LOADER (mash_data_loader_get_type())
#include "mash-ply-loader.h"
