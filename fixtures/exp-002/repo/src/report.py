"""Small, synthetic CLI report used only for ACIL experiments."""
import argparse


def main():
    parser = argparse.ArgumentParser(description="Synthetic greeting report")
    parser.add_argument("--name", default="guest")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
