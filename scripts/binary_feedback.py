"""Validate AFL++ binary feedback without equating tuples to source coverage."""

from hashlib import sha256
from pathlib import Path
import re


def checked_range(value: str) -> tuple[int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-f]+-0x[0-9a-f]+", value):
        raise ValueError(f"invalid QEMU address range: {value!r}")
    start, end = (int(part, 16) for part in value.split("-"))
    if not 0 < start < end:
        raise ValueError(f"invalid QEMU address range: {value!r}")
    return start, end


def check_binary_feedback(project: Path, root: Path, manifest: dict, feedback: dict) -> None:
    """Require a pinned parser DSO and isolated, repeatable native edge feedback."""
    if manifest.get("coverage_kind") != "native_binary_edges":
        raise ValueError("project is not configured for native binary feedback")
    if manifest.get("binary_feedback_scope") != "underlying_shared_library":
        raise ValueError("binary feedback must name its underlying library scope")
    module = manifest["binary_feedback_module"]
    module_hash = manifest["binary_feedback_module_sha256"]
    tool_digest = manifest["binary_feedback_tool_image_digest"]
    module_path = Path(module)
    if (not module.startswith("/opt/venv/lib/")
            or ".." in module_path.parts
            or not re.fullmatch(r"lib[A-Za-z0-9_+.-]+\.so(?:\.[A-Za-z0-9_.-]+)?", module_path.name)
            or not re.fullmatch(r"[0-9a-f]{64}", module_hash)
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", tool_digest)):
        raise ValueError("binary module or tool image is not pinned")
    variant = root / manifest["binary_feedback_variant"]
    if (not variant.is_file() or sha256(variant.read_bytes()).hexdigest()
            != manifest["binary_feedback_variant_sha256"]):
        raise ValueError("binary feedback variant control changed")
    dockerfile = (project / "binary-feedback/Dockerfile").read_text()
    if tool_digest not in dockerfile or "afl-qemu-trace" not in dockerfile:
        raise ValueError("binary feedback Dockerfile does not pin AFL++ QEMU")
    if (feedback.get("feedback_kind") != "native_binary_edges_not_source_coverage"
            or feedback.get("module") != module
            or feedback.get("module_sha256") != module_hash
            or feedback.get("repeat_identical") is not True
            or feedback.get("variant_differs") is not True
            or not isinstance(feedback.get("control_tuples"), int)
            or feedback["control_tuples"] < 10
            or not isinstance(feedback.get("variant_tuples"), int)
            or feedback["variant_tuples"] < 10
            or not isinstance(feedback.get("excluded_module_tuples"), int)
            or not 0 <= feedback["excluded_module_tuples"] <= 2
            or feedback["control_tuples"] <= feedback["excluded_module_tuples"] + 10
            or not re.fullmatch(r"[0-9a-f]{64}", feedback.get("control_map_sha256", ""))):
        raise ValueError("binary feedback is not isolated and repeatable")
    module_start, module_end = checked_range(feedback["module_text_range"])
    executable_start, executable_end = checked_range(feedback["executable_excluded_range"])
    if module_start < executable_end and executable_start < module_end:
        raise ValueError("binary module overlaps excluded host executable")
