# Valid RIFF/WAVE files (Microsoft RIFF and WAVEFORMATEX(TENSIBLE) rules).
#
# Each file is one of 24 layouts: PCM (format tag 1) with 8, 16, 24 or 32
# bits and one or two channels, written with a 16-byte PCMWAVEFORMAT or an
# 18-byte WAVEFORMATEX (cbSize 0); IEEE float (tag 3) with 32 or 64 bits and
# one or two channels, an 18-byte WAVEFORMATEX and a fact chunk; and
# WAVE_FORMAT_EXTENSIBLE (tag 0xFFFE, 40-byte fmt, cbSize 22) carrying 16- or
# 24-bit PCM or 32-bit float in one, two, four or six channels with the
# standard channel mask, wValidBitsPerSample equal to the container size and
# a fact chunk. The sample rate is one of nine. nBlockAlign is channels times
# bytes per sample and nAvgBytesPerSec is rate times nBlockAlign; both are
# literal per layout and rate, so no constraint repairs them.
#
# The data chunk holds 1 to 400 whole sample frames, so its length is always
# a multiple of nBlockAlign. The fact chunk's dwSampleLength is the frame
# count. Float samples are finite, with magnitude in [2**-15, 1.0). PCM
# samples are arbitrary bytes. An odd-length chunk (8-bit or 24-bit data with
# an odd frame count, an INFO string or JUNK) is followed by one zero pad
# byte that its size does not count; the RIFF size counts it.
#
# Optional chunks: JUNK before fmt; LIST/INFO (one to four of INAM, IART,
# ICMT, ICRD, IGNR, ISFT, NUL-terminated ASCII) and JUNK between fmt (or
# fact) and data, and after data. fmt always precedes data and appears once;
# there is one data chunk. No cue, smpl, bext or compressed formats.

import struct

def u32(n):
    return struct.pack('<I', n)

def pad(node):
    return b'\x00' if len(bytes(node)) % 2 else b''

<start> ::= b'RIFF' <riff_size> <wave>
where <riff_size> == u32(len(bytes(<wave>)))
<wave> ::= b'WAVE' <lead>? <layout>
<lead> ::= <junk>

# 16-bit PCM is two of the five top-level choices; the other layouts share the rest.
<layout> ::= <pcm16_1> | <pcm16_2> | <pcm_other> | <ieee_float> | <extensible>
<pcm_other> ::= <pcm8_1> | <pcm8_2> | <pcm24_1> | <pcm24_2> | <pcm32_1> | <pcm32_2>
<ieee_float> ::= <float32_1> | <float32_2> | <float64_1> | <float64_2>
<extensible> ::= <ext_pcm16_1> | <ext_pcm16_2> | <ext_pcm16_4> | <ext_pcm16_6> | <ext_pcm24_1> | <ext_pcm24_2> | <ext_pcm24_4> | <ext_pcm24_6> | <ext_float32_1> | <ext_float32_2> | <ext_float32_4> | <ext_float32_6>

<pcm8_1> ::= <fmt_pcm8_1> <mid>{0,2} <data_pcm8_1> <tail>{0,2}
<pcm8_2> ::= <fmt_pcm8_2> <mid>{0,2} <data_pcm8_2> <tail>{0,2}
<pcm16_1> ::= <fmt_pcm16_1> <mid>{0,2} <data_pcm16_1> <tail>{0,2}
<pcm16_2> ::= <fmt_pcm16_2> <mid>{0,2} <data_pcm16_2> <tail>{0,2}
<pcm24_1> ::= <fmt_pcm24_1> <mid>{0,2} <data_pcm24_1> <tail>{0,2}
<pcm24_2> ::= <fmt_pcm24_2> <mid>{0,2} <data_pcm24_2> <tail>{0,2}
<pcm32_1> ::= <fmt_pcm32_1> <mid>{0,2} <data_pcm32_1> <tail>{0,2}
<pcm32_2> ::= <fmt_pcm32_2> <mid>{0,2} <data_pcm32_2> <tail>{0,2}
<float32_1> ::= <fmt_float32_1> <fact> <mid>{0,2} <data_float32_1> <tail>{0,2}
<float32_2> ::= <fmt_float32_2> <fact> <mid>{0,2} <data_float32_2> <tail>{0,2}
<float64_1> ::= <fmt_float64_1> <fact> <mid>{0,2} <data_float64_1> <tail>{0,2}
<float64_2> ::= <fmt_float64_2> <fact> <mid>{0,2} <data_float64_2> <tail>{0,2}
<ext_pcm16_1> ::= <fmt_ext_pcm16_1> <fact> <mid>{0,2} <data_ext_pcm16_1> <tail>{0,2}
<ext_pcm16_2> ::= <fmt_ext_pcm16_2> <fact> <mid>{0,2} <data_ext_pcm16_2> <tail>{0,2}
<ext_pcm16_4> ::= <fmt_ext_pcm16_4> <fact> <mid>{0,2} <data_ext_pcm16_4> <tail>{0,2}
<ext_pcm16_6> ::= <fmt_ext_pcm16_6> <fact> <mid>{0,2} <data_ext_pcm16_6> <tail>{0,2}
<ext_pcm24_1> ::= <fmt_ext_pcm24_1> <fact> <mid>{0,2} <data_ext_pcm24_1> <tail>{0,2}
<ext_pcm24_2> ::= <fmt_ext_pcm24_2> <fact> <mid>{0,2} <data_ext_pcm24_2> <tail>{0,2}
<ext_pcm24_4> ::= <fmt_ext_pcm24_4> <fact> <mid>{0,2} <data_ext_pcm24_4> <tail>{0,2}
<ext_pcm24_6> ::= <fmt_ext_pcm24_6> <fact> <mid>{0,2} <data_ext_pcm24_6> <tail>{0,2}
<ext_float32_1> ::= <fmt_ext_float32_1> <fact> <mid>{0,2} <data_ext_float32_1> <tail>{0,2}
<ext_float32_2> ::= <fmt_ext_float32_2> <fact> <mid>{0,2} <data_ext_float32_2> <tail>{0,2}
<ext_float32_4> ::= <fmt_ext_float32_4> <fact> <mid>{0,2} <data_ext_float32_4> <tail>{0,2}
<ext_float32_6> ::= <fmt_ext_float32_6> <fact> <mid>{0,2} <data_ext_float32_6> <tail>{0,2}

<mid> ::= <list_info> | <junk>
<tail> ::= <list_info> | <junk>

# fmt chunks: the rate alternative carries nSamplesPerSec and nAvgBytesPerSec.
<fmt_pcm8_1> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm8_1> b'\x01\x00\x08\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm8_1> b'\x01\x00\x08\x00\x00\x00')
<rate_pcm8_1> ::= b'\x40\x1f\x00\x00\x40\x1f\x00\x00' | b'\x11\x2b\x00\x00\x11\x2b\x00\x00' | b'\x80\x3e\x00\x00\x80\x3e\x00\x00' | b'\x22\x56\x00\x00\x22\x56\x00\x00' | b'\xc0\x5d\x00\x00\xc0\x5d\x00\x00' | b'\x00\x7d\x00\x00\x00\x7d\x00\x00' | b'\x44\xac\x00\x00\x44\xac\x00\x00' | b'\x80\xbb\x00\x00\x80\xbb\x00\x00' | b'\x00\x77\x01\x00\x00\x77\x01\x00'
<fmt_pcm8_2> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm8_2> b'\x02\x00\x08\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm8_2> b'\x02\x00\x08\x00\x00\x00')
<rate_pcm8_2> ::= b'\x40\x1f\x00\x00\x80\x3e\x00\x00' | b'\x11\x2b\x00\x00\x22\x56\x00\x00' | b'\x80\x3e\x00\x00\x00\x7d\x00\x00' | b'\x22\x56\x00\x00\x44\xac\x00\x00' | b'\xc0\x5d\x00\x00\x80\xbb\x00\x00' | b'\x00\x7d\x00\x00\x00\xfa\x00\x00' | b'\x44\xac\x00\x00\x88\x58\x01\x00' | b'\x80\xbb\x00\x00\x00\x77\x01\x00' | b'\x00\x77\x01\x00\x00\xee\x02\x00'
<fmt_pcm16_1> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm16_1> b'\x02\x00\x10\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm16_1> b'\x02\x00\x10\x00\x00\x00')
<rate_pcm16_1> ::= b'\x40\x1f\x00\x00\x80\x3e\x00\x00' | b'\x11\x2b\x00\x00\x22\x56\x00\x00' | b'\x80\x3e\x00\x00\x00\x7d\x00\x00' | b'\x22\x56\x00\x00\x44\xac\x00\x00' | b'\xc0\x5d\x00\x00\x80\xbb\x00\x00' | b'\x00\x7d\x00\x00\x00\xfa\x00\x00' | b'\x44\xac\x00\x00\x88\x58\x01\x00' | b'\x80\xbb\x00\x00\x00\x77\x01\x00' | b'\x00\x77\x01\x00\x00\xee\x02\x00'
<fmt_pcm16_2> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm16_2> b'\x04\x00\x10\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm16_2> b'\x04\x00\x10\x00\x00\x00')
<rate_pcm16_2> ::= b'\x40\x1f\x00\x00\x00\x7d\x00\x00' | b'\x11\x2b\x00\x00\x44\xac\x00\x00' | b'\x80\x3e\x00\x00\x00\xfa\x00\x00' | b'\x22\x56\x00\x00\x88\x58\x01\x00' | b'\xc0\x5d\x00\x00\x00\x77\x01\x00' | b'\x00\x7d\x00\x00\x00\xf4\x01\x00' | b'\x44\xac\x00\x00\x10\xb1\x02\x00' | b'\x80\xbb\x00\x00\x00\xee\x02\x00' | b'\x00\x77\x01\x00\x00\xdc\x05\x00'
<fmt_pcm24_1> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm24_1> b'\x03\x00\x18\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm24_1> b'\x03\x00\x18\x00\x00\x00')
<rate_pcm24_1> ::= b'\x40\x1f\x00\x00\xc0\x5d\x00\x00' | b'\x11\x2b\x00\x00\x33\x81\x00\x00' | b'\x80\x3e\x00\x00\x80\xbb\x00\x00' | b'\x22\x56\x00\x00\x66\x02\x01\x00' | b'\xc0\x5d\x00\x00\x40\x19\x01\x00' | b'\x00\x7d\x00\x00\x00\x77\x01\x00' | b'\x44\xac\x00\x00\xcc\x04\x02\x00' | b'\x80\xbb\x00\x00\x80\x32\x02\x00' | b'\x00\x77\x01\x00\x00\x65\x04\x00'
<fmt_pcm24_2> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm24_2> b'\x06\x00\x18\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm24_2> b'\x06\x00\x18\x00\x00\x00')
<rate_pcm24_2> ::= b'\x40\x1f\x00\x00\x80\xbb\x00\x00' | b'\x11\x2b\x00\x00\x66\x02\x01\x00' | b'\x80\x3e\x00\x00\x00\x77\x01\x00' | b'\x22\x56\x00\x00\xcc\x04\x02\x00' | b'\xc0\x5d\x00\x00\x80\x32\x02\x00' | b'\x00\x7d\x00\x00\x00\xee\x02\x00' | b'\x44\xac\x00\x00\x98\x09\x04\x00' | b'\x80\xbb\x00\x00\x00\x65\x04\x00' | b'\x00\x77\x01\x00\x00\xca\x08\x00'
<fmt_pcm32_1> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm32_1> b'\x04\x00\x20\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x01\x00' <rate_pcm32_1> b'\x04\x00\x20\x00\x00\x00')
<rate_pcm32_1> ::= b'\x40\x1f\x00\x00\x00\x7d\x00\x00' | b'\x11\x2b\x00\x00\x44\xac\x00\x00' | b'\x80\x3e\x00\x00\x00\xfa\x00\x00' | b'\x22\x56\x00\x00\x88\x58\x01\x00' | b'\xc0\x5d\x00\x00\x00\x77\x01\x00' | b'\x00\x7d\x00\x00\x00\xf4\x01\x00' | b'\x44\xac\x00\x00\x10\xb1\x02\x00' | b'\x80\xbb\x00\x00\x00\xee\x02\x00' | b'\x00\x77\x01\x00\x00\xdc\x05\x00'
<fmt_pcm32_2> ::= b'fmt ' (b'\x10\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm32_2> b'\x08\x00\x20\x00' | b'\x12\x00\x00\x00' b'\x01\x00\x02\x00' <rate_pcm32_2> b'\x08\x00\x20\x00\x00\x00')
<rate_pcm32_2> ::= b'\x40\x1f\x00\x00\x00\xfa\x00\x00' | b'\x11\x2b\x00\x00\x88\x58\x01\x00' | b'\x80\x3e\x00\x00\x00\xf4\x01\x00' | b'\x22\x56\x00\x00\x10\xb1\x02\x00' | b'\xc0\x5d\x00\x00\x00\xee\x02\x00' | b'\x00\x7d\x00\x00\x00\xe8\x03\x00' | b'\x44\xac\x00\x00\x20\x62\x05\x00' | b'\x80\xbb\x00\x00\x00\xdc\x05\x00' | b'\x00\x77\x01\x00\x00\xb8\x0b\x00'
<fmt_float32_1> ::= b'fmt ' b'\x12\x00\x00\x00' b'\x03\x00\x01\x00' <rate_float32_1> b'\x04\x00\x20\x00\x00\x00'
<rate_float32_1> ::= b'\x40\x1f\x00\x00\x00\x7d\x00\x00' | b'\x11\x2b\x00\x00\x44\xac\x00\x00' | b'\x80\x3e\x00\x00\x00\xfa\x00\x00' | b'\x22\x56\x00\x00\x88\x58\x01\x00' | b'\xc0\x5d\x00\x00\x00\x77\x01\x00' | b'\x00\x7d\x00\x00\x00\xf4\x01\x00' | b'\x44\xac\x00\x00\x10\xb1\x02\x00' | b'\x80\xbb\x00\x00\x00\xee\x02\x00' | b'\x00\x77\x01\x00\x00\xdc\x05\x00'
<fmt_float32_2> ::= b'fmt ' b'\x12\x00\x00\x00' b'\x03\x00\x02\x00' <rate_float32_2> b'\x08\x00\x20\x00\x00\x00'
<rate_float32_2> ::= b'\x40\x1f\x00\x00\x00\xfa\x00\x00' | b'\x11\x2b\x00\x00\x88\x58\x01\x00' | b'\x80\x3e\x00\x00\x00\xf4\x01\x00' | b'\x22\x56\x00\x00\x10\xb1\x02\x00' | b'\xc0\x5d\x00\x00\x00\xee\x02\x00' | b'\x00\x7d\x00\x00\x00\xe8\x03\x00' | b'\x44\xac\x00\x00\x20\x62\x05\x00' | b'\x80\xbb\x00\x00\x00\xdc\x05\x00' | b'\x00\x77\x01\x00\x00\xb8\x0b\x00'
<fmt_float64_1> ::= b'fmt ' b'\x12\x00\x00\x00' b'\x03\x00\x01\x00' <rate_float64_1> b'\x08\x00\x40\x00\x00\x00'
<rate_float64_1> ::= b'\x40\x1f\x00\x00\x00\xfa\x00\x00' | b'\x11\x2b\x00\x00\x88\x58\x01\x00' | b'\x80\x3e\x00\x00\x00\xf4\x01\x00' | b'\x22\x56\x00\x00\x10\xb1\x02\x00' | b'\xc0\x5d\x00\x00\x00\xee\x02\x00' | b'\x00\x7d\x00\x00\x00\xe8\x03\x00' | b'\x44\xac\x00\x00\x20\x62\x05\x00' | b'\x80\xbb\x00\x00\x00\xdc\x05\x00' | b'\x00\x77\x01\x00\x00\xb8\x0b\x00'
<fmt_float64_2> ::= b'fmt ' b'\x12\x00\x00\x00' b'\x03\x00\x02\x00' <rate_float64_2> b'\x10\x00\x40\x00\x00\x00'
<rate_float64_2> ::= b'\x40\x1f\x00\x00\x00\xf4\x01\x00' | b'\x11\x2b\x00\x00\x10\xb1\x02\x00' | b'\x80\x3e\x00\x00\x00\xe8\x03\x00' | b'\x22\x56\x00\x00\x20\x62\x05\x00' | b'\xc0\x5d\x00\x00\x00\xdc\x05\x00' | b'\x00\x7d\x00\x00\x00\xd0\x07\x00' | b'\x44\xac\x00\x00\x40\xc4\x0a\x00' | b'\x80\xbb\x00\x00\x00\xb8\x0b\x00' | b'\x00\x77\x01\x00\x00\x70\x17\x00'
<fmt_ext_pcm16_1> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x01\x00' <rate_ext_pcm16_1> b'\x02\x00\x10\x00\x16\x00\x10\x00\x04\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm16_1> ::= b'\x40\x1f\x00\x00\x80\x3e\x00\x00' | b'\x11\x2b\x00\x00\x22\x56\x00\x00' | b'\x80\x3e\x00\x00\x00\x7d\x00\x00' | b'\x22\x56\x00\x00\x44\xac\x00\x00' | b'\xc0\x5d\x00\x00\x80\xbb\x00\x00' | b'\x00\x7d\x00\x00\x00\xfa\x00\x00' | b'\x44\xac\x00\x00\x88\x58\x01\x00' | b'\x80\xbb\x00\x00\x00\x77\x01\x00' | b'\x00\x77\x01\x00\x00\xee\x02\x00'
<fmt_ext_pcm16_2> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x02\x00' <rate_ext_pcm16_2> b'\x04\x00\x10\x00\x16\x00\x10\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm16_2> ::= b'\x40\x1f\x00\x00\x00\x7d\x00\x00' | b'\x11\x2b\x00\x00\x44\xac\x00\x00' | b'\x80\x3e\x00\x00\x00\xfa\x00\x00' | b'\x22\x56\x00\x00\x88\x58\x01\x00' | b'\xc0\x5d\x00\x00\x00\x77\x01\x00' | b'\x00\x7d\x00\x00\x00\xf4\x01\x00' | b'\x44\xac\x00\x00\x10\xb1\x02\x00' | b'\x80\xbb\x00\x00\x00\xee\x02\x00' | b'\x00\x77\x01\x00\x00\xdc\x05\x00'
<fmt_ext_pcm16_4> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x04\x00' <rate_ext_pcm16_4> b'\x08\x00\x10\x00\x16\x00\x10\x00\x33\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm16_4> ::= b'\x40\x1f\x00\x00\x00\xfa\x00\x00' | b'\x11\x2b\x00\x00\x88\x58\x01\x00' | b'\x80\x3e\x00\x00\x00\xf4\x01\x00' | b'\x22\x56\x00\x00\x10\xb1\x02\x00' | b'\xc0\x5d\x00\x00\x00\xee\x02\x00' | b'\x00\x7d\x00\x00\x00\xe8\x03\x00' | b'\x44\xac\x00\x00\x20\x62\x05\x00' | b'\x80\xbb\x00\x00\x00\xdc\x05\x00' | b'\x00\x77\x01\x00\x00\xb8\x0b\x00'
<fmt_ext_pcm16_6> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x06\x00' <rate_ext_pcm16_6> b'\x0c\x00\x10\x00\x16\x00\x10\x00\x3f\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm16_6> ::= b'\x40\x1f\x00\x00\x00\x77\x01\x00' | b'\x11\x2b\x00\x00\xcc\x04\x02\x00' | b'\x80\x3e\x00\x00\x00\xee\x02\x00' | b'\x22\x56\x00\x00\x98\x09\x04\x00' | b'\xc0\x5d\x00\x00\x00\x65\x04\x00' | b'\x00\x7d\x00\x00\x00\xdc\x05\x00' | b'\x44\xac\x00\x00\x30\x13\x08\x00' | b'\x80\xbb\x00\x00\x00\xca\x08\x00' | b'\x00\x77\x01\x00\x00\x94\x11\x00'
<fmt_ext_pcm24_1> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x01\x00' <rate_ext_pcm24_1> b'\x03\x00\x18\x00\x16\x00\x18\x00\x04\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm24_1> ::= b'\x40\x1f\x00\x00\xc0\x5d\x00\x00' | b'\x11\x2b\x00\x00\x33\x81\x00\x00' | b'\x80\x3e\x00\x00\x80\xbb\x00\x00' | b'\x22\x56\x00\x00\x66\x02\x01\x00' | b'\xc0\x5d\x00\x00\x40\x19\x01\x00' | b'\x00\x7d\x00\x00\x00\x77\x01\x00' | b'\x44\xac\x00\x00\xcc\x04\x02\x00' | b'\x80\xbb\x00\x00\x80\x32\x02\x00' | b'\x00\x77\x01\x00\x00\x65\x04\x00'
<fmt_ext_pcm24_2> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x02\x00' <rate_ext_pcm24_2> b'\x06\x00\x18\x00\x16\x00\x18\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm24_2> ::= b'\x40\x1f\x00\x00\x80\xbb\x00\x00' | b'\x11\x2b\x00\x00\x66\x02\x01\x00' | b'\x80\x3e\x00\x00\x00\x77\x01\x00' | b'\x22\x56\x00\x00\xcc\x04\x02\x00' | b'\xc0\x5d\x00\x00\x80\x32\x02\x00' | b'\x00\x7d\x00\x00\x00\xee\x02\x00' | b'\x44\xac\x00\x00\x98\x09\x04\x00' | b'\x80\xbb\x00\x00\x00\x65\x04\x00' | b'\x00\x77\x01\x00\x00\xca\x08\x00'
<fmt_ext_pcm24_4> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x04\x00' <rate_ext_pcm24_4> b'\x0c\x00\x18\x00\x16\x00\x18\x00\x33\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm24_4> ::= b'\x40\x1f\x00\x00\x00\x77\x01\x00' | b'\x11\x2b\x00\x00\xcc\x04\x02\x00' | b'\x80\x3e\x00\x00\x00\xee\x02\x00' | b'\x22\x56\x00\x00\x98\x09\x04\x00' | b'\xc0\x5d\x00\x00\x00\x65\x04\x00' | b'\x00\x7d\x00\x00\x00\xdc\x05\x00' | b'\x44\xac\x00\x00\x30\x13\x08\x00' | b'\x80\xbb\x00\x00\x00\xca\x08\x00' | b'\x00\x77\x01\x00\x00\x94\x11\x00'
<fmt_ext_pcm24_6> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x06\x00' <rate_ext_pcm24_6> b'\x12\x00\x18\x00\x16\x00\x18\x00\x3f\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_pcm24_6> ::= b'\x40\x1f\x00\x00\x80\x32\x02\x00' | b'\x11\x2b\x00\x00\x32\x07\x03\x00' | b'\x80\x3e\x00\x00\x00\x65\x04\x00' | b'\x22\x56\x00\x00\x64\x0e\x06\x00' | b'\xc0\x5d\x00\x00\x80\x97\x06\x00' | b'\x00\x7d\x00\x00\x00\xca\x08\x00' | b'\x44\xac\x00\x00\xc8\x1c\x0c\x00' | b'\x80\xbb\x00\x00\x00\x2f\x0d\x00' | b'\x00\x77\x01\x00\x00\x5e\x1a\x00'
<fmt_ext_float32_1> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x01\x00' <rate_ext_float32_1> b'\x04\x00\x20\x00\x16\x00\x20\x00\x04\x00\x00\x00\x03\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_float32_1> ::= b'\x40\x1f\x00\x00\x00\x7d\x00\x00' | b'\x11\x2b\x00\x00\x44\xac\x00\x00' | b'\x80\x3e\x00\x00\x00\xfa\x00\x00' | b'\x22\x56\x00\x00\x88\x58\x01\x00' | b'\xc0\x5d\x00\x00\x00\x77\x01\x00' | b'\x00\x7d\x00\x00\x00\xf4\x01\x00' | b'\x44\xac\x00\x00\x10\xb1\x02\x00' | b'\x80\xbb\x00\x00\x00\xee\x02\x00' | b'\x00\x77\x01\x00\x00\xdc\x05\x00'
<fmt_ext_float32_2> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x02\x00' <rate_ext_float32_2> b'\x08\x00\x20\x00\x16\x00\x20\x00\x03\x00\x00\x00\x03\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_float32_2> ::= b'\x40\x1f\x00\x00\x00\xfa\x00\x00' | b'\x11\x2b\x00\x00\x88\x58\x01\x00' | b'\x80\x3e\x00\x00\x00\xf4\x01\x00' | b'\x22\x56\x00\x00\x10\xb1\x02\x00' | b'\xc0\x5d\x00\x00\x00\xee\x02\x00' | b'\x00\x7d\x00\x00\x00\xe8\x03\x00' | b'\x44\xac\x00\x00\x20\x62\x05\x00' | b'\x80\xbb\x00\x00\x00\xdc\x05\x00' | b'\x00\x77\x01\x00\x00\xb8\x0b\x00'
<fmt_ext_float32_4> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x04\x00' <rate_ext_float32_4> b'\x10\x00\x20\x00\x16\x00\x20\x00\x33\x00\x00\x00\x03\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_float32_4> ::= b'\x40\x1f\x00\x00\x00\xf4\x01\x00' | b'\x11\x2b\x00\x00\x10\xb1\x02\x00' | b'\x80\x3e\x00\x00\x00\xe8\x03\x00' | b'\x22\x56\x00\x00\x20\x62\x05\x00' | b'\xc0\x5d\x00\x00\x00\xdc\x05\x00' | b'\x00\x7d\x00\x00\x00\xd0\x07\x00' | b'\x44\xac\x00\x00\x40\xc4\x0a\x00' | b'\x80\xbb\x00\x00\x00\xb8\x0b\x00' | b'\x00\x77\x01\x00\x00\x70\x17\x00'
<fmt_ext_float32_6> ::= b'fmt ' b'\x28\x00\x00\x00' b'\xfe\xff\x06\x00' <rate_ext_float32_6> b'\x18\x00\x20\x00\x16\x00\x20\x00\x3f\x00\x00\x00\x03\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xaa\x00\x38\x9b\x71'
<rate_ext_float32_6> ::= b'\x40\x1f\x00\x00\x00\xee\x02\x00' | b'\x11\x2b\x00\x00\x98\x09\x04\x00' | b'\x80\x3e\x00\x00\x00\xdc\x05\x00' | b'\x22\x56\x00\x00\x30\x13\x08\x00' | b'\xc0\x5d\x00\x00\x00\xca\x08\x00' | b'\x00\x7d\x00\x00\x00\xb8\x0b\x00' | b'\x44\xac\x00\x00\x60\x26\x10\x00' | b'\x80\xbb\x00\x00\x00\x94\x11\x00' | b'\x00\x77\x01\x00\x00\x28\x23\x00'

# data chunks: whole frames, then the pad byte when the length is odd.
<data_pcm8_1> ::= b'data' <size> <frames_pcm8_1> <pad>
<frames_pcm8_1> ::= <frame_pcm8_1>{1,400}
<frame_pcm8_1> ::= <s8>
<data_pcm8_2> ::= b'data' <size> <frames_pcm8_2> <pad>
<frames_pcm8_2> ::= <frame_pcm8_2>{1,400}
<frame_pcm8_2> ::= <s8> <s8>
<data_pcm16_1> ::= b'data' <size> <frames_pcm16_1> <pad>
<frames_pcm16_1> ::= <frame_pcm16_1>{1,400}
<frame_pcm16_1> ::= <s16>
<data_pcm16_2> ::= b'data' <size> <frames_pcm16_2> <pad>
<frames_pcm16_2> ::= <frame_pcm16_2>{1,400}
<frame_pcm16_2> ::= <s16> <s16>
<data_pcm24_1> ::= b'data' <size> <frames_pcm24_1> <pad>
<frames_pcm24_1> ::= <frame_pcm24_1>{1,400}
<frame_pcm24_1> ::= <s24>
<data_pcm24_2> ::= b'data' <size> <frames_pcm24_2> <pad>
<frames_pcm24_2> ::= <frame_pcm24_2>{1,400}
<frame_pcm24_2> ::= <s24> <s24>
<data_pcm32_1> ::= b'data' <size> <frames_pcm32_1> <pad>
<frames_pcm32_1> ::= <frame_pcm32_1>{1,400}
<frame_pcm32_1> ::= <s32>
<data_pcm32_2> ::= b'data' <size> <frames_pcm32_2> <pad>
<frames_pcm32_2> ::= <frame_pcm32_2>{1,400}
<frame_pcm32_2> ::= <s32> <s32>
<data_float32_1> ::= b'data' <size> <frames_float32_1> <pad>
<frames_float32_1> ::= <frame_float32_1>{1,400}
<frame_float32_1> ::= <f32>
<data_float32_2> ::= b'data' <size> <frames_float32_2> <pad>
<frames_float32_2> ::= <frame_float32_2>{1,400}
<frame_float32_2> ::= <f32> <f32>
<data_float64_1> ::= b'data' <size> <frames_float64_1> <pad>
<frames_float64_1> ::= <frame_float64_1>{1,400}
<frame_float64_1> ::= <f64>
<data_float64_2> ::= b'data' <size> <frames_float64_2> <pad>
<frames_float64_2> ::= <frame_float64_2>{1,400}
<frame_float64_2> ::= <f64> <f64>
<data_ext_pcm16_1> ::= b'data' <size> <frames_ext_pcm16_1> <pad>
<frames_ext_pcm16_1> ::= <frame_ext_pcm16_1>{1,400}
<frame_ext_pcm16_1> ::= <s16>
<data_ext_pcm16_2> ::= b'data' <size> <frames_ext_pcm16_2> <pad>
<frames_ext_pcm16_2> ::= <frame_ext_pcm16_2>{1,400}
<frame_ext_pcm16_2> ::= <s16> <s16>
<data_ext_pcm16_4> ::= b'data' <size> <frames_ext_pcm16_4> <pad>
<frames_ext_pcm16_4> ::= <frame_ext_pcm16_4>{1,400}
<frame_ext_pcm16_4> ::= <s16> <s16> <s16> <s16>
<data_ext_pcm16_6> ::= b'data' <size> <frames_ext_pcm16_6> <pad>
<frames_ext_pcm16_6> ::= <frame_ext_pcm16_6>{1,400}
<frame_ext_pcm16_6> ::= <s16> <s16> <s16> <s16> <s16> <s16>
<data_ext_pcm24_1> ::= b'data' <size> <frames_ext_pcm24_1> <pad>
<frames_ext_pcm24_1> ::= <frame_ext_pcm24_1>{1,400}
<frame_ext_pcm24_1> ::= <s24>
<data_ext_pcm24_2> ::= b'data' <size> <frames_ext_pcm24_2> <pad>
<frames_ext_pcm24_2> ::= <frame_ext_pcm24_2>{1,400}
<frame_ext_pcm24_2> ::= <s24> <s24>
<data_ext_pcm24_4> ::= b'data' <size> <frames_ext_pcm24_4> <pad>
<frames_ext_pcm24_4> ::= <frame_ext_pcm24_4>{1,400}
<frame_ext_pcm24_4> ::= <s24> <s24> <s24> <s24>
<data_ext_pcm24_6> ::= b'data' <size> <frames_ext_pcm24_6> <pad>
<frames_ext_pcm24_6> ::= <frame_ext_pcm24_6>{1,400}
<frame_ext_pcm24_6> ::= <s24> <s24> <s24> <s24> <s24> <s24>
<data_ext_float32_1> ::= b'data' <size> <frames_ext_float32_1> <pad>
<frames_ext_float32_1> ::= <frame_ext_float32_1>{1,400}
<frame_ext_float32_1> ::= <f32>
<data_ext_float32_2> ::= b'data' <size> <frames_ext_float32_2> <pad>
<frames_ext_float32_2> ::= <frame_ext_float32_2>{1,400}
<frame_ext_float32_2> ::= <f32> <f32>
<data_ext_float32_4> ::= b'data' <size> <frames_ext_float32_4> <pad>
<frames_ext_float32_4> ::= <frame_ext_float32_4>{1,400}
<frame_ext_float32_4> ::= <f32> <f32> <f32> <f32>
<data_ext_float32_6> ::= b'data' <size> <frames_ext_float32_6> <pad>
<frames_ext_float32_6> ::= <frame_ext_float32_6>{1,400}
<frame_ext_float32_6> ::= <f32> <f32> <f32> <f32> <f32> <f32>

where <data_pcm8_1>.<size> == u32(len(bytes(<data_pcm8_1>.<frames_pcm8_1>)))
where <data_pcm8_1>.<pad> == pad(<data_pcm8_1>.<frames_pcm8_1>)
where <data_pcm8_2>.<size> == u32(len(bytes(<data_pcm8_2>.<frames_pcm8_2>)))
where <data_pcm8_2>.<pad> == pad(<data_pcm8_2>.<frames_pcm8_2>)
where <data_pcm16_1>.<size> == u32(len(bytes(<data_pcm16_1>.<frames_pcm16_1>)))
where <data_pcm16_1>.<pad> == pad(<data_pcm16_1>.<frames_pcm16_1>)
where <data_pcm16_2>.<size> == u32(len(bytes(<data_pcm16_2>.<frames_pcm16_2>)))
where <data_pcm16_2>.<pad> == pad(<data_pcm16_2>.<frames_pcm16_2>)
where <data_pcm24_1>.<size> == u32(len(bytes(<data_pcm24_1>.<frames_pcm24_1>)))
where <data_pcm24_1>.<pad> == pad(<data_pcm24_1>.<frames_pcm24_1>)
where <data_pcm24_2>.<size> == u32(len(bytes(<data_pcm24_2>.<frames_pcm24_2>)))
where <data_pcm24_2>.<pad> == pad(<data_pcm24_2>.<frames_pcm24_2>)
where <data_pcm32_1>.<size> == u32(len(bytes(<data_pcm32_1>.<frames_pcm32_1>)))
where <data_pcm32_1>.<pad> == pad(<data_pcm32_1>.<frames_pcm32_1>)
where <data_pcm32_2>.<size> == u32(len(bytes(<data_pcm32_2>.<frames_pcm32_2>)))
where <data_pcm32_2>.<pad> == pad(<data_pcm32_2>.<frames_pcm32_2>)
where <data_float32_1>.<size> == u32(len(bytes(<data_float32_1>.<frames_float32_1>)))
where <data_float32_1>.<pad> == pad(<data_float32_1>.<frames_float32_1>)
where <float32_1>.<fact>.<count> == u32(len(bytes(<data_float32_1>.<frames_float32_1>)) // 4)
where <data_float32_2>.<size> == u32(len(bytes(<data_float32_2>.<frames_float32_2>)))
where <data_float32_2>.<pad> == pad(<data_float32_2>.<frames_float32_2>)
where <float32_2>.<fact>.<count> == u32(len(bytes(<data_float32_2>.<frames_float32_2>)) // 8)
where <data_float64_1>.<size> == u32(len(bytes(<data_float64_1>.<frames_float64_1>)))
where <data_float64_1>.<pad> == pad(<data_float64_1>.<frames_float64_1>)
where <float64_1>.<fact>.<count> == u32(len(bytes(<data_float64_1>.<frames_float64_1>)) // 8)
where <data_float64_2>.<size> == u32(len(bytes(<data_float64_2>.<frames_float64_2>)))
where <data_float64_2>.<pad> == pad(<data_float64_2>.<frames_float64_2>)
where <float64_2>.<fact>.<count> == u32(len(bytes(<data_float64_2>.<frames_float64_2>)) // 16)
where <data_ext_pcm16_1>.<size> == u32(len(bytes(<data_ext_pcm16_1>.<frames_ext_pcm16_1>)))
where <data_ext_pcm16_1>.<pad> == pad(<data_ext_pcm16_1>.<frames_ext_pcm16_1>)
where <ext_pcm16_1>.<fact>.<count> == u32(len(bytes(<data_ext_pcm16_1>.<frames_ext_pcm16_1>)) // 2)
where <data_ext_pcm16_2>.<size> == u32(len(bytes(<data_ext_pcm16_2>.<frames_ext_pcm16_2>)))
where <data_ext_pcm16_2>.<pad> == pad(<data_ext_pcm16_2>.<frames_ext_pcm16_2>)
where <ext_pcm16_2>.<fact>.<count> == u32(len(bytes(<data_ext_pcm16_2>.<frames_ext_pcm16_2>)) // 4)
where <data_ext_pcm16_4>.<size> == u32(len(bytes(<data_ext_pcm16_4>.<frames_ext_pcm16_4>)))
where <data_ext_pcm16_4>.<pad> == pad(<data_ext_pcm16_4>.<frames_ext_pcm16_4>)
where <ext_pcm16_4>.<fact>.<count> == u32(len(bytes(<data_ext_pcm16_4>.<frames_ext_pcm16_4>)) // 8)
where <data_ext_pcm16_6>.<size> == u32(len(bytes(<data_ext_pcm16_6>.<frames_ext_pcm16_6>)))
where <data_ext_pcm16_6>.<pad> == pad(<data_ext_pcm16_6>.<frames_ext_pcm16_6>)
where <ext_pcm16_6>.<fact>.<count> == u32(len(bytes(<data_ext_pcm16_6>.<frames_ext_pcm16_6>)) // 12)
where <data_ext_pcm24_1>.<size> == u32(len(bytes(<data_ext_pcm24_1>.<frames_ext_pcm24_1>)))
where <data_ext_pcm24_1>.<pad> == pad(<data_ext_pcm24_1>.<frames_ext_pcm24_1>)
where <ext_pcm24_1>.<fact>.<count> == u32(len(bytes(<data_ext_pcm24_1>.<frames_ext_pcm24_1>)) // 3)
where <data_ext_pcm24_2>.<size> == u32(len(bytes(<data_ext_pcm24_2>.<frames_ext_pcm24_2>)))
where <data_ext_pcm24_2>.<pad> == pad(<data_ext_pcm24_2>.<frames_ext_pcm24_2>)
where <ext_pcm24_2>.<fact>.<count> == u32(len(bytes(<data_ext_pcm24_2>.<frames_ext_pcm24_2>)) // 6)
where <data_ext_pcm24_4>.<size> == u32(len(bytes(<data_ext_pcm24_4>.<frames_ext_pcm24_4>)))
where <data_ext_pcm24_4>.<pad> == pad(<data_ext_pcm24_4>.<frames_ext_pcm24_4>)
where <ext_pcm24_4>.<fact>.<count> == u32(len(bytes(<data_ext_pcm24_4>.<frames_ext_pcm24_4>)) // 12)
where <data_ext_pcm24_6>.<size> == u32(len(bytes(<data_ext_pcm24_6>.<frames_ext_pcm24_6>)))
where <data_ext_pcm24_6>.<pad> == pad(<data_ext_pcm24_6>.<frames_ext_pcm24_6>)
where <ext_pcm24_6>.<fact>.<count> == u32(len(bytes(<data_ext_pcm24_6>.<frames_ext_pcm24_6>)) // 18)
where <data_ext_float32_1>.<size> == u32(len(bytes(<data_ext_float32_1>.<frames_ext_float32_1>)))
where <data_ext_float32_1>.<pad> == pad(<data_ext_float32_1>.<frames_ext_float32_1>)
where <ext_float32_1>.<fact>.<count> == u32(len(bytes(<data_ext_float32_1>.<frames_ext_float32_1>)) // 4)
where <data_ext_float32_2>.<size> == u32(len(bytes(<data_ext_float32_2>.<frames_ext_float32_2>)))
where <data_ext_float32_2>.<pad> == pad(<data_ext_float32_2>.<frames_ext_float32_2>)
where <ext_float32_2>.<fact>.<count> == u32(len(bytes(<data_ext_float32_2>.<frames_ext_float32_2>)) // 8)
where <data_ext_float32_4>.<size> == u32(len(bytes(<data_ext_float32_4>.<frames_ext_float32_4>)))
where <data_ext_float32_4>.<pad> == pad(<data_ext_float32_4>.<frames_ext_float32_4>)
where <ext_float32_4>.<fact>.<count> == u32(len(bytes(<data_ext_float32_4>.<frames_ext_float32_4>)) // 16)
where <data_ext_float32_6>.<size> == u32(len(bytes(<data_ext_float32_6>.<frames_ext_float32_6>)))
where <data_ext_float32_6>.<pad> == pad(<data_ext_float32_6>.<frames_ext_float32_6>)
where <ext_float32_6>.<fact>.<count> == u32(len(bytes(<data_ext_float32_6>.<frames_ext_float32_6>)) // 24)

<fact> ::= b'fact' b'\x04\x00\x00\x00' <count>

<list_info> ::= b'LIST' <size> <info_body>
where <list_info>.<size> == u32(len(bytes(<list_info>.<info_body>)))
<info_body> ::= b'INFO' <info_item>{1,4}
<info_item> ::= <info_id> <size> <info_text> <pad>
where <info_item>.<size> == u32(len(bytes(<info_item>.<info_text>)))
where <info_item>.<pad> == pad(<info_item>.<info_text>)
<info_id> ::= b'INAM' | b'IART' | b'ICMT' | b'ICRD' | b'IGNR' | b'ISFT'
<info_text> ::= <achar>{1,24} b'\x00'

<junk> ::= b'JUNK' <size> <junk_data> <pad>
where <junk>.<size> == u32(len(bytes(<junk>.<junk_data>)))
where <junk>.<pad> == pad(<junk>.<junk_data>)
<junk_data> ::= b'\x00'{1,33}

<riff_size> ::= <byte>{4}
<size> ::= <byte>{4}
<count> ::= <byte>{4}
<pad> ::= rb'\x00?'
<s8> ::= <byte>
<s16> ::= <byte>{2}
<s24> ::= <byte>{3}
<s32> ::= <byte>{4}
# |x| in [2**-15, 0.5) for float32 and [2**-15, 1.0) for float64
<f32> ::= <byte>{3} rb'[\x38-\x3e\xb8-\xbe]'
<f64> ::= <byte>{6} rb'[\x00-\xef]' rb'[\x3f\xbf]'
<byte> ::= rb'[\x00-\xff]'
<achar> ::= rb'[\x20-\x7e]'
