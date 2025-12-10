import argparse
import sys

from .client import Client
from .playlist import convert_playlist


def main():
    parser = argparse.ArgumentParser(description="YouTube Music Utilities CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Version command
    subparsers.add_parser("version", help="Show version")

    # Get Song command
    parser_get_song = subparsers.add_parser("get-song", help="Get song metadata by Video ID")
    parser_get_song.add_argument("video_id", help="The Video ID of the song")

    # Convert Playlist command
    parser_convert = subparsers.add_parser("convert-playlist", help="Convert playlist CSV with enriched metadata")
    parser_convert.add_argument("input_file", help="Path to input CSV file")
    parser_convert.add_argument("output_file", help="Path to output CSV file")

    args = parser.parse_args()

    if args.command == "version":
        # TODO: Get version dynamically from package
        print("youtube-music-utils v0.1.0")
    elif args.command == "get-song":
        try:
            client = Client()
            result = client.get_song_details(video_id=args.video_id)
            print(result)
        except Exception as e:
            print(f"Error getting song: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "convert-playlist":
        try:
            client = Client()
            with (
                open(args.input_file, "r", encoding="utf-8") as f_in,
                open(args.output_file, "w", encoding="utf-8", newline="") as f_out,
            ):
                convert_playlist(f_in, f_out, client)
            print(f"Successfully converted playlist to {args.output_file}")
        except Exception as e:
            print(f"Error converting playlist: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
