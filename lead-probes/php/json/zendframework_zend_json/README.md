# zendframework/zend-json lead check — PHP / JSON

This is a reproducible **excluded lead probe**, not a Parsarium parser project. In the pinned 3.1.2 release, the default `Zend\Json\Json::decode(string)` calls PHP's `json_decode` and returns its result, so it shares the ext/json family already verified as `json/php/stdlib_json_decode`. The documented `Json::$useBuiltinEncoderDecoder = true` flag does run the package's own PHP lexer and parser in `Decoder.php`. That decoder is the predecessor of the laminas/laminas-json 3.8.0 `Decoder` already verified as `json/php/laminas_json`. After the `Zend\` → `Laminas\` rename, both files declare the same methods and differ only in coding-standard rewrites such as `switch` → `match`. Counting it would duplicate that family.

From the repository root:

```sh
python3 lead-probes/php/json/zendframework_zend_json/check.py
```

The command builds the pinned Docker image, which checks the zend-json source archive SHA-256 and diffs it against the Composer install. It unpacks the hash-pinned laminas-json 3.8.0 archive beside it, because Composer refuses to install both. It then decodes both valid controls through three routes under Xdebug:

- zend-json default
- zend-json opt-in
- laminas-json opt-in

It compares exact type-tagged trees with an independent Python `json` oracle. It fails if any of these does not hold:

- the default route runs anything beyond the `json_decode` delegation lines
- the opt-in route does not reach `Decoder::decode`
- the opt-in route runs different `Decoder` methods from laminas-json

It writes [the observation](../../../../data/php/json/zendframework-zend-json-lead-check.json). It does not run malformed inputs, a fuzz campaign or an AFL++ bridge. A bridge would duplicate the laminas-json decoder family, or instrument a `json_decode` wrapper.
