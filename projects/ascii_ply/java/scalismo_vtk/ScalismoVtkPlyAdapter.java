package org.parsarium;

import java.io.File;
import java.io.IOException;
import scalismo.geometry._3D;
import scalismo.mesh.TriangleCell;
import scalismo.mesh.TriangleMesh;
import scala.util.Try;

public final class ScalismoVtkPlyAdapter {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        // Documented scalismo.vtk.initialize(): load the VTK natives (no GC thread), then
        // scalismo.vtk.io.MeshIO.readMesh(File), which reads .ply through VTK's vtkPLYReader.
        scalismo.vtk.initialize.apply(false, 0L);
        Try<TriangleMesh<_3D>> result = scalismo.vtk.io.MeshIO.readMesh(new File(args[0]));
        if (result.isFailure()) {
            // readMesh reports a read error as a Failure; its exception is the reason.
            Throwable failure = result.failed().get();
            throw new IOException(failure.toString(), failure);
        }
        TriangleMesh<_3D> mesh = result.get();
        int triangles = mesh.triangulation().triangles().size();
        String indices = "";
        if (triangles > 0) {
            TriangleCell cell = mesh.triangulation().triangles().apply(0);
            indices = cell.ptId1() + "," + cell.ptId2() + "," + cell.ptId3();
        }
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%s]}%n",
                mesh.pointSet().numberOfPoints(), triangles, indices);
    }
}
