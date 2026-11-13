package org.parsarium;

import com.github.dabasan.jassimp.AiMesh;
import com.github.dabasan.jassimp.AiScene;
import com.github.dabasan.jassimp.Jassimp;

public final class JassimpPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) System.exit(2);
        AiScene scene = Jassimp.importFile(args[0]);
        if (scene == null || scene.getNumMeshes() != 1) System.exit(1);
        AiMesh mesh = scene.getMeshes().get(0);
        System.out.printf("{\"meshes\":%d,\"vertices\":%d,\"faces\":%d}%n",
                scene.getNumMeshes(), mesh.getNumVertices(), mesh.getNumFaces());
    }
}
