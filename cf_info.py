import os
import argparse
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
import logging
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

# Rich console and logging setup
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        RichHandler(rich_tracebacks=True, show_level=False, show_time=False, show_path=False),
        logging.FileHandler("logs/cloudflare_dns_info.log", mode="a", encoding="utf-8"),
    ],
)
logger = logging.getLogger("cloudflare_dns")

API_ENDPOINT = "https://api.cloudflare.com/client/v4"

headers = {
    "X-Auth-Email": os.getenv("CLOUDFLARE_EMAIL"),
    "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_TOKEN')}",
    "Content-Type": "application/json",
}

def get_accounts():
    url = f"{API_ENDPOINT}/accounts"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("result", [])
    logger.error(f"Failed to fetch accounts: {response.text}")
    return []

def get_zones(account_id):
    url = f"{API_ENDPOINT}/zones?account.id={account_id}&per_page=100"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("result", [])
    logger.error(f"Failed to fetch zones for account {account_id}: {response.text}")
    return []

def get_dns_records(zone_id):
    url = f"{API_ENDPOINT}/zones/{zone_id}/dns_records?per_page=100"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("result", [])
    logger.error(f"Failed to fetch DNS records for zone {zone_id}: {response.text}")
    return []

def type_color(record_type):
    colors = {
        "A": "cyan",
        "CNAME": "green",
        "MX": "yellow",
        "TXT": "magenta",
        "AAAA": "blue",
        "NS": "bright_black",
        "SRV": "bright_magenta",
    }
    return colors.get(record_type, "white")

def proxy_color(proxied):
    return "bright_green" if proxied else "bright_red"

def simplify_name(name, zone_name):
    if name == zone_name:
        return name
    if name.endswith(f".{zone_name}"):
        return name.replace(f".{zone_name}", "")
    return name

def format_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M")

def display_dns_table(account_name, zone_name, records):
    table = Table(title=f"[bold blue]{account_name}[/bold blue] - [bold yellow]{zone_name}[/bold yellow]", show_lines=True,  box=box.HORIZONTALS , title_justify="left" )
    columns = ["Type", "Name", "Contents", "Priority", "Proxy", "TTL", "Created", "Modified", "Message"]

    for col in columns:
        table.add_column(col, style="white")

    for record in records:
        table.add_row(
            f"[{type_color(record.get('type'))}]{record.get('type', '')}[/{type_color(record.get('type'))}]",
            f"[white]{simplify_name(record.get('name', ''), zone_name)}[/white]",
            f"[blue]{record.get('content', '')}[blue]",
            str(record.get("priority", "-")),
            f"[{proxy_color(record.get('proxied', False))}]{record.get('proxied', False)}[/{proxy_color(record.get('proxied', False))}]",
            str(record.get("ttl", "")),
            f"[bright_black]{format_time(record['created_on'])}[/bright_black]",
            f"[bright_black]{format_time(record['modified_on'])}[/bright_black]",
            record.get("comment", ""),
        )

    console.print(table)
    console.print("")
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=str, help="Filter accounts by name (case-insensitive substring)")
    parser.add_argument("--zone", type=str, help="Filter zones by name (case-insensitive substring)")
    args = parser.parse_args()

    env_accounts = [a.lower() for a in os.getenv("ACCOUNTS", "").split(",")] if os.getenv("ACCOUNTS") else None
    env_zones = [z.lower() for z in os.getenv("ZONES", "").split(",")] if os.getenv("ZONES") else None

    accounts = get_accounts()
    if not accounts:
        console.print("[bold red]No accounts available.[/bold red]")
        return

    for account in accounts:
        account_name = account.get("name")
        account_id = account.get("id")

        if env_accounts and not any(e in account_name.lower() for e in env_accounts):
            continue

        if args.account and args.account.lower() not in account_name.lower():
            continue

        zones = get_zones(account_id)
        for zone in zones:
            zone_name = zone.get("name")
            zone_id = zone.get("id")

            if env_zones and not any(e in zone_name.lower() for e in env_zones):
                continue

            if args.zone and args.zone.lower() not in zone_name.lower():
                continue

            records = get_dns_records(zone_id)
            display_dns_table(account_name, zone_name, records)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        console.print(f"[bold red]에러:[/bold red] {e}")