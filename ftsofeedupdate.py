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

# Function to update a feed by name (case-sensitive)
def update_feed(data, name, new_sources=None, new_category=None):
    feed_found = False
    for feed in data:
        if feed['feed']['name'] == name:  # Case-sensitive matching
            feed_found = True
            if new_sources:  # Update sources only if new_sources is provided
                feed['sources'] = new_sources
            if new_category is not None:  # Update category if new_category is provided
                feed['feed']['category'] = new_category
            print(f"Feed '{name}' updated successfully.")
            break

    if not feed_found:
        print(f"Feed not found: {name}")
    return feed_found


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
