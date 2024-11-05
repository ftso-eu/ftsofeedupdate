
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

            # Filter out any existing sources that don't match the specified exchanges and pairs
            new_sources = []
            existing_sources = {(source['exchange'], source['symbol']): source for source in feed['sources']}

            # Add USD and USDT pairs based on exchange groupings
            for exchanges, base_pair in exchange_pairs:
                for exchange in exchanges:
                    symbol = f"{base_asset}/{base_pair}"
                    key = (exchange, symbol)
                    # Only add if not already present in existing_sources
                    if key not in existing_sources:
                        new_sources.append({"exchange": exchange, "symbol": symbol})
                    # Remove any existing conflicting pairs from the same exchange
                    conflicting_symbol = f"{base_asset}/{'USDT' if base_pair == 'USD' else 'USD'}"
                    conflicting_key = (exchange, conflicting_symbol)
                    if conflicting_key in existing_sources:
                        del existing_sources[conflicting_key]

            # Combine new sources with existing sources, ensuring no duplicates
            feed['sources'] = list(existing_sources.values()) + new_sources

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
