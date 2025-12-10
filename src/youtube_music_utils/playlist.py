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
    # 0: Playlist Metadata Header
    # 1: Playlist Metadata Values
    # 2: Gap/Other
    # 3: Song Header found, switch to processing songs
    state = 0
    header_indices = []
    target_columns = ["Playlist Id", "Channel Id", "Title", "Description"]

    for row in reader:
        if not row:
            writer.writerow(row)
            continue

        if state == 0:
            # Expecting Header Row
            if row[0].strip() == "Video Id":
                # No metadata or skipped? Should not happen based on spec but handle safely
                writer.writerow(["VideoId", "Title", "Artist", "Album"])
                state = 3
            else:
                # Calculate indices for target columns
                header_indices = []
                current_header = row
                for col in target_columns:
                    try:
                        index = current_header.index(col)
                        header_indices.append(index)
                    except ValueError:
                        # Column not found, handle gracefully?
                        # For now, append -1 to indicate missing
                        header_indices.append(-1)
                
                # Write filtered header
                writer.writerow(target_columns)
                state = 1

        elif state == 1:
            # Expecting Value Row
            filtered_values = []
            for index in header_indices:
                if index != -1 and index < len(row):
                    filtered_values.append(row[index])
                else:
                    filtered_values.append("")
            writer.writerow(filtered_values)
            state = 2

        elif state == 2:
            # Waiting for Song Section
            if row[0].strip() == "Video Id":
                writer.writerow(["VideoId", "Title", "Artist", "Album"])
                state = 3
            else:
                # Just copy unknown rows in between? or ignore?
                # Example shows empty line which is handled by `if not row` check at start.
                # If there are other lines, maybe preserve them?
                writer.writerow(row)

        elif state == 3:
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
