import csv
from typing import TextIO

from .client import Client


def convert_playlist(input_file: TextIO, output_file: TextIO, client: Client) -> None:
    """
    Reads a playlist CSV, fetches song details, and writes a new CSV.

    Args:
        input_file: Open file object for reading the input CSV.
        output_file: Open file object for writing the output CSV.
        client: Initialized Client for fetching song details.
    """
    reader = csv.reader(input_file)
    writer = csv.writer(output_file, lineterminator="\n")

    # State machine to handle the file sections
    # 0: Playlist Metadata
    # 1: Song Header found, switch to processing songs
    state = 0

    for row in reader:
        if not row:
            writer.writerow(row)
            continue

        if state == 0:
            if row[0].strip() == "Video Id":
                # Found the start of the songs section
                # Write the new header
                writer.writerow(["VideoId", "Title", "Artist", "Album"])
                state = 1
            else:
                # Still in metadata section, just copy
                writer.writerow(row)
        elif state == 1:
            # Processing songs
            video_id = row[0]
            try:
                details = client.get_song_details(video_id)
                writer.writerow(
                    [
                        details.video_id,
                        details.title,
                        details.artist,
                        details.album or "",
                    ]
                )
            except Exception as e:
                # In case of error, maybe write the ID and the error?
                # Or just skip? For now, let's print to stderr and skip/fill empty?
                # The requirement implies a valid conversion.
                # Let's write the ID and empty fields if fetch fails to keep the row?
                # Or better, just raise/print error.
                # For a CLI tool, printing to stderr is good.
                import sys

                print(f"Error fetching details for {video_id}: {e}", file=sys.stderr)
                writer.writerow([video_id, "ERROR", "ERROR", "ERROR"])
