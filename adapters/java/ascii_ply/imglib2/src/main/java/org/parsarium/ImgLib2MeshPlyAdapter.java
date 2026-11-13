package org.parsarium;

import net.imglib2.mesh.io.ply.PLYMeshIO;

public final class ImgLib2MeshPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        var mesh = PLYMeshIO.open(args[0]);
        System.out.printf("{\"vertices\":%d,\"faces\":%d}%n",
                mesh.vertices().size(), mesh.triangles().size());
    }
}
