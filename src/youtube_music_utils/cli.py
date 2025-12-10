import argparse
import sys

from ytmusicapi import setup_oauth


def main():
    parser = argparse.ArgumentParser(description="YouTube Music Utilities CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Version command
    subparsers.add_parser("version", help="Show version")

    # Login command
    parser_login = subparsers.add_parser("login", help="Setup authentication")
    parser_login.add_argument("--file", default="oauth.json", help="Output file for credentials")

    args = parser.parse_args()

    if args.command == "version":
        # TODO: Get version dynamically from package
        print("youtube-music-utils v0.1.0")
    elif args.command == "login":
        print(f"Setting up OAuth to {args.file}...")
        try:
            setup_oauth(filepath=args.file)
            print(f"Authentication successful! Credentials saved to {args.file}")
        except Exception as e:
            print(f"Error during authentication: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
