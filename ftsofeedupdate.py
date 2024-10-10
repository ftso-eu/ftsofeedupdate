
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

# Function to update or add feeds based on provided exchanges, base pairs, and category
def update_all_feeds(data, exchanges, base_pairs, category):
    for base_pair in base_pairs:
        feed_name = f"{base_pair}".upper()
        found_feed = None
        
        # Search for an existing feed with the same name
        for feed in data:
            if feed['feed']['name'] == feed_name:
                found_feed = feed
                break
        
        if found_feed:
            # Update the category of the existing feed
            found_feed['feed']['category'] = category
            print(f"Updating feed: {feed_name} with category {category}")
            
            # Add any new sources (exchange + symbol) that do not exist in the sources list
            for exchange in exchanges:
                symbol = f"{feed_name}"
                if not source_exists(found_feed['sources'], exchange, symbol):
                    found_feed['sources'].append({
                        'exchange': exchange,
                        'symbol': symbol
                    })
                    print(f"Added source {exchange} with symbol {symbol} to feed {feed_name}")
        else:
            # Create a new feed if it doesn't exist
            print(f"Creating new feed: {feed_name}")
            new_feed = {
                "feed": {
                    "category": category,
                    "name": feed_name
                },
                "sources": [
                    {
                        "exchange": exchange,
                        "symbol": base_pair
                    } for exchange in exchanges
                ]
            }
            data.append(new_feed)

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
        # Other functionality as per the original script

if __name__ == "__main__":
    main()
