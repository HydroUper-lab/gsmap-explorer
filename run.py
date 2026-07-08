import sys
import os
import argparse

# supaya bisa akses src/
sys.path.append(os.path.abspath("src"))

from main import run_pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["extract", "visualize", "thiessen", "all"],
        default="extract",
        help="Pilih mode: extract | visualize | thiessen | all"
    )

    args = parser.parse_args()

    run_pipeline(mode=args.mode)
