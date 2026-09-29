# TMDB Sentinel

A Python service that monitors TMDB metadata for changes and sends notifications when monitored data is updated.

## Status

Early development.

## Development

This project uses:

- Python
- pytest
- Ruff
- mypy

### Run tests

```bash
pytest
```

### Run linting
```bash
ruff check .
```

### Check formatting 
```bash 
ruff format --check
```

### Run type checking 
```bash
mypy src
```