import difflib
from pathlib import Path

import pytest

from mdwrap.common.formatter import Formatter
from mdwrap.md.line_context import LineContext
from mdwrap.md.transforms.unwrap_transform import UnwrapTransform
from mdwrap.md.transforms.wrap_transform import WrapTransform


@pytest.mark.parametrize(
    "test_path_str",
    [str(f) for f in (Path(__file__).parent / "integration").iterdir() if f.is_dir()],
)
def test_files(test_path_str: str) -> None:
    """Test formatter on files."""
    test_path = Path(test_path_str)
    test_file = test_path / "test.md"
    expected_file = test_path / "expected.md"
    output_file = test_path / "output.md"
    diff_file = test_path / "output.diff"

    line_context = LineContext()
    formatter = Formatter(
        line_context=line_context,
        transforms=[UnwrapTransform(), WrapTransform(print_width=80)],
    )
    actual = formatter._format_text(test_file.read_text())

    if not expected_file.exists():
        expected_file.write_text(actual)
        output_file.unlink(missing_ok=True)
        diff_file.unlink(missing_ok=True)
        pytest.skip(f"Expected file {expected_file} does not exist. Creating new file.")

    if actual != expected_file.read_text():
        output_file.write_text(actual)
        diff = "\n".join(
            difflib.unified_diff(
                expected_file.read_text().splitlines(),
                actual.splitlines(),
                fromfile="expected",
                tofile="actual",
            )
        )
        diff_file.write_text(diff)
    else:
        output_file.unlink(missing_ok=True)
        diff_file.unlink(missing_ok=True)
    assert actual == expected_file.read_text()
