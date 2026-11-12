package org.parsarium;

import java.io.File;
import ij_plugins.imageio.IJImageIO;

/** Parse local P3 PPM through IJ Plugins ImageIO and JAI PNM provider. */
public final class IjpPnmAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: IjpPnmAdapter control.ppm");
        var images = IJImageIO.read(new File(args[0]));
        if (images.length != 1) throw new IllegalStateException("expected one PPM image");
        var image = images[0].getBufferedImage();
        System.out.printf("{\"width\":%d,\"height\":%d,\"pixels\":\"%08x,%08x\"}%n",
            image.getWidth(), image.getHeight(), image.getRGB(0, 0), image.getRGB(1, 0));
    }
}
