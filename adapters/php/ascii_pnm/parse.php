<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

if ($package === 'osiemsiedem/intervention-image-vips-driver') {
    require __DIR__ . '/legacy/vendor/autoload.php';
} else {
    require __DIR__ . '/vendor/autoload.php';
}

switch ($package) {
    case 'jcupitt/vips':
        $image = \Jcupitt\Vips\Image::newFromFile($path);
        $output = [
            'width' => $image->width,
            'height' => $image->height,
            'left_rgb' => array_map('intval', $image->getpoint(0, 0)),
            'right_rgb' => array_map('intval', $image->getpoint(1, 0)),
        ];
        break;
    case 'spatie/image':
        $image = \Spatie\Image\Image::useImageDriver(\Spatie\Image\Enums\ImageDriver::Vips)
            ->loadFile($path);
        $output = ['width' => $image->getWidth(), 'height' => $image->getHeight()];
        break;
    case 'rokka/imagine-vips':
        $image = (new \Imagine\Vips\Imagine())->open($path);
        $size = $image->getSize();
        $output = ['width' => $size->getWidth(), 'height' => $size->getHeight()];
        break;
    case 'intervention/image':
        $manager = new \Intervention\Image\ImageManager(new \Intervention\Image\Drivers\Vips\Driver());
        $image = $manager->decodePath($path);
        $output = ['width' => $image->width(), 'height' => $image->height()];
        break;
    case 'intervention/image-driver-vips':
        $image = (new \Intervention\Image\Drivers\Vips\Driver())->decodeImage($path);
        $output = ['width' => $image->width(), 'height' => $image->height()];
        break;
    case 'osiemsiedem/intervention-image-vips-driver':
        $image = (new \Intervention\Image\Vips\Decoder())->initFromPath($path);
        $output = ['width' => $image->width(), 'height' => $image->height()];
        break;
    default:
        throw new InvalidArgumentException('unknown ASCII PNM package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
