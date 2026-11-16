package org.parsarium;

import java.nio.file.Path;
import io.brunoborges.jairosvg.JairoSVG;

public final class JairoSvgAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: local.svg");
        var image = JairoSVG.builder().fromFile(Path.of(args[0])).toImage();
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
            image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
    }
}
