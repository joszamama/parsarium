#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  Assimp::Importer importer;
  const aiScene *scene = importer.ReadFile(argv[1], 0);
  if (!scene || scene->mNumMeshes != 1) return 1;
  const aiMesh *mesh = scene->mMeshes[0];
  if (mesh->mNumFaces != 1 || mesh->mFaces[0].mNumIndices != 3) return 1;
  std::printf("{\"meshes\":%u,\"vertices\":%u,\"faces\":%u,\"face\":[%u,%u,%u]}\n",
              scene->mNumMeshes, mesh->mNumVertices, mesh->mNumFaces,
              mesh->mFaces[0].mIndices[0], mesh->mFaces[0].mIndices[1],
              mesh->mFaces[0].mIndices[2]);
  return 0;
}
