import org.lwjgl.assimp.AIFace;
import org.lwjgl.assimp.AIMesh;
import org.lwjgl.assimp.AIScene;

// Struct layout LWJGL 3.4.3 computes for the same fields as abi_layout.c.
public final class AbiLayout {
    public static void main(String[] args) {
        System.out.printf("{\"aiScene.SIZEOF\":%d,\"aiScene.mFlags\":%d,\"aiScene.mNumMeshes\":%d,"
                + "\"aiScene.mMeshes\":%d,\"aiScene.mMetaData\":%d,\"aiScene.mName\":%d,"
                + "\"aiScene.mNumSkeletons\":%d,\"aiScene.mSkeletons\":%d,\"aiScene.mPrivate\":%d,"
                + "\"aiMesh.SIZEOF\":%d,\"aiMesh.mPrimitiveTypes\":%d,\"aiMesh.mNumVertices\":%d,"
                + "\"aiMesh.mNumFaces\":%d,\"aiMesh.mVertices\":%d,\"aiMesh.mFaces\":%d,"
                + "\"aiMesh.mName\":%d,\"aiMesh.mAABB\":%d,\"aiMesh.mTextureCoordsNames\":%d,"
                + "\"aiFace.SIZEOF\":%d,\"aiFace.mNumIndices\":%d,\"aiFace.mIndices\":%d}%n",
                AIScene.SIZEOF, AIScene.MFLAGS, AIScene.MNUMMESHES, AIScene.MMESHES,
                AIScene.MMETADATA, AIScene.MNAME, AIScene.MNUMSKELETONS, AIScene.MSKELETONS,
                AIScene.MPRIVATE, AIMesh.SIZEOF, AIMesh.MPRIMITIVETYPES, AIMesh.MNUMVERTICES,
                AIMesh.MNUMFACES, AIMesh.MVERTICES, AIMesh.MFACES, AIMesh.MNAME, AIMesh.MAABB,
                AIMesh.MTEXTURECOORDSNAMES, AIFace.SIZEOF, AIFace.MNUMINDICES, AIFace.MINDICES);
    }
}
