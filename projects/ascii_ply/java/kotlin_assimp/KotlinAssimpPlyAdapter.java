package org.parsarium;

import assimp.AiMesh;
import assimp.AiScene;
import assimp.Importer;
import java.io.File;
import java.util.List;
import java.util.stream.Collectors;

/** Read the supplied local ASCII PLY through the released JVM Assimp port. */
public final class KotlinAssimpPlyAdapter {
    private KotlinAssimpPlyAdapter() {}

    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected local PLY path");
        AiScene scene = new Importer().readFile(new File(args[0]).toURI(), 0);
        if (scene == null || scene.getNumMeshes() < 1) {
            // Importer.readFile returns null when the importer rejects the file.
            System.out.println("{\"rejected\":\"no mesh\"}");
            return;
        }
        AiMesh mesh = scene.getMeshes().get(0);
        List<Integer> indices = mesh.getNumFaces() > 0 ? mesh.getFaces().get(0) : List.of();
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%s]}%n",
                mesh.getNumVertices(), mesh.getNumFaces(),
                indices.stream().map(String::valueOf).collect(Collectors.joining(",")));
    }
}
