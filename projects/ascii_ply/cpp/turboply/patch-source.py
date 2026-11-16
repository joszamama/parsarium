from hashlib import sha256
from pathlib import Path

stream = Path('/work/source/plystream.cpp')
original = stream.read_bytes()
assert sha256(original).hexdigest() == '941241d93d5ac320283cdc4a585f1f1fe2b2a265276fd965ba68e3da4ee59a87'
text = stream.read_text()
start = text.index('class FormatHandler {')
block_start = text.index('protected:\n    template <typename F, typename StreamT>', start)
block_end = text.index('\n};', block_start)
block = text[block_start:block_end]
text = text[:block_start] + text[block_end:]
text = text[:start] + text[start:].replace('class FormatHandler {',
    'class FormatHandler {\n' + block + '\npublic:', 1)
stream.write_text(text)
assert sha256(stream.read_bytes()).hexdigest() == 'c25ab410e16cc99fbc0e83fce2ca117a736e185c9d80e79e5123e1b86052d944'
