package org.parsarium;

import com.github.stephengold.wrench.LwjglAssetKey;
import com.github.stephengold.wrench.LwjglAssetLoader;
import com.jme3.asset.DesktopAssetManager;
import com.jme3.asset.plugins.FileLocator;
import com.jme3.scene.Geometry;
import com.jme3.scene.Mesh;
import com.jme3.scene.Node;
import com.jme3.scene.Spatial;
import java.nio.file.Path;

public final class MonkeyWrenchPlyAdapter {
    private MonkeyWrenchPlyAdapter() {}

    private static Geometry firstGeometry(Spatial spatial) {
        if (spatial instanceof Geometry) return (Geometry) spatial;
        if (spatial instanceof Node) {
            for (Spatial child : ((Node) spatial).getChildren()) {
                Geometry found = firstGeometry(child);
                if (found != null) return found;
            }
        }
        return null;
    }

    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("Expected local ASCII PLY path");
        Path path = Path.of(args[0]).toAbsolutePath();
        DesktopAssetManager manager = new DesktopAssetManager(true);
        manager.registerLocator(path.getParent().toString(), FileLocator.class);
        manager.registerLoader(LwjglAssetLoader.class, "ply");
        Spatial model = manager.loadModel(new LwjglAssetKey(path.getFileName().toString()));
        Geometry geometry = firstGeometry(model);
        if (geometry == null) throw new IllegalStateException("No parsed mesh geometry");
        Mesh mesh = geometry.getMesh();
        int[] indices = new int[3];
        mesh.getTriangle(0, indices);
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                mesh.getVertexCount(), mesh.getTriangleCount(), indices[0], indices[1], indices[2]);
    }
}
