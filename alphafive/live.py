"""Live trading entry point."""
import argparse


def main():
    parser = argparse.ArgumentParser(description="Live trade AlphaFive")
    parser.add_argument("--confirm", action="store_true", help="confirm live trading")
    args = parser.parse_args()
    if not args.confirm:
        print("Live trading requires --confirm flag")
        return
    print("Starting live trading... (placeholder)")


if __name__ == "__main__":
    main()
