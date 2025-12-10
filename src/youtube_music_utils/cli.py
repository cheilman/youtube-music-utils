import argparse
import json
import sys

from .client import Client


def main():
    parser = argparse.ArgumentParser(description="YouTube Music Utilities CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Version command
    subparsers.add_parser("version", help="Show version")

    # Get Song command
    parser_get_song = subparsers.add_parser("get-song", help="Get song metadata by Video ID")
    parser_get_song.add_argument("video_id", help="The Video ID of the song")

    args = parser.parse_args()

    if args.command == "version":
        # TODO: Get version dynamically from package
        print("youtube-music-utils v0.1.0")
    elif args.command == "get-song":
        try:
            client = Client()
            result = client.api.get_song(videoId=args.video_id)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error getting song: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
