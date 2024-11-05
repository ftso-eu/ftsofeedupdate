
import json
import argparse

def update_feed(feed_data, category, exchange_pairs, update_all=False, specific_pair=None):
    for feed in feed_data:
        if feed['feed']['category'] == category:
            feed_name = feed['feed']['name']
            base_asset = feed_name.split('/')[0]

            # Skip feeds that don't match the specific pair if --pair is specified
            if specific_pair and base_asset != specific_pair:
                continue

            existing_exchanges = {source['exchange']: source for source in feed['sources']}
            new_sources = []

            # Add USD and USDT pairs based on exchange groupings
            for exchanges, base_pair in exchange_pairs:
                symbol = f"{base_asset}/{base_pair}"
                for exchange in exchanges:
                    if exchange not in existing_exchanges or existing_exchanges[exchange]['symbol'] != symbol:
                        new_sources.append({"exchange": exchange, "symbol": symbol})

            # Update sources while preserving unique entries
            feed['sources'].extend(new_sources)
            feed['sources'] = list({(source['exchange'], source['symbol']): source for source in feed['sources']}.values())

def main():
    parser = argparse.ArgumentParser(description="Update feed sources with specific base pairs per exchange group.")
    parser.add_argument("--category", type=int, required=True, help="Category of the feed to update.")
    parser.add_argument("--exchange-pairs", nargs='+', action='append', metavar=('EXCHANGES', 'BASE_PAIR'),
                        help="List of exchanges and base pair, e.g., '--exchange-pairs exchange1 exchange2 USD' for USD base pair.")
    parser.add_argument("--source-file", required=True, help="Path to the input JSON file.")
    parser.add_argument("--dest-file", required=True, help="Path to the output JSON file.")
    parser.add_argument("--all", action="store_true", help="Update all pairs in the specified category.")
    parser.add_argument("--pair", help="Update a specific pair (e.g., BTC).")

    args = parser.parse_args()

    # Check if --all or --pair is provided
    if not args.all and not args.pair:
        parser.error("Either --all or --pair must be specified.")

    # Load feed data
    with open(args.source_file, 'r') as f:
        feed_data = json.load(f)

    # Process exchange pairs argument
    exchange_pairs = [(exch_list[:-1], exch_list[-1]) for exch_list in args.exchange_pairs]

    # Update feed data
    update_feed(feed_data, args.category, exchange_pairs, update_all=args.all, specific_pair=args.pair)

    # Save updated feed data
    with open(args.dest_file, 'w') as f:
        json.dump(feed_data, f, indent=4)

if __name__ == "__main__":
    main()
