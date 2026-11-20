# Tagged MP3: an ID3v2.3 or ID3v2.4 tag, an ID3v1 trailer, or both, around
# one MPEG-1 or MPEG-2 Layer III stream.
#
# Audio. Every frame of a file has the same MPEG version, sample rate,
# channel mode, mode extension, flags and protection (CRC) bit. A file is
# constant bitrate (every frame repeats the first frame's bitrate; only the
# padding bit may differ) or variable bitrate (each frame picks its own
# bitrate index). A file has 5 to 60 audio frames, optionally preceded by a
# Xing ("Xing" for VBR, "Info" for CBR) frame that carries the audio frame
# count and the stream byte count. Files with a Xing frame have no CRC, so
# the tag sits where readers look for it. The side information and main data
# are zeros: every granule has part2_3_length 0 and decodes to silence. Each
# frame's length follows from its header: 144000 * kbps / rate (MPEG-1) or
# 72000 * kbps / rate (MPEG-2), plus the padding bit. A protected frame's
# CRC-16 (poly 0x8005, init 0xFFFF) covers header bytes 3 and 4 and the side
# information. The derived bytes are where constraints that Fandango repairs.
#
# ID3v2. One tag of version 2.3 or 2.4, without unsynchronisation, extended
# header or footer, holding one to seven distinct frames in a fixed order:
# TIT2, TPE1, TALB, TYER (2.3) or TDRC (2.4), TRCK, TCON and COMM, each
# present in about half the files. Text is ISO-8859-1, UTF-16 with a BOM
# (little or big endian) or, in 2.4 only, UTF-8, with no terminator. Frame
# sizes are 32-bit (2.3) or synchsafe (2.4); the tag size is synchsafe and
# includes optional zero padding.
#
# ID3v1. An optional 128-byte trailer: title, artist and album (30 bytes
# each), a four-digit year, a 30-byte comment or a 28-byte comment with an
# ID3v1.1 track number, and a genre byte. Text fields are zero padded. The
# ID3v1 fields are drawn independently of the ID3v2 frames.

BITRATES = {3: (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
            2: (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)}
RATES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000)}
FRAMES = ('<frame0>', '<cbr>', '<vbr>')

def crc16(data):
    crc = 0xffff
    for value in data:
        crc ^= value << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x8005) if crc & 0x8000 else crc << 1
            crc &= 0xffff
    return crc

def header(hdr):
    data = bytes(hdr)
    return data[1], data[2], data[3]

def frame_length(b1, b2):
    version = (b1 >> 3) & 3
    rate = RATES[version][(b2 >> 2) & 3]
    kbps = BITRATES[version][b2 >> 4]
    return (144000 if version == 3 else 72000) * kbps // rate + ((b2 >> 1) & 1)

def side_length(b1, b3):
    mono = (b3 >> 6) == 3
    if (b1 >> 3) & 3 == 3:
        return 17 if mono else 32
    return 9 if mono else 17

# CRC-16 field: empty when the protection bit is 1 (no CRC).
def crc_field(hdr):
    b1, b2, b3 = header(hdr)
    if b1 & 1:
        return b''
    return crc16(bytes([b2, b3]) + bytes(side_length(b1, b3))).to_bytes(2, 'big')

# Zero side information and main data up to the frame length.
def body(hdr):
    b1, b2, _ = header(hdr)
    return bytes(frame_length(b1, b2) - 4 - (0 if b1 & 1 else 2))

# Bitrate byte of a later frame: the first frame's sample rate, the frame's
# own bitrate (VBR) or the first frame's bitrate (CBR), the frame's own padding.
def vbr_b2(first, mine):
    return bytes([(bytes(mine)[0] & 0xf2) | (bytes(first)[0] & 0x0c)])

def cbr_b2(first, mine):
    return bytes([(bytes(mine)[0] & 0x02) | (bytes(first)[0] & 0xfc)])

# Xing frame header byte: the first frame's sample rate and the first frame's
# bitrate, raised to the lowest bitrate whose frame holds the Xing fields.
def xing_b2(first, xb1, xb3):
    b1, b3 = bytes(xb1)[0], bytes(xb3)[0]
    value = bytes(first)[0] & 0xfc
    need = 4 + side_length(b1, b3) + 16
    while frame_length(b1, value) < need:
        value += 0x10
    return bytes([value])

def find_all(node, names, found):
    if str(node.symbol) in names:
        found.append(node)
        return found
    for child in node.children:
        find_all(child, names, found)
    return found

# Side information (zeros), "Xing" or "Info", flags (frames and bytes), the
# audio frame count, the byte count of all MPEG frames including this one,
# then zeros to the frame length.
def xing_body(start, xhdr):
    b1, b2, b3 = header(xhdr)
    frames = find_all(start, FRAMES, [])
    total = frame_length(b1, b2) + sum(len(bytes(frame)) for frame in frames)
    kinds = {bytes(frame)[2] >> 4 for frame in frames}
    side = side_length(b1, b3)
    fields = (b'Info' if len(kinds) == 1 else b'Xing') + (3).to_bytes(4, 'big') \
        + len(frames).to_bytes(4, 'big') + total.to_bytes(4, 'big')
    return bytes(side) + fields + bytes(max(0, frame_length(b1, b2) - 4 - side - len(fields)))

def u32(n):
    return n.to_bytes(4, 'big')

def synchsafe(n):
    return bytes([(n >> 21) & 0x7f, (n >> 14) & 0x7f, (n >> 7) & 0x7f, n & 0x7f])

# Three of four alternatives carry an ID3v2 tag (with or without an ID3v1
# trailer); the fourth has only the ID3v1 trailer.
<start> ::= <v2_file> | <v2_file> | <v2_file> | <v1_file>
<v2_file> ::= <id3v2> <audio> <id3v1>?
<v1_file> ::= <audio> <id3v1>

# ---------------------------------------------------------------- audio
<audio> ::= <xing> <frame0> <cbr>{4,59} | <xing> <frame0> <vbr>{4,59} | <frame0> <cbr>{4,59} | <frame0> <vbr>{4,59}
<frame0> ::= <hdr> <crc> <body>
<cbr> ::= <hdr> <crc> <body>
<vbr> ::= <hdr> <crc> <body>
<xing> ::= <xhdr> <xbody>

# Header: sync, then MPEG-1 (0xFB/0xFA) or MPEG-2 (0xF3/0xF2) Layer III with
# (0xFA, 0xF2) or without a CRC. Bitrate byte: index 1-14, sample rate index
# 0-2, padding 0 or 1, private bit 0. Mode byte: stereo, joint stereo with
# mode extension 0-3, dual channel or mono, original bit 0 or 1, no
# emphasis.
<hdr> ::= b'\xff' <b1> <b2> <b3>
<xhdr> ::= b'\xff' <xb1> <b2> <b3>
<b1> ::= b'\xfb' | b'\xfa' | b'\xf3' | b'\xf2'
<xb1> ::= b'\xfb' | b'\xf3'
<b2> ::= rb'[\x10\x12\x14\x16\x18\x1a\x20\x22\x24\x26\x28\x2a\x30\x32\x34\x36\x38\x3a\x40\x42\x44\x46\x48\x4a\x50\x52\x54\x56\x58\x5a\x60\x62\x64\x66\x68\x6a\x70\x72\x74\x76\x78\x7a\x80\x82\x84\x86\x88\x8a\x90\x92\x94\x96\x98\x9a\xa0\xa2\xa4\xa6\xa8\xaa\xb0\xb2\xb4\xb6\xb8\xba\xc0\xc2\xc4\xc6\xc8\xca\xd0\xd2\xd4\xd6\xd8\xda\xe0\xe2\xe4\xe6\xe8\xea]'
<b3> ::= rb'[\x00\x04]' | rb'[\x40\x44\x50\x54\x60\x64\x70\x74]' | rb'[\x80\x84]' | rb'[\xc0\xc4]'
<crc> ::= rb'([\x00-\xff]{2})?'
<body> ::= rb'\x00*'
<xbody> ::= rb'[\x00-\xff]*'

where <frame0>.<hdr>.<b1> == bytes(<xing>.<xhdr>.<xb1>)
where <xing>.<xhdr>.<b3> == bytes(<frame0>.<hdr>.<b3>)
where <xing>.<xhdr>.<b2> == xing_b2(<frame0>.<hdr>.<b2>, <xing>.<xhdr>.<xb1>, <xing>.<xhdr>.<b3>)
where <cbr>.<hdr>.<b1> == bytes(<frame0>.<hdr>.<b1>)
where <vbr>.<hdr>.<b1> == bytes(<frame0>.<hdr>.<b1>)
where <cbr>.<hdr>.<b3> == bytes(<frame0>.<hdr>.<b3>)
where <vbr>.<hdr>.<b3> == bytes(<frame0>.<hdr>.<b3>)
where <cbr>.<hdr>.<b2> == cbr_b2(<frame0>.<hdr>.<b2>, <cbr>.<hdr>.<b2>)
where <vbr>.<hdr>.<b2> == vbr_b2(<frame0>.<hdr>.<b2>, <vbr>.<hdr>.<b2>)
where <frame0>.<crc> == crc_field(<frame0>.<hdr>)
where <cbr>.<crc> == crc_field(<cbr>.<hdr>)
where <vbr>.<crc> == crc_field(<vbr>.<hdr>)
where <frame0>.<body> == body(<frame0>.<hdr>)
where <cbr>.<body> == body(<cbr>.<hdr>)
where <vbr>.<body> == body(<vbr>.<hdr>)
where <xing>.<xbody> == xing_body(<start>, <xing>.<xhdr>)

# ---------------------------------------------------------------- ID3v2
<id3v2> ::= <id3v23> | <id3v24>
<id3v23> ::= b'ID3\x03\x00\x00' <tag_size> <v23_frames> <padding>?
<id3v24> ::= b'ID3\x04\x00\x00' <tag_size> <v24_frames> <padding>?
<tag_size> ::= rb'[\x00-\x7f]{4}'
<padding> ::= rb'\x00{1,200}'
<fsize> ::= rb'[\x00-\xff]{4}'

<v23_frames> ::= <v23_tit2>? <v23_tpe1>? <v23_talb>? <v23_tyer>? <v23_trck>? <v23_tcon>? <v23_comm>?
<v24_frames> ::= <v24_tit2>? <v24_tpe1>? <v24_talb>? <v24_tdrc>? <v24_trck>? <v24_tcon>? <v24_comm>?
where len(bytes(<v23_frames>)) > 0
where len(bytes(<v24_frames>)) > 0

<v23_tit2> ::= b'TIT2' <fsize> b'\x00\x00' <text23>
<v23_tpe1> ::= b'TPE1' <fsize> b'\x00\x00' <text23>
<v23_talb> ::= b'TALB' <fsize> b'\x00\x00' <text23>
<v23_tyer> ::= b'TYER' <fsize> b'\x00\x00' <year23>
<v23_trck> ::= b'TRCK' <fsize> b'\x00\x00' <track23>
<v23_tcon> ::= b'TCON' <fsize> b'\x00\x00' <genre23>
<v23_comm> ::= b'COMM' <fsize> b'\x00\x00' <comm23>
<v24_tit2> ::= b'TIT2' <fsize> b'\x00\x00' <text24>
<v24_tpe1> ::= b'TPE1' <fsize> b'\x00\x00' <text24>
<v24_talb> ::= b'TALB' <fsize> b'\x00\x00' <text24>
<v24_tdrc> ::= b'TDRC' <fsize> b'\x00\x00' <date24>
<v24_trck> ::= b'TRCK' <fsize> b'\x00\x00' <track24>
<v24_tcon> ::= b'TCON' <fsize> b'\x00\x00' <genre24>
<v24_comm> ::= b'COMM' <fsize> b'\x00\x00' <comm24>

where <id3v23>.<tag_size> == synchsafe(len(bytes(<id3v23>)) - 10)
where <id3v24>.<tag_size> == synchsafe(len(bytes(<id3v24>)) - 10)
where <v23_tit2>.<fsize> == u32(len(bytes(<v23_tit2>)) - 10)
where <v23_tpe1>.<fsize> == u32(len(bytes(<v23_tpe1>)) - 10)
where <v23_talb>.<fsize> == u32(len(bytes(<v23_talb>)) - 10)
where <v23_tyer>.<fsize> == u32(len(bytes(<v23_tyer>)) - 10)
where <v23_trck>.<fsize> == u32(len(bytes(<v23_trck>)) - 10)
where <v23_tcon>.<fsize> == u32(len(bytes(<v23_tcon>)) - 10)
where <v23_comm>.<fsize> == u32(len(bytes(<v23_comm>)) - 10)
where <v24_tit2>.<fsize> == synchsafe(len(bytes(<v24_tit2>)) - 10)
where <v24_tpe1>.<fsize> == synchsafe(len(bytes(<v24_tpe1>)) - 10)
where <v24_talb>.<fsize> == synchsafe(len(bytes(<v24_talb>)) - 10)
where <v24_tdrc>.<fsize> == synchsafe(len(bytes(<v24_tdrc>)) - 10)
where <v24_trck>.<fsize> == synchsafe(len(bytes(<v24_trck>)) - 10)
where <v24_tcon>.<fsize> == synchsafe(len(bytes(<v24_tcon>)) - 10)
where <v24_comm>.<fsize> == synchsafe(len(bytes(<v24_comm>)) - 10)

# Encoded text: 0 ISO-8859-1, 1 UTF-16 with a BOM, 3 UTF-8 (2.4 only)
<text23> ::= b'\x00' <l1_text> | b'\x01' <u16_text>
<text24> ::= b'\x00' <l1_text> | b'\x01' <u16_text> | b'\x03' <u8_text>
<year23> ::= b'\x00' <year> | b'\x01' <u16_year>
<date24> ::= b'\x00' <date> | b'\x01' <u16_date> | b'\x03' <date>
<track23> ::= b'\x00' <track> | b'\x01' <u16_track>
<track24> ::= b'\x00' <track> | b'\x01' <u16_track> | b'\x03' <track>
<genre23> ::= b'\x00' <genre_v23> | b'\x01' <u16_genre_v23>
<genre24> ::= b'\x00' <genre_v24> | b'\x01' <u16_genre_v24> | b'\x03' <genre_v24>
# COMM: encoding, language, short description, terminator, text
<comm23> ::= b'\x00' <lang> <l1_desc> b'\x00' <l1_text> | b'\x01' <lang> <u16_comm>
<comm24> ::= b'\x00' <lang> <l1_desc> b'\x00' <l1_text> | b'\x01' <lang> <u16_comm> | b'\x03' <lang> <l1_desc> b'\x00' <u8_text>
<lang> ::= b'eng' | b'deu' | b'spa'
<u16_comm> ::= b'\xff\xfe' <le_desc> b'\x00\x00' b'\xff\xfe' <le_text> | b'\xfe\xff' <be_desc> b'\x00\x00' b'\xfe\xff' <be_text>

# Words of ASCII letters and digits with at most one other character:
# punctuation that needs escaping in JSON or C strings, a Latin-1 letter,
# or (UTF-16 and UTF-8) a Cyrillic, CJK or astral-plane character.
<l1_text> ::= <l1_word> (b' ' <l1_word>){0,3}
<l1_word> ::= <alnum>{1,8} | <alnum>{0,3} <l1_special> <alnum>{0,3}
<l1_special> ::= <punct> | b'\xe9' | b'\xf1' | b'\xfc' | b'\xdf' | b'\xc5'
<u8_text> ::= <u8_word> (b' ' <u8_word>){0,3}
<u8_word> ::= <alnum>{1,8} | <alnum>{0,3} <u8_special> <alnum>{0,3}
<u8_special> ::= <punct> | b'\xc3\xa9' | b'\xc3\xb1' | b'\xd0\x96' | b'\xe6\x97\xa5' | b'\xf0\x9f\x8e\xb5'
<u16_text> ::= b'\xff\xfe' <le_text> | b'\xfe\xff' <be_text>
<le_text> ::= <le_word> (b' \x00' <le_word>){0,3}
<le_word> ::= <le_alnum>{1,8} | <le_alnum>{0,3} <le_special> <le_alnum>{0,3}
<le_alnum> ::= <alnum> b'\x00'
<le_special> ::= <punct> b'\x00' | b'\xe9\x00' | b'\xf1\x00' | b'\x16\x04' | b'\xe5\x65' | b'\x3c\xd8\xb5\xdf'
<be_text> ::= <be_word> (b'\x00 ' <be_word>){0,3}
<be_word> ::= <be_alnum>{1,8} | <be_alnum>{0,3} <be_special> <be_alnum>{0,3}
<be_alnum> ::= b'\x00' <alnum>
<be_special> ::= b'\x00' <punct> | b'\x00\xe9' | b'\x00\xf1' | b'\x04\x16' | b'\x65\xe5' | b'\xd8\x3c\xdf\xb5'
<alnum> ::= rb'[A-Za-z0-9]'
<punct> ::= b'"' | b'\\' | b"'" | b'&' | b'/' | b'-' | b'(' | b'.'
<l1_desc> ::= <alnum>{0,8}
<le_desc> ::= <le_alnum>{0,8}
<be_desc> ::= <be_alnum>{0,8}

# Numbers: year, date, track and genre
<year> ::= (b'19' | b'20') <digit> <digit>
<date> ::= <year> | <year> b'-' <month> b'-' <day>
<month> ::= b'0' rb'[1-9]' | b'1' rb'[0-2]'
<day> ::= b'0' rb'[1-9]' | b'1' <digit> | b'2' rb'[0-8]'
<track> ::= <number> | <number> b'/' <number>
<number> ::= rb'[1-9]' | rb'[1-9]' <digit>
<genre_v23> ::= b'(' <genre_id> b')' | <genre_name>
<genre_v24> ::= <genre_id> | <genre_name>
<genre_id> ::= <digit> | rb'[1-7]' <digit>
<genre_name> ::= b'Rock' | b'Pop' | b'Jazz' | b'Blues' | b'Classical' | b'Hip-Hop' | b'Electronic'
<digit> ::= rb'[0-9]'
<u16_year> ::= b'\xff\xfe' (b'1\x009\x00' | b'2\x000\x00') <le_digit> <le_digit> | b'\xfe\xff' (b'\x001\x009' | b'\x002\x000') <be_digit> <be_digit>
<u16_date> ::= <u16_year>
<u16_track> ::= b'\xff\xfe' <le_number> (b'/\x00' <le_number>)? | b'\xfe\xff' <be_number> (b'\x00/' <be_number>)?
<le_number> ::= <le_nonzero> <le_digit>?
<be_number> ::= <be_nonzero> <be_digit>?
<le_digit> ::= <digit> b'\x00'
<be_digit> ::= b'\x00' <digit>
<le_nonzero> ::= rb'[1-9]' b'\x00'
<be_nonzero> ::= b'\x00' rb'[1-9]'
<u16_genre_v23> ::= b'\xff\xfe(\x00' <le_digit> b')\x00' | b'\xfe\xff\x00(' <be_digit> b'\x00)' | b'\xff\xfeR\x00o\x00c\x00k\x00' | b'\xfe\xff\x00J\x00a\x00z\x00z'
<u16_genre_v24> ::= b'\xff\xfe' <le_digit> | b'\xfe\xff' <be_digit> | b'\xff\xfeR\x00o\x00c\x00k\x00' | b'\xfe\xff\x00J\x00a\x00z\x00z'

# ---------------------------------------------------------------- ID3v1
# Text fields are fixed-width templates: empty, one to three words of fixed
# lengths (one may hold a Latin-1 letter or punctuation), or a full field
# with no padding.
<id3v1> ::= b'TAG' <v1_30> <v1_30> <v1_30> <year> <v1_comment> <v1_genre>
<v1_comment> ::= <v1_30> | <v1_28> b'\x00' rb'[\x01-\x63]'
<v1_30> ::= b'\x00'{30} | <alnum>{8} b'\x00'{22} | <alnum>{4} b' ' <alnum>{6} b'\x00'{19} | <alnum>{3} <l1_special> <alnum>{3} b'\x00'{23} | <alnum>{5} b' ' <alnum>{2} <l1_special> <alnum>{2} b' ' <alnum>{4} b'\x00'{14} | <alnum>{30}
<v1_28> ::= b'\x00'{28} | <alnum>{8} b'\x00'{20} | <alnum>{4} b' ' <alnum>{6} b'\x00'{17} | <alnum>{3} <l1_special> <alnum>{3} b'\x00'{21} | <alnum>{28}
<v1_genre> ::= rb'[\x00-\x93]' | b'\xff'
