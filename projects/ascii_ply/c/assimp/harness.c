#include "harness.h"

#include <assimp/cimport.h>
#include <assimp/scene.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    const struct aiScene *scene = aiImportFileFromMemory(
        (const char *)data, (unsigned)size, 0, "ply");
    if (!scene) return 0;
    int okay = 0;
    if (scene->mNumMeshes > 0 && scene->mMeshes && scene->mMeshes[0]) {
        const struct aiMesh *mesh = scene->mMeshes[0];
        if (mesh->mNumFaces > 0 && mesh->mFaces &&
            mesh->mFaces[0].mNumIndices >= 3 && mesh->mFaces[0].mIndices) {
            result->meshes = scene->mNumMeshes;
            result->vertices = mesh->mNumVertices;
            result->faces = mesh->mNumFaces;
            for (int i = 0; i < 3; ++i)
                result->face[i] = mesh->mFaces[0].mIndices[i];
            okay = 1;
        }
    }
    aiReleaseImport(scene);
    return okay;
}
