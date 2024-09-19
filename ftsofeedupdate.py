import json

# Load JSON data from file
with open("/mnt/data/feeds.json", "r") as file:
    data = json.load(file)

# Function to add a new feed
def add_feed(category, name, sources):
    new_feed = {
        "feed": {
            "category": category,
            "name": name
        },
        "sources": sources
    }
    data.append(new_feed)

# Function to update a feed by name
def update_feed(feed_name, new_sources=None, new_category=None):
    for feed in data:
        if feed['feed']['name'] == feed_name:
            if new_sources:
                feed['sources'] = new_sources
            if new_category is not None:
                feed['feed']['category'] = new_category
            return True
    return False

# Function to delete a feed by name
def delete_feed(feed_name):
    global data
    data = [feed for feed in data if feed['feed']['name'] != feed_name]

# Example Usage
# Adding a new feed
add_feed(1, "NEW_FEED/USD", [{"exchange": "example", "symbol": "NEW/USD"}])

# Updating a feed
update_feed("FLR/USD", new_sources=[{"exchange": "new_exchange", "symbol": "FLR/NEW"}])

# Deleting a feed
delete_feed("SGB/USD")

# Save the updated JSON back to the file
with open("/mnt/data/feeds_updated.json", "w") as file:
    json.dump(data, file, indent=4)

print("Changes made and saved to feeds_updated.json.")
