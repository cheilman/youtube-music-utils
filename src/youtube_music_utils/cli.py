import argparse
import sys
from pathlib import Path

from ytmusicapi import setup_oauth

from .client import Client


def main():
    parser = argparse.ArgumentParser(description="YouTube Music Utilities CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Version command
    subparsers.add_parser("version", help="Show version")

    # Login command
    parser_login = subparsers.add_parser("login", help="Setup authentication")
    parser_login.add_argument("--file", default="oauth.json", help="Output file for credentials")
    parser_login.add_argument("--client-id", help="OAuth Client ID")
    parser_login.add_argument("--client-secret", help="OAuth Client Secret")

    args = parser.parse_args()

    if args.command == "version":
        # TODO: Get version dynamically from package
        print("youtube-music-utils v0.1.0")
    elif args.command == "login":
        auth_file_path = Path(args.file)

        if args.client_id and args.client_secret:
            print(f"Setting up OAuth to {auth_file_path}...")
            try:
                setup_oauth(
                    client_id=args.client_id,
                    client_secret=args.client_secret,
                    filepath=str(auth_file_path),
                )
                print(f"Authentication successful! Credentials saved to {auth_file_path}")
            except Exception as e:
                print(f"Error during authentication setup: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            if auth_file_path.exists():
                print(f"Auth file '{auth_file_path}' exists. Verifying session...")
                try:
                    # Attempt to initialize client to verify file validity
                    # This relies on YTMusic constructor to validate the file
                    Client(auth=str(auth_file_path))
                    print("Existing session verified successfully.")
                except Exception as e:
                    print(
                        f"Error verifying existing session: {e}. "
                        "Please re-run with --client-id and --client-secret to re-authenticate.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            else:
                print(
                    "Error: --client-id and --client-secret are required to set up a new authentication file."
                    " Alternatively, specify an existing --file to verify an existing session.",
                    file=sys.stderr,
                )
                sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
