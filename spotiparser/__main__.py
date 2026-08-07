import sys
import argparse
from rich.console import Console
from rich.table import Table

from spotiparser.client import SpotiClient
from spotiparser.parser import parse_profile
from spotiparser.exceptions import SpotiError

console = Console()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", help="URL to scrape")
    p.add_argument("--json", action="store_true", help="output raw json")
    args = p.parse_args()

    client = SpotiClient()
    
    try:
        html = client.get_raw(args.url)
        if "/artist/" in args.url:
            # logic for artists will go here
            pass
        
        # for now just testing profiles
        res = parse_profile(html)
        
        if args.json:
            print(res.model_dump_json())
            return

        table = Table(title=f"Stats for {res.name}")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Followers", str(res.followers))
        table.add_row("Following", str(res.following))
        console.print(table)

    except SpotiError as e:
        console.print(f"[bold red]Error:[/] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected crash:[/] {e}")
        # print(html) # debug helper
        sys.exit(1)

if __name__ == "__main__":
    main()
