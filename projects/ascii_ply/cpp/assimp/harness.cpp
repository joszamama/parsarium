#include "harness.h"

#include <assimp/Importer.hpp>
#include <assimp/scene.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    Assimp::Importer importer;
    const aiScene *scene = importer.ReadFileFromMemory(data, size, 0, "ply");
    if (!scene || scene->mNumMeshes == 0 || !scene->mMeshes || !scene->mMeshes[0])
        return false;
    const aiMesh *mesh = scene->mMeshes[0];
    if (mesh->mNumFaces == 0 || !mesh->mFaces ||
        mesh->mFaces[0].mNumIndices < 3 || !mesh->mFaces[0].mIndices)
        return false;
    result->meshes = scene->mNumMeshes;
    result->vertices = mesh->mNumVertices;
    result->faces = mesh->mNumFaces;
    for (int i = 0; i < 3; ++i)
        result->face[i] = mesh->mFaces[0].mIndices[i];
    return true;
}
