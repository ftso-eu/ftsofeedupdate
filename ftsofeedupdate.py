
import json
import argparse

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def update_sources(feeds, usd_exchanges, usdt_exchanges, category):
    for feed in feeds:
        if feed['feed']['category'] == category:
            feed_name = feed['feed']['name']
            base_currency = feed_name.split('/')[1]

            # Add USD sources for specified USD exchanges
            if base_currency == 'USD' and usd_exchanges:
                for exchange in usd_exchanges:
                    usd_source = {'exchange': exchange, 'symbol': f"{feed_name}"}
                    if usd_source not in feed['sources']:
                        feed['sources'].append(usd_source)

            # Add USDT sources for specified USDT exchanges
            if base_currency == 'USD' and usdt_exchanges:
                for exchange in usdt_exchanges:
                    usdt_source = {'exchange': exchange, 'symbol': f"{feed_name.split('/')[0]}/USDT"}
                    if usdt_source not in feed['sources']:
                        feed['sources'].append(usdt_source)
    return feeds

def main():
    parser = argparse.ArgumentParser(description="Update FTSO feed JSON with specific USD and USDT pairs")
    parser.add_argument("--source-file", required=True, help="Path to the source JSON file")
    parser.add_argument("--dest-file", required=True, help="Path to save the updated JSON file")
    parser.add_argument("--category", type=int, required=True, help="Category number to update feeds for")
    parser.add_argument("--usd-exchanges", nargs='+', help="List of exchanges to add USD pairs to")
    parser.add_argument("--usdt-exchanges", nargs='+', help="List of exchanges to add USDT pairs to")
    
    args = parser.parse_args()
    
    feeds = load_json(args.source_file)
    updated_feeds = update_sources(feeds, args.usd_exchanges, args.usdt_exchanges, args.category)
    save_json(updated_feeds, args.dest_file)

if __name__ == "__main__":
    main()
