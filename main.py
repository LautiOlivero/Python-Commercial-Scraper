import sys
import os
import argparse
from scraper import extract_data
from gui import launch_gui


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, nargs='?', help="URL del producto a extraer")
    args = parser.parse_args()
    
    if args.url:
        extract_data(args.url)
    else:
        launch_gui()

if __name__ == "__main__":
    main()

