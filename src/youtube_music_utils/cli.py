import argparse


def main():
    parser = argparse.ArgumentParser(description="YouTube Music Utilities CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Version command
    subparsers.add_parser("version", help="Show version")

    args = parser.parse_args()

    if args.command == "version":
        # TODO: Get version dynamically from package
        print("youtube-music-utils v0.1.0")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
