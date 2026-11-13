package org.parsarium;

import ca.eandb.jmist.framework.loader.ply.ElementDescriptor;
import ca.eandb.jmist.framework.loader.ply.ElementListener;
import ca.eandb.jmist.framework.loader.ply.PlyReader;
import ca.eandb.jmist.framework.loader.ply.PlyTarget;
import java.io.File;

public final class JmistPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected a local ASCII PLY file path");
        }
        final int[] counts = new int[2];
        final int[] indices = new int[3];
        final double[] secondX = new double[1];
        PlyTarget target = new PlyTarget() {
            public ElementListener beginSection(ElementDescriptor descriptor) {
                if (descriptor.getName().equals("vertex")) {
                    return element -> {
                        if (counts[0] == 1) {
                            secondX[0] = element.getProperty("x").getDoubleValue();
                        }
                        counts[0]++;
                    };
                }
                if (descriptor.getName().equals("face")) {
                    return element -> {
                        var property = element.getProperty("vertex_indices");
                        for (int i = 0; i < 3; i++) {
                            indices[i] = property.getIntValue(i);
                        }
                        counts[1]++;
                    };
                }
                return null;
            }
            public void endSection() {}
        };
        new PlyReader().read(new File(args[0]), target);
        System.out.printf("{\"vertices\":%d,\"faces\":%d,\"second_x\":%.1f,\"indices\":[%d,%d,%d]}%n",
                counts[0], counts[1], secondX[0], indices[0], indices[1], indices[2]);
    }
}
