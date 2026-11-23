#include "harness.h"

#include <assimp/Importer.hpp>
#include <assimp/scene.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    Assimp::Importer importer;
    const aiScene *scene = importer.ReadFileFromMemory(data, size, 0, "ply");
    if (!scene) {
        result->error = importer.GetErrorString();
        if (result->error.empty()) result->error = "ReadFileFromMemory returned no scene";
        return false;
    }
    result->meshes = scene->mNumMeshes;
    result->vertices = result->faces = 0;
    result->face.clear();
    if (scene->mNumMeshes == 0 || !scene->mMeshes || !scene->mMeshes[0]) return true;
    const aiMesh *mesh = scene->mMeshes[0];
    result->vertices = mesh->mNumVertices;
    result->faces = mesh->mNumFaces;
    // Without aiProcess_Triangulate Assimp keeps polygons: report every index of
    // the first face, however many it has.
    if (mesh->mNumFaces > 0 && mesh->mFaces && mesh->mFaces[0].mIndices)
        result->face.assign(mesh->mFaces[0].mIndices,
                            mesh->mFaces[0].mIndices + mesh->mFaces[0].mNumIndices);
    return true;
}
