#include <stddef.h>
#include <stdio.h>
#include <assimp/scene.h>

/* Struct layout of the Assimp headers the instrumented library was compiled from. */
#define FIELD(type, member) printf(",\"" #type "." #member "\":%zu", offsetof(struct type, member))

int main(void) {
    printf("{\"aiScene.SIZEOF\":%zu", sizeof(struct aiScene));
    FIELD(aiScene, mFlags); FIELD(aiScene, mNumMeshes); FIELD(aiScene, mMeshes);
    FIELD(aiScene, mMetaData); FIELD(aiScene, mName); FIELD(aiScene, mNumSkeletons);
    FIELD(aiScene, mSkeletons); FIELD(aiScene, mPrivate);
    printf(",\"aiMesh.SIZEOF\":%zu", sizeof(struct aiMesh));
    FIELD(aiMesh, mPrimitiveTypes); FIELD(aiMesh, mNumVertices); FIELD(aiMesh, mNumFaces);
    FIELD(aiMesh, mVertices); FIELD(aiMesh, mFaces); FIELD(aiMesh, mName);
    FIELD(aiMesh, mAABB); FIELD(aiMesh, mTextureCoordsNames);
    printf(",\"aiFace.SIZEOF\":%zu", sizeof(struct aiFace));
    FIELD(aiFace, mNumIndices); FIELD(aiFace, mIndices);
    printf("}\n");
    return 0;
}
