package org.parsarium;

import java.io.IOException;
import java.nio.file.Path;
import org.lwjgl.assimp.AIFace;
import org.lwjgl.assimp.AIMesh;
import org.lwjgl.assimp.AIScene;
import org.lwjgl.assimp.Assimp;

public final class LwjglAssimpPlyAdapter {
    // /work/native holds the source-built, LLVM-instrumented Assimp; /work/native-stock holds
    // the unmodified natives-linux-arm64 libraries. Absolute names stop LWJGL from falling back
    // to a classpath or system copy, and the loaded path is checked after initialization.
    private static final String NATIVE_DIR =
            System.getenv().getOrDefault("PARSARIUM_LWJGL_NATIVE_DIR", "/work/native");

    static {
        System.setProperty("org.lwjgl.librarypath", NATIVE_DIR);
        System.setProperty("org.lwjgl.assimp.libname", NATIVE_DIR + "/libassimp.so");
        System.setProperty("org.lwjgl.assimp.draco.libname", NATIVE_DIR + "/libdraco.so");
        String loaded = Assimp.getLibrary().getPath();
        if (loaded == null || !Path.of(loaded).toAbsolutePath().normalize()
                .equals(Path.of(NATIVE_DIR, "libassimp.so"))) {
            throw new IllegalStateException("unexpected Assimp library: " + loaded);
        }
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        AIScene scene = Assimp.aiImportFile(args[0], 0);
        // Import failures and scenes without a triangle are parser rejections, not harness faults.
        if (scene == null) throw new IOException(Assimp.aiGetErrorString());
        try {
            if (scene.mNumMeshes() == 0) throw new IOException("no mesh");
            AIMesh mesh = AIMesh.create(scene.mMeshes().get(0));
            if (mesh.mNumFaces() == 0) throw new IOException("no face");
            AIFace face = mesh.mFaces().get(0);
            if (face.mNumIndices() < 3) throw new IOException("face has fewer than three indices");
            System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                    mesh.mNumVertices(), mesh.mNumFaces(), face.mIndices().get(0),
                    face.mIndices().get(1), face.mIndices().get(2));
        } finally {
            Assimp.aiReleaseImport(scene);
        }
    }
}
