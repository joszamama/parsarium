#include <assimp/cimport.h>
#include <assimp/scene.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  const struct aiScene *scene = aiImportFile(argv[1], 0);
  if (!scene || scene->mNumMeshes != 1) return 1;
  const struct aiMesh *mesh = scene->mMeshes[0];
  if (mesh->mNumFaces != 1 || mesh->mFaces[0].mNumIndices != 3) return 1;
  printf("{\"meshes\":%u,\"vertices\":%u,\"faces\":%u,\"face\":[%u,%u,%u]}\n",
         scene->mNumMeshes, mesh->mNumVertices, mesh->mNumFaces,
         mesh->mFaces[0].mIndices[0], mesh->mFaces[0].mIndices[1],
         mesh->mFaces[0].mIndices[2]);
  aiReleaseImport(scene);
  return 0;
}
