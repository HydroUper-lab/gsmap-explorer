import sys
import os
import argparse

# supaya bisa akses src/
sys.path.append(os.path.abspath("src"))

from main import run_pipeline


def pilih_mode():
    print("=" * 30)
    print("      PILIH MODE PROGRAM")
    print("=" * 30)
    print("1. Extract CSV")
    print("2. Visualisasi")
    print("3. Hujan Regional (Thiessen)")
    print("4. Semua")
    print()

    mapping = {
        "1": "extract",
        "2": "visualize",
        "3": "thiessen",
        "4": "all"
    }

    while True:
        choice = input("Pilih opsi (1/2/3/4): ").strip()

        if choice in mapping:
            return mapping[choice]

        print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["extract", "visualize", "thiessen", "all"],
        help="Pilih mode"
    )

    args = parser.parse_args()

    # Jika --mode tidak diberikan → tampilkan menu
    mode = args.mode if args.mode else pilih_mode()

    run_pipeline(mode=mode)