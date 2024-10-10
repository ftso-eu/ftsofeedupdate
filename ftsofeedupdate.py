
import json
import argparse

# Function to load the JSON file
def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Function to save the updated JSON file
def save_json_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Function to check if a source already exists in a feed
def source_exists(sources, exchange, symbol):
    for source in sources:
        if source['exchange'] == exchange and source['symbol'] == symbol:
            return True
    return False

# Function to update feeds with category, exchanges, and base pairs
def update_all_feeds(data, exchanges, base_pairs, category):
    for feed in data:
        # Update the category for every existing feed
        feed['feed']['category'] = category
        feed_name = feed['feed']['name'].split('/')[0]  # Extract symbol from the feed name (before the '/')
        print(f"Updating category and sources for feed: {feed_name}")
        
        # For each base pair and exchange, update the sources
        for base_pair in base_pairs:
            symbol = f"{feed_name}/{base_pair}"  # Correctly format the symbol
            for exchange in exchanges:
                if not source_exists(feed['sources'], exchange, symbol):
                    feed['sources'].append({
                        'exchange': exchange,
                        'symbol': symbol
                    })
                    print(f"Added source {exchange} with symbol {symbol} to feed {feed_name}")

def main():
    parser = argparse.ArgumentParser(description="JSON Feed Modification Script")
    
    # Adding the update --all options as a flag, not expecting arguments
    parser.add_argument('--update', action='store_true', help='Update feed(s)')
    parser.add_argument('--all', action='store_true', help='Update all feeds for a list of base pairs')
    parser.add_argument('--exchanges', nargs='+', help='List of exchanges to update', required=True)
    parser.add_argument('--base-pairs', nargs='+', help='List of base pairs to update', required=True)
    parser.add_argument('--category', type=int, required=True, help='Numeric category of the feeds to update')

    # Adding the source and destination file options
    parser.add_argument('--source-file', required=True, help='Path to the source JSON file')
    parser.add_argument('--dest-file', required=True, help='Path to the destination JSON file')
    
    args = parser.parse_args()

    if args.update and args.all:
        if args.exchanges is None or args.base_pairs is None:
            print("Error: You must specify both exchanges and base pairs when using --update --all.")
        else:
            # Load the source file
            data = load_json_file(args.source_file)
            
            # Update or add feeds
            update_all_feeds(data, args.exchanges, args.base_pairs, args.category)
            
            # Save the updated data to the destination file
            save_json_file(data, args.dest_file)
            print(f"All feeds updated successfully and saved to {args.dest_file}.")
    else:
        print("Error: Please use the --update and --all options correctly.")

if __name__ == "__main__":
    main()
