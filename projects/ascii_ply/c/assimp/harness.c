#include "harness.h"

#include <stdlib.h>

#include <assimp/cimport.h>
#include <assimp/scene.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    result->meshes = result->vertices = result->faces = result->face_count = 0;
    result->face = NULL;
    const struct aiScene *scene = aiImportFileFromMemory(
        (const char *)data, (unsigned)size, 0, "ply");
    if (!scene) return 0;
    int okay = 1;
    result->meshes = scene->mNumMeshes;
    if (scene->mNumMeshes > 0 && scene->mMeshes && scene->mMeshes[0]) {
        const struct aiMesh *mesh = scene->mMeshes[0];
        result->vertices = mesh->mNumVertices;
        result->faces = mesh->mNumFaces;
        /* Without aiProcess_Triangulate Assimp keeps polygons: report every
         * index of the first face, however many it has. */
        if (mesh->mNumFaces > 0 && mesh->mFaces && mesh->mFaces[0].mNumIndices > 0 &&
            mesh->mFaces[0].mIndices) {
            unsigned count = mesh->mFaces[0].mNumIndices;
            result->face = malloc((size_t)count * sizeof(unsigned));
            if (!result->face) {
                okay = 0;
            } else {
                for (unsigned i = 0; i < count; ++i)
                    result->face[i] = mesh->mFaces[0].mIndices[i];
                result->face_count = count;
            }
        }
    }
    aiReleaseImport(scene);
    return okay;
}

void parsarium_free_result(struct parsarium_ply_result *result) {
    if (!result) return;
    free(result->face);
    result->face = NULL;
    result->face_count = 0;
}

const char *parsarium_error(void) {
    const char *message = aiGetErrorString();
    return message && *message ? message : "aiImportFileFromMemory returned no scene";
}
