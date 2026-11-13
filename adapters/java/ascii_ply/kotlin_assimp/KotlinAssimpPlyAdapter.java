package org.parsarium;

import assimp.AiMesh;
import assimp.AiScene;
import assimp.Importer;
import java.io.File;
import java.util.List;

/** Read the supplied local ASCII PLY through the released JVM Assimp port. */
public final class KotlinAssimpPlyAdapter {
    private KotlinAssimpPlyAdapter() {}

    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected local PLY path");
        AiScene scene = new Importer().readFile(new File(args[0]).toURI(), 0);
        if (scene == null || scene.getNumMeshes() != 1) {
            throw new IllegalStateException("Expected one parsed mesh");
        }
        AiMesh mesh = scene.getMeshes().get(0);
        if (mesh.getNumFaces() != 1) throw new IllegalStateException("Expected one face");
        List<Integer> indices = mesh.getFaces().get(0);
        if (indices.size() != 3) throw new IllegalStateException("Expected a triangle");
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                mesh.getNumVertices(), mesh.getNumFaces(),
                indices.get(0), indices.get(1), indices.get(2));
    }
}
