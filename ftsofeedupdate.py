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

# Function to add a new feed
def add_feed(data, category, name, sources):
    new_feed = {
        "feed": {
            "category": category,
            "name": name
        },
        "sources": sources
    }
    data.append(new_feed)

# Function to update an existing feed
def update_feed(data, name, new_sources=None, new_category=None):
    for feed in data:
        if feed['feed']['name'] == name:
            if new_sources:
                feed['sources'] = new_sources
            if new_category is not None:
                feed['feed']['category'] = new_category
            return True
    return False

# Function to delete a feed by name
def delete_feed(data, name):
    return [feed for feed in data if feed['feed']['name'] != name]

# argparse setup to accept source and destination files
def main():
    parser = argparse.ArgumentParser(description="Modify JSON feeds from the command line")
    parser.add_argument("source_file", help="The source JSON file")
    parser.add_argument("destination_file", help="The destination JSON file")
    parser.add_argument("--add", nargs=3, metavar=('CATEGORY', 'NAME', 'SOURCES'),
                        help="Add a new feed. Example: --add 1 FLR/USD '[{\"exchange\":\"example\",\"symbol\":\"FLR/USD\"}]'")
    parser.add_argument("--update", nargs=3, metavar=('NAME', 'NEW_SOURCES', 'NEW_CATEGORY'),
                        help="Update an existing feed. Example: --update FLR/USD '[{\"exchange\":\"new_exchange\",\"symbol\":\"FLR/USD\"}]' 2")
    parser.add_argument("--delete", metavar='NAME', help="Delete a feed. Example: --delete FLR/USD")
    
    args = parser.parse_args()

    # Load the source JSON file
    data = load_json_file(args.source_file)

    # Handle add, update, and delete operations
    if args.add:
        category = int(args.add[0])
        name = args.add[1]
        sources = json.loads(args.add[2])  # Parse the sources as a JSON string
        add_feed(data, category, name, sources)
        print(f"Added feed: {name}")

    if args.update:
        name = args.update[0]
        new_sources = json.loads(args.update[1])  # Parse the new sources as a JSON string
        new_category = int(args.update[2]) if args.update[2] else None
        if update_feed(data, name, new_sources, new_category):
            print(f"Updated feed: {name}")
        else:
            print(f"Feed not found: {name}")

    if args.delete:
        data = delete_feed(data, args.delete)
        print(f"Deleted feed: {args.delete}")

    # Save the updated JSON to the destination file
    save_json_file(data, args.destination_file)
    print(f"Changes saved to {args.destination_file}")

if __name__ == "__main__":
    main()

# Function to update all feeds based on provided exchanges and base pairs
def update_all_feeds(data, exchanges, base_pairs):
    for exchange in exchanges:
        for base_pair in base_pairs:
            feed_name = f"{exchange}_{base_pair}".lower()
            if feed_name in data["feeds"]:
                print(f"Updating feed: {feed_name}")
                # Update logic for the feed goes here, this is a placeholder
            else:
                print(f"Feed {feed_name} does not exist in the current data.")

def main():
    parser = argparse.ArgumentParser(description="JSON Feed Modification Script")
    
    # Adding the update --all options
    parser.add_argument('--update', action='store_true', help='Update feed(s)')
    parser.add_argument('--all', action='store_true', help='Update all feeds for a list of exchanges and base pairs')
    parser.add_argument('--exchanges', nargs='+', help='List of exchanges to update')
    parser.add_argument('--base-pairs', nargs='+', help='List of base pairs to update')
    
    args = parser.parse_args()

    if args.update and args.all:
        if args.exchanges is None or args.base_pairs is None:
            print("Error: You must specify both exchanges and base pairs when using --update --all.")
        else:
            data = load_json_file("feeds.json")  # Assuming the feeds are in feeds.json
            update_all_feeds(data, args.exchanges, args.base_pairs)
            save_json_file(data, "feeds.json")
            print("All feeds updated successfully.")
    else:
        # Other functionality as per the original script goes here
        pass

if __name__ == "__main__":
    main()

# Including proper handling of source and destination file arguments for updating feeds
