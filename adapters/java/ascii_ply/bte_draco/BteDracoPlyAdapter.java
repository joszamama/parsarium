package org.parsarium;

import com.mndk.bteterrarenderer.datatype.DataType;
import com.mndk.bteterrarenderer.draco.core.DecoderBuffer;
import com.mndk.bteterrarenderer.draco.core.Status;
import com.mndk.bteterrarenderer.draco.io.PlyElement;
import com.mndk.bteterrarenderer.draco.io.PlyPropertyReader;
import com.mndk.bteterrarenderer.draco.io.PlyReader;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;

/** Reads a local ASCII PLY control using BTETerraRenderer's public Draco module. */
public class BteDracoPlyAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Expected one local PLY path");
        }
        DecoderBuffer buffer = new DecoderBuffer();
        try (InputStream stream = Files.newInputStream(Paths.get(args[0]))) {
            buffer.init(stream);
        }
        PlyReader reader = new PlyReader();
        Status status = reader.read(buffer);
        if (status.isError()) {
            throw new IllegalStateException(status.toString());
        }
        PlyElement vertices = reader.getElementByName("vertex");
        PlyElement faces = reader.getElementByName("face");
        PlyPropertyReader<Float> x = new PlyPropertyReader<>(
                DataType.float32(), vertices.getPropertyByName("x"));
        System.out.println("{\"vertices\":" + vertices.getNumEntries()
                + ",\"faces\":" + faces.getNumEntries()
                + ",\"second_x\":" + x.readValue(1) + "}");
    }
}
