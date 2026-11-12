#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef __cplusplus
extern "C"
#endif
int sqlite3_zipfile_init(sqlite3 *, char **, const sqlite3_api_routines *);

static void json_string(const unsigned char *bytes, size_t length) {
    putchar('"');
    for (size_t i = 0; i < length; ++i) {
        unsigned char ch = bytes[i];
        if (ch == '"' || ch == '\\') { putchar('\\'); putchar(ch); }
        else if (ch == '\n') fputs("\\n", stdout);
        else if (ch == '\r') fputs("\\r", stdout);
        else if (ch == '\t') fputs("\\t", stdout);
        else if (ch < 0x20) printf("\\u%04x", ch);
        else putchar(ch);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    sqlite3 *db = NULL;
    sqlite3_stmt *query = NULL;
    if (sqlite3_open(":memory:", &db) != SQLITE_OK ||
        sqlite3_zipfile_init(db, NULL, NULL) != SQLITE_OK ||
        sqlite3_prepare_v2(db, "SELECT name,data FROM zipfile(?1)", -1,
                           &query, NULL) != SQLITE_OK ||
        sqlite3_bind_text(query, 1, argv[1], -1, SQLITE_STATIC) != SQLITE_OK) {
        if (query) sqlite3_finalize(query);
        if (db) sqlite3_close(db);
        return 3;
    }
    unsigned int entries = 0;
    char *first_name = NULL;
    unsigned char *first_content = NULL;
    int first_size = 0;
    int step;
    while ((step = sqlite3_step(query)) == SQLITE_ROW) {
        ++entries;
        if (entries != 1) continue;
        const unsigned char *name = sqlite3_column_text(query, 0);
        const unsigned char *content =
            (const unsigned char *)sqlite3_column_blob(query, 1);
        first_size = sqlite3_column_bytes(query, 1);
        if (!name || first_size < 0 || (first_size && !content)) break;
        size_t name_size = strlen((const char *)name);
        first_name = (char *)malloc(name_size + 1);
        first_content = (unsigned char *)malloc((size_t)first_size + 1);
        if (!first_name || !first_content) break;
        memcpy(first_name, name, name_size + 1);
        if (first_size) memcpy(first_content, content, (size_t)first_size);
    }
    if (step != SQLITE_DONE || !first_name || !first_content) {
        free(first_name);
        free(first_content);
        sqlite3_finalize(query);
        sqlite3_close(db);
        return 4;
    }
    printf("{\"entries\":%u,\"name\":", entries);
    json_string((const unsigned char *)first_name, strlen(first_name));
    fputs(",\"content\":", stdout);
    json_string(first_content, (size_t)first_size);
    puts("}");
    free(first_name);
    free(first_content);
    sqlite3_finalize(query);
    sqlite3_close(db);
    return 0;
}
