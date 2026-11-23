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
        // Import failures are parser rejections, with Assimp's own error string.
        if (scene == null) throw new IOException(Assimp.aiGetErrorString());
        try {
            // The first mesh and all indices of its first face (Assimp keeps polygons
            // without aiProcess_Triangulate); a scene without meshes or faces has none.
            int vertices = 0, faces = 0;
            StringBuilder indices = new StringBuilder();
            if (scene.mNumMeshes() > 0) {
                AIMesh mesh = AIMesh.create(scene.mMeshes().get(0));
                vertices = mesh.mNumVertices();
                faces = mesh.mNumFaces();
                if (faces > 0) {
                    AIFace face = mesh.mFaces().get(0);
                    for (int i = 0; i < face.mNumIndices(); i++) {
                        if (i > 0) indices.append(',');
                        indices.append(face.mIndices().get(i));
                    }
                }
            }
            System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%s]}%n",
                    vertices, faces, indices);
        } finally {
            Assimp.aiReleaseImport(scene);
        }
    }
}
