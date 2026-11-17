package org.parsarium;

import app.f3d.F3D.Engine;
import app.f3d.F3D.Types;

public final class F3DPlyAdapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("expected local PLY path");
        Engine.autoloadPlugins();
        try (Engine engine = Engine.createNone()) {
            engine.getScene().add(args[0]);
            Types.SceneInfo info = engine.getScene().getSceneInfo();
            System.out.printf("{\"files\":%d,\"actors\":%d,\"points\":%d,\"cells\":%d}%n",
                    info.numberOfFiles, info.numberOfActors, info.numberOfPoints, info.numberOfCells);
        }
    }
}
