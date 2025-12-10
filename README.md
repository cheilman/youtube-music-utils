# youtube-music-utils

Utilities for interfacing with YouTube Music.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
uv sync
```

## Usage

### CLI

The project provides a CLI tool `ym-utils`.

```bash
# Show version
uv run ym-utils version
```

### Library

You can also use the library in your Python code:

```python
from youtube_music_utils import Client

# Initialize client (always unauthenticated)
client = Client()

# Access underlying ytmusicapi instance
results = client.api.search("The Beatles")
print(results)
```

## Development

Run tests:

```bash
uv run pytest
```

Lint and format:



```bash

uv run ruff check .

uv run ruff format .

```



Type check:



```bash

uv run mypy src tests

```
