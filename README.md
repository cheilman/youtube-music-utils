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

# Setup Authentication
uv run ym-utils login
```

### Library

You can also use the library in your Python code:

```python
from youtube_music_utils import Client

# Initialize client (looks for oauth.json by default or works unauthenticated)
client = Client()

# Or provide path to auth file
client = Client(auth="path/to/oauth.json")

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
