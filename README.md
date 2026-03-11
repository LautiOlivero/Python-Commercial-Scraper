# Python Commercial Scraper

A modular web scraper built with Python, Playwright, and Pandas. Designed for efficient data extraction from dynamic product pages.

## Key Features
- **Dynamic Content Handling**: Uses Playwright to scrape SPA and JavaScript-heavy websites.
- **Internal Data Viewer**: Built-in GUI viewer to inspect records without external software.
- **Export Capabilities**: Clean CSV exports with customizable filenames.
- **Modular Architecture**: Separated logic for scraping, GUI, and configuration.

## Requirements
- Python 3.8+
- Playwright
- Pandas

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install browser binaries:
```bash
playwright install chromium
```

## Usage

### GUI Mode
Run the application without arguments to launch the interactive interface:
```bash
python main.py
```

### CLI Mode
Scrape a specific URL directly from the terminal:
```bash
python main.py <URL>
```

## Project Structure
- `main.py`: Entry point for both CLI and GUI modes.
- `gui.py`: Tkinter-based interface and history viewer.
- `scraper.py`: Core extraction logic using Playwright.
- `config.py`: Global settings and file path management.
- `.gitignore`: Ensures data files and environments are not tracked.
