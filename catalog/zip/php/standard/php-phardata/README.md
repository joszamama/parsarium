# php-phardata — ZIP / PHP

- **Runtime:** PHP 8.5.12 CLI with zip extension 1.22.8 (libzip 1.12.1) and Phar extension
- **Input API:** `PharData(local ZIP path); Countable; iteration over PharFileInfo; getContent`
- **Official documentation:** [reference](https://www.php.net/manual/en/class.phardata.php)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/php/zip/standard.json) · [saved result](../../../../../data/php/zip/verification.json)

**Parser family:** PHP Phar ZIP archive reader

## Observed control result

```json
{
  "entries": 1,
  "name": "hello.txt",
  "content": "parsarium\n"
}
```

[Control adapter](../../../../../adapters/php/zip/runtime_phardata.php)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
