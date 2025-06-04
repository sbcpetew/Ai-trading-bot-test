"""Paper trading entry point."""
import argparse


def main():
    parser = argparse.ArgumentParser(description="Paper trade AlphaFive")
    parser.add_argument("--days", type=int, default=1)
    args = parser.parse_args()
    print(f"Paper trading for {args.days} days... (placeholder)")


if __name__ == "__main__":
    main()
