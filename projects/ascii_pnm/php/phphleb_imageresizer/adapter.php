<?php
declare(strict_types=1);

[$script, $package, $path] = $argv + [null, null, null];
if ($package === null || $path === null) {
    throw new InvalidArgumentException('usage: php parse.php PACKAGE CONTROL');
}

if ($package === 'pecl/imagick') {
    // This extension is built separately from its pinned PECL source archive.
} elseif ($package === 'osiemsiedem/intervention-image-vips-driver') {
    require __DIR__ . '/vendor/autoload.php';
} elseif (in_array($package, ['calcinai/php-imagick', 'orbitale/imagemagick-php', 'phpthumb/phpthumb'], true)) {
    require __DIR__ . '/vendor/autoload.php';
} elseif (in_array($package, ['league/glide', 'phpixie/image', 'francodacosta/phmagick'], true)) {
    require __DIR__ . '/vendor/autoload.php';
} elseif (in_array($package, ['php-ffmpeg/php-ffmpeg', 'phphleb/imageresizer'], true)) {
    require __DIR__ . '/vendor/autoload.php';
} elseif (in_array($package, ['tpmanc/yii2-imagick', 'horde/image'], true)) {
    require __DIR__ . '/vendor/autoload.php';
} elseif ($package === 'intervention/image-laravel') {
    require __DIR__ . '/vendor/autoload.php';
} elseif ($package === 'locomotivemtl/charcoal-image') {
    require __DIR__ . '/vendor/autoload.php';
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
    case 'imagine/imagine':
        $image = (new \Imagine\Imagick\Imagine())->open($path);
        $size = $image->getSize();
        $output = ['width' => $size->getWidth(), 'height' => $size->getHeight()];
        break;
    case 'pecl/imagick':
        $image = new \Imagick();
        $image->readImage($path);
        $left = $image->getImagePixelColor(0, 0)->getColor();
        $right = $image->getImagePixelColor(1, 0)->getColor();
        $output = [
            'width' => $image->getImageWidth(),
            'height' => $image->getImageHeight(),
            'left_rgb' => [$left['r'], $left['g'], $left['b']],
            'right_rgb' => [$right['r'], $right['g'], $right['b']],
        ];
        break;
    case 'phpthumb/phpthumb':
        $image = new \PHPThumb\Imagick($path);
        $size = $image->getCurrentDimensions();
        $output = ['width' => $size['width'], 'height' => $size['height']];
        break;
    case 'orbitale/imagemagick-php':
        $response = (new \Orbitale\Component\ImageMagick\Command())->identify($path)->run();
        if ($response->hasFailed() || !preg_match('/\s(PPM)\s(\d+)x(\d+)\s/', $response->getOutput(), $matches)) {
            throw new RuntimeException('ImageMagick did not identify the control as PPM');
        }
        $output = ['width' => (int) $matches[2], 'height' => (int) $matches[3], 'format' => $matches[1]];
        break;
    case 'calcinai/php-imagick':
        $image = new \Imagick($path);
        $blob = $image->getImageBlob();
        if (!preg_match('/\AP6\s+(\d+)\s+(\d+)\s+(\d+)\s/s', $blob, $matches, PREG_OFFSET_CAPTURE)) {
            throw new RuntimeException('ImageMagick did not decode the P3 control to P6');
        }
        $pixels = substr($blob, $matches[0][1] + strlen($matches[0][0]));
        $output = [
            'width' => (int) $matches[1][0],
            'height' => (int) $matches[2][0],
            'maxval' => (int) $matches[3][0],
            'left_rgb' => array_values(unpack('C3', substr($pixels, 0, 3))),
            'right_rgb' => array_values(unpack('C3', substr($pixels, 3, 3))),
        ];
        break;
    case 'phpixie/image':
        $image = (new \PHPixie\Image())->read($path, 'imagick');
        $output = ['width' => $image->width(), 'height' => $image->height()];
        break;
    case 'league/glide':
        $cache = __DIR__ . '/image_pipeline/cache';
        if (!is_dir($cache) && !mkdir($cache, 0777, true) && !is_dir($cache)) {
            throw new RuntimeException('Unable to create Glide cache');
        }
        $server = \League\Glide\ServerFactory::create([
            'source' => dirname($path), 'cache' => $cache, 'driver' => 'imagick',
        ]);
        $server->deleteCache(basename($path));
        $cached = $server->makeImage(basename($path), ['fm' => 'png']);
        $info = getimagesize($cache . '/' . $cached);
        if ($info === false || $info['mime'] !== 'image/png') {
            throw new RuntimeException('Glide did not convert the PNM control to PNG');
        }
        $output = ['width' => $info[0], 'height' => $info[1], 'mime' => $info['mime']];
        break;
    case 'francodacosta/phmagick':
        $base = tempnam(sys_get_temp_dir(), 'parsarium-pnm-');
        if ($base === false) {
            throw new RuntimeException('Unable to create temporary output path');
        }
        unlink($base);
        $destination = $base . '.png';
        try {
            (new \phMagick\Core\Runner())->run(new \phMagick\Action\Convert($path, $destination));
            $info = getimagesize($destination);
            if ($info === false || $info['mime'] !== 'image/png') {
                throw new RuntimeException('phMagick did not convert the PNM control to PNG');
            }
            $output = ['width' => $info[0], 'height' => $info[1], 'mime' => $info['mime']];
        } finally {
            @unlink($destination);
        }
        break;
    case 'php-ffmpeg/php-ffmpeg':
        $stream = \FFMpeg\FFProbe::create()->streams($path)->videos()->first();
        if ($stream === null) {
            throw new RuntimeException('FFprobe did not find a PNM video stream');
        }
        $output = [
            'codec' => $stream->get('codec_name'),
            'width' => $stream->get('width'),
            'height' => $stream->get('height'),
        ];
        break;
    case 'phphleb/imageresizer':
        $image = new \Phphleb\Imageresizer\SimpleImage();
        if (!$image->load($path) || !($image->getImagick() instanceof \Imagick)) {
            throw new RuntimeException('Imagick processor did not decode the PNM control');
        }
        $output = ['width' => $image->getWidth(), 'height' => $image->getHeight()];
        break;
    case 'tpmanc/yii2-imagick':
        $image = \tpmanc\imagick\Imagick::open($path);
        $output = ['width' => $image->getWidth(), 'height' => $image->getHeight()];
        break;
    case 'horde/image':
        $image = (new \Horde\Image\Driver\ImagickDriver())->loadFile($path);
        $size = $image->size();
        $output = ['width' => (int) $size->width, 'height' => (int) $size->height];
        break;
    case 'intervention/image-laravel':
        // The provider expects Laravel's global config() helper; this adapter supplies
        // the same lookup through the pinned Illuminate Config repository.
        function config($key, $default = null) {
            return \Illuminate\Container\Container::getInstance()->make('config')->get($key, $default);
        }
        $app = new \Illuminate\Container\Container();
        \Illuminate\Container\Container::setInstance($app);
        \Illuminate\Support\Facades\Facade::setFacadeApplication($app);
        $app->instance('config', new \Illuminate\Config\Repository([
            'intervention-image' => ['driver' => \Intervention\Image\Drivers\Imagick\Driver::class],
        ]));
        (new \Intervention\Image\Laravel\ServiceProvider($app))->register();
        $image = \Intervention\Image\Laravel\Facades\Image::decodePath($path);
        $output = ['width' => $image->width(), 'height' => $image->height()];
        break;
    case 'locomotivemtl/charcoal-image':
        $image = (new \Charcoal\Image\Imagick\ImagickImage())->open($path);
        $output = ['width' => $image->width(), 'height' => $image->height()];
        break;
    default:
        throw new InvalidArgumentException('unknown ASCII PNM package: ' . $package);
}

echo json_encode($output, JSON_THROW_ON_ERROR), "\n";
