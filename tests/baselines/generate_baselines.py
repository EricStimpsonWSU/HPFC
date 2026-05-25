from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.baselines.reference_cases import generate_baselines


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sHPFC regression baselines")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "data",
        help="Directory that will receive the .npz baseline files",
    )
    args = parser.parse_args()
    written_paths = generate_baselines(args.output_dir)
    for path in written_paths:
        print(path)


if __name__ == "__main__":
    main()
