import sys
import argparse
from spotiparser.client import SpotiClient

def main():
    parser = argparse.ArgumentParser(description="Extract Spotify data without API keys")
    parser.add_argument("url", help="Spotify profile or playlist URL")
    args = parser.parse_args()

    client = SpotiClient()
    # TODO: implement actual routing between profile/playlist parsers
    print(f"fetching {args.url}...")
    data = client.get_raw(args.url)
    print("done.")

if __name__ == "__main__":
    main()
