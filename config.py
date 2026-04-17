from pathlib import Path

BASE_DIR: Path = Path(__file__).parent

CONFIG = {
    "input_dir": BASE_DIR / "data/input",
    "output_dir": BASE_DIR / "data/output",
}