#include "harness.h"

#include <sqlite3.h>
#include <string.h>

#define PARSARIUM_MAX_INPUT (1u << 20)

int sqlite3_zipfile_init(sqlite3 *, char **, const sqlite3_api_routines *);

int parsarium_parse_zip(const uint8_t *data, size_t size,
                        struct parsarium_zip_result *result) {
    if (!data || !result || size == 0 || size > PARSARIUM_MAX_INPUT) return 0;
    memset(result, 0, sizeof(*result));
    sqlite3 *db = NULL;
    sqlite3_stmt *query = NULL;
    int ok = 0;
    if (sqlite3_open(":memory:", &db) != SQLITE_OK) goto done;
    if (sqlite3_zipfile_init(db, NULL, NULL) != SQLITE_OK) goto done;
    if (sqlite3_prepare_v2(db, "SELECT name,data FROM zipfile(?1)", -1,
                           &query, NULL) != SQLITE_OK) goto done;
    if (sqlite3_bind_blob(query, 1, data, (int)size, SQLITE_STATIC) != SQLITE_OK) goto done;
    int step;
    while ((step = sqlite3_step(query)) == SQLITE_ROW) {
        result->entries++;
        if (result->entries != 1) continue;
        const unsigned char *name = sqlite3_column_text(query, 0);
        int name_len = sqlite3_column_bytes(query, 0);
        const unsigned char *content = sqlite3_column_blob(query, 1);
        int content_len = sqlite3_column_bytes(query, 1);
        if (!name || name_len <= 0 || (size_t)name_len >= sizeof(result->name)
                || content_len < 0 || (size_t)content_len > sizeof(result->content)
                || (content_len && !content)) goto done;
        result->name_len = (size_t)name_len;
        memcpy(result->name, name, result->name_len);
        result->content_len = (size_t)content_len;
        if (content_len) memcpy(result->content, content, result->content_len);
    }
    ok = step == SQLITE_DONE && result->entries > 0 && result->name_len > 0;
done:
    if (query) sqlite3_finalize(query);
    if (db) sqlite3_close(db);
    return ok;
}

