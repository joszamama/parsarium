#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
module_dir="$repo_root/adapters/go/ascii_ply"
native_dir="$module_dir/native/plyfile"
mkdir -p "$native_dir"

cd "$module_dir"
go mod download github.com/cobaltgray/go-plyfile github.com/bloeys/assimp-go
cobalt_dir="$(go list -m -f '{{.Dir}}' github.com/cobaltgray/go-plyfile)"
clang -O2 -c "$cobalt_dir/lib/plyfile.c" -o "$native_dir/plyfile.o"
ar rcs "$native_dir/libplyfile.a" "$native_dir/plyfile.o"

if [[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  bloeys_dir="$(go list -m -f '{{.Dir}}' github.com/bloeys/assimp-go)"
  ln -sfn "$bloeys_dir/asig/libs/libassimp_darwin_arm64.dylib" "$native_dir/libassimp.5.dylib"
fi

printf '%s\n' "$native_dir"
