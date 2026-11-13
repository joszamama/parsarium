"""Build JAssimp 1.0.0 JNI from its tag and parse the local ASCII PLY control."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json
import platform
import subprocess
import tarfile
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/java/ascii_ply/jassimp-lock.json"
CONTROL = ROOT / "controls/ascii_ply/triangle.ply"
ADAPTER = ROOT / "adapters/java/ascii_ply/jassimp/JassimpPlyAdapter.java"


def run(command: list[str]) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                               timeout=180, check=True)
    return completed.stdout.strip()


def download(url: str, expected: str, destination: Path) -> None:
    with urlopen(Request(url, headers={"User-Agent": "Parsarium JAssimp verifier"}),
                 timeout=90) as response:
        destination.write_bytes(response.read())
    assert sha256(destination.read_bytes()).hexdigest() == expected, url


def main() -> None:
    assert platform.system() == "Darwin" and platform.machine() == "arm64"
    lock = json.loads(LOCK.read_text())["jassimp"]
    assert sha256(CONTROL.read_bytes()).hexdigest() == lock["control_sha256"]
    dependency = lock["assimp_dependency"]
    assimp = json.loads((ROOT / dependency["source_lock"]).read_text())["assimp"]
    assert assimp["release"] == dependency["release"]
    assert assimp["source_sha256"] == dependency["source_sha256"]
    assert run(["brew", "list", "--versions", "assimp"]) == "assimp 6.0.6"
    for kind in ("header", "library"):
        assert sha256(Path(dependency[f"{kind}_path"]).read_bytes()).hexdigest() == (
            dependency[f"{kind}_sha256"])

    with tempfile.TemporaryDirectory(prefix="parsarium-jassimp-ply-") as directory:
        temp = Path(directory)
        archive = temp / "jassimp-v1.0.0.tar.gz"
        download(lock["source_url"], lock["source_sha256"], archive)
        with tarfile.open(archive) as source_tar:
            for member_name, expected in lock["source_members"].items():
                member = source_tar.extractfile(member_name)
                assert member is not None and sha256(member.read()).hexdigest() == expected
            native_cpp = source_tar.extractfile("JAssimp-1.0.0/JNI/jassimp.cpp")
            native_h = source_tar.extractfile("JAssimp-1.0.0/JNI/jassimp.h")
            assert native_cpp is not None and native_h is not None
            (temp / "jassimp.cpp").write_bytes(native_cpp.read())
            (temp / "jassimp.h").write_bytes(native_h.read())

        jar = temp / "jassimp.jar"
        pom = temp / "jassimp.pom"
        sources_jar = temp / "jassimp-sources.jar"
        for key, path in (("jar", jar), ("pom", pom), ("sources_jar", sources_jar)):
            download(lock[f"{key}_url"], lock[f"{key}_sha256"], path)
        with zipfile.ZipFile(sources_jar) as source_zip:
            java_source = source_zip.read(lock["source_jar_member"])
        assert sha256(java_source).hexdigest() == lock["source_members"][
            "JAssimp-1.0.0/src/main/java/com/github/dabasan/jassimp/Jassimp.java"]

        java_home = Path(run(["/usr/libexec/java_home", "-v", "21"]))
        library = temp / "libjassimp.dylib"
        build_native = ["c++", "-std=c++14", "-w", "-fPIC", "-dynamiclib",
                        str(temp / "jassimp.cpp"), "-I" + str(java_home / "include"),
                        "-I" + str(java_home / "include/darwin"),
                        "-I" + str(Path(dependency["header_path"]).parents[1]),
                        "-L" + str(Path(dependency["library_path"]).parent),
                        "-lassimp", "-o", str(library)]
        run(build_native)
        assert "libassimp.6.dylib" in run(["otool", "-L", str(library)])

        classes = temp / "classes"
        classes.mkdir()
        build_java = ["javac", "--release", "21", "-cp", str(jar),
                      "-d", str(classes), str(ADAPTER)]
        run(build_java)
        command = ["java", "-Djava.library.path=" + str(temp),
                   "-cp", f"{classes}:{jar}", "org.parsarium.JassimpPlyAdapter",
                   str(CONTROL)]
        output = json.loads(run(command))
        assert output == {"meshes": 1, "vertices": 3, "faces": 1}, output
        print(json.dumps({"package": "jassimp", "version": "1.0.0",
                          "output": output, "pass": True}))


if __name__ == "__main__":
    main()
