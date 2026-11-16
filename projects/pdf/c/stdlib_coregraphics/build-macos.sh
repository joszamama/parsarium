#!/bin/sh
# Build replay.c against the system Core Graphics framework on the observed macOS host.
# Set PARSARIUM_ALLOW_UNPINNED=1 to build on another macOS/SDK; such builds cannot refresh the receipt.
set -eu

PINNED_OS_VERSION=27.2
PINNED_OS_BUILD=26B123
PINNED_ARCH=arm64
PINNED_CLT=27.2.0.0.1792721180
PINNED_SDK_VERSION=27.2
PINNED_SDK_BUILD=26B118
PINNED_COMPILER="Apple clang version 21.0.0 (clang-2100.4.1.1)"

project=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$project/target"

[ "$(uname -s)" = Darwin ] || { echo "Core Graphics requires macOS" >&2; exit 1; }
sdk=$(xcrun --sdk macosx --show-sdk-path)
os_version=$(sw_vers -productVersion)
os_build=$(sw_vers -buildVersion)
arch=$(uname -m)
clt=$(pkgutil --pkg-info=com.apple.pkg.CLTools_Executables 2>/dev/null | sed -n 's/^version: //p')
sdk_version=$(xcrun --sdk macosx --show-sdk-version)
sdk_build=$(xcrun --sdk macosx --show-sdk-build-version)
compiler=$(xcrun clang --version | head -n 1)
developer_dir=$(xcode-select -p)

pinned=true
for pair in "$os_version|$PINNED_OS_VERSION" "$os_build|$PINNED_OS_BUILD" "$arch|$PINNED_ARCH" \
            "$clt|$PINNED_CLT" "$sdk_version|$PINNED_SDK_VERSION" "$sdk_build|$PINNED_SDK_BUILD" \
            "$compiler|$PINNED_COMPILER"; do
    observed=${pair%%|*}
    expected=${pair#*|}
    if [ "$observed" != "$expected" ]; then
        echo "toolchain mismatch: observed '$observed', pinned '$expected'" >&2
        pinned=false
    fi
done
if [ "$pinned" = false ] && [ "${PARSARIUM_ALLOW_UNPINNED:-}" != 1 ]; then
    echo "refusing unpinned build; set PARSARIUM_ALLOW_UNPINNED=1 to build anyway" >&2
    exit 1
fi

xcrun clang -std=c11 -O2 -Wall -Wextra -Werror -arch "$arch" -isysroot "$sdk" \
    "$project/replay.c" -framework CoreGraphics -framework CoreFoundation \
    -o "$project/target/coregraphics-replay"

cat > "$project/target/toolchain.json" <<JSON
{
  "pinned": $pinned,
  "os_version": "$os_version",
  "os_build": "$os_build",
  "arch": "$arch",
  "developer_dir": "$developer_dir",
  "command_line_tools": "$clt",
  "sdk_version": "$sdk_version",
  "sdk_build": "$sdk_build",
  "compiler": "$compiler",
  "core_graphics_tbd_sha256": "$(shasum -a 256 "$sdk/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics.tbd" | cut -d ' ' -f 1)"
}
JSON
echo "$project/target/coregraphics-replay"
