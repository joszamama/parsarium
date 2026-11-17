# Minimal ISO BMFF / MP4: ftyp + moov with one empty video track, plus
# optional free boxes before and after moov. Every box size is a 32-bit
# big-endian field that a constraint ties to the box's own byte length;
# Fandango repairs these fields directly, so all generated files have
# consistent sizes.

import struct

def u32(n):
    return struct.pack('>I', n)

<start> ::= <ftyp> <free>? <moov> <free>?

<size> ::= <byte>{4}

# File type box
<ftyp> ::= <size> b'ftyp' <brand> b'\x00\x00\x00\x00' <brand>{1,4}
<brand> ::= b'isom' | b'iso2' | b'mp41' | b'mp42' | b'avc1'

# Movie box
<moov> ::= <size> b'moov' <mvhd> <trak>
<mvhd> ::= <size> b'mvhd' b'\x00\x00\x00\x00' <time> <time> <timescale> <duration> b'\x00\x01\x00\x00' b'\x01\x00' b'\x00'{10} <matrix> b'\x00'{24} b'\x00\x00\x00\x02'
<trak> ::= <size> b'trak' <tkhd> <mdia>
<tkhd> ::= <size> b'tkhd' b'\x00\x00\x00\x03' <time> <time> b'\x00\x00\x00\x01' b'\x00\x00\x00\x00' <duration> b'\x00'{8} b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' <matrix> <dimension> <dimension>
<mdia> ::= <size> b'mdia' <mdhd> <hdlr> <minf>
<mdhd> ::= <size> b'mdhd' b'\x00\x00\x00\x00' <time> <time> <timescale> <duration> <language> b'\x00\x00'
<hdlr> ::= <size> b'hdlr' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'vide' b'\x00'{12} <handler_name>
<minf> ::= <size> b'minf' <vmhd> <dinf> <stbl>
<vmhd> ::= <size> b'vmhd' b'\x00\x00\x00\x01' b'\x00'{8}
<dinf> ::= <size> b'dinf' <dref>
<dref> ::= <size> b'dref' b'\x00\x00\x00\x00' b'\x00\x00\x00\x01' <url>
<url> ::= <size> b'url ' b'\x00\x00\x00\x01'
# Empty sample tables: a track with no samples is structurally valid.
<stbl> ::= <size> b'stbl' <stsd> <stts> <stsc> <stsz> <stco>
<stsd> ::= <size> b'stsd' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00'
<stts> ::= <size> b'stts' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00'
<stsc> ::= <size> b'stsc' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00'
<stsz> ::= <size> b'stsz' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00'
<stco> ::= <size> b'stco' b'\x00\x00\x00\x00' b'\x00\x00\x00\x00'

<free> ::= <size> b'free' <byte>{0,16}

# Field values
<time> ::= b'\x00\x00\x00\x00' | b'\xe0' <byte>{3}
<timescale> ::= b'\x00\x00\x02\x58' | b'\x00\x00\x03\xe8' | b'\x00\x00\x75\x30' | b'\x00\x01\x5f\x90'
<duration> ::= b'\x00\x00' <byte> <byte>
<matrix> ::= b'\x00\x01\x00\x00' b'\x00'{12} b'\x00\x01\x00\x00' b'\x00'{12} b'\x40\x00\x00\x00'
# 16.16 fixed point, integer part 1..255 (Exiv2 rejects zero dimensions)
<dimension> ::= b'\x00' rb'[\x01-\xff]' b'\x00\x00'
<language> ::= b'\x55\xc4' | b'\x15\xc7' | b'\x19\x4c'
<handler_name> ::= b'\x00' | b'VideoHandler\x00' | b'Parsarium\x00'

where <ftyp>.<size> == u32(len(bytes(<ftyp>)))
where <moov>.<size> == u32(len(bytes(<moov>)))
where <mvhd>.<size> == u32(len(bytes(<mvhd>)))
where <trak>.<size> == u32(len(bytes(<trak>)))
where <tkhd>.<size> == u32(len(bytes(<tkhd>)))
where <mdia>.<size> == u32(len(bytes(<mdia>)))
where <mdhd>.<size> == u32(len(bytes(<mdhd>)))
where <hdlr>.<size> == u32(len(bytes(<hdlr>)))
where <minf>.<size> == u32(len(bytes(<minf>)))
where <vmhd>.<size> == u32(len(bytes(<vmhd>)))
where <dinf>.<size> == u32(len(bytes(<dinf>)))
where <dref>.<size> == u32(len(bytes(<dref>)))
where <url>.<size> == u32(len(bytes(<url>)))
where <stbl>.<size> == u32(len(bytes(<stbl>)))
where <stsd>.<size> == u32(len(bytes(<stsd>)))
where <stts>.<size> == u32(len(bytes(<stts>)))
where <stsc>.<size> == u32(len(bytes(<stsc>)))
where <stsz>.<size> == u32(len(bytes(<stsz>)))
where <stco>.<size> == u32(len(bytes(<stco>)))
where <free>.<size> == u32(len(bytes(<free>)))
# Track duration is in the movie timescale, so it matches mvhd.
where <tkhd>.<duration> == bytes(<mvhd>.<duration>)
