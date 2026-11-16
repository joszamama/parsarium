package org.parsarium;

import org.im4java.core.Info;

/** Parse local ASCII PPM through im4java's ImageMagick identify wrapper. */
public final class Im4javaPnmAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: Im4javaPnmAdapter control.ppm");
        var info = new Info(args[0], true);
        System.out.printf("{\"format\":\"%s\",\"width\":%d,\"height\":%d}%n",
            info.getImageFormat(), info.getImageWidth(), info.getImageHeight());
    }
}
