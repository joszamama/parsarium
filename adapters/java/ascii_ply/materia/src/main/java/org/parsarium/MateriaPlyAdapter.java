package org.parsarium;

import io.materia.core.scene.Mesh;
import io.materia.loader.ModelAsset;
import io.materia.loader.PLYLoader;
import java.nio.file.Path;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.EmptyCoroutineContext;
import kotlin.jvm.functions.Function2;
import kotlinx.coroutines.BuildersKt;
import kotlinx.coroutines.CoroutineScope;

public final class MateriaPlyAdapter {
    private MateriaPlyAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("expected local PLY path");
        }
        final String path = Path.of(args[0]).toAbsolutePath().toString();
        ModelAsset asset = BuildersKt.runBlocking(EmptyCoroutineContext.INSTANCE,
                new Function2<CoroutineScope, Continuation<? super ModelAsset>, Object>() {
                    @Override
                    public Object invoke(CoroutineScope scope, Continuation<? super ModelAsset> continuation) {
                        return new PLYLoader().load(path, continuation);
                    }
                });
        Mesh mesh = (Mesh) asset.getScene().getChildren().get(0);
        var geometry = mesh.getGeometry();
        float[] parsedIndices = geometry.getIndex().getArray();
        if (parsedIndices.length != 3) {
            throw new IllegalStateException("expected one parsed triangle");
        }
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}%n",
                geometry.getAttribute("position").getCount(), geometry.getTriangleCount(),
                (int) parsedIndices[0], (int) parsedIndices[1], (int) parsedIndices[2]);
    }
}
