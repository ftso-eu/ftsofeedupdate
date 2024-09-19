
# JSON Feed Modification Script

This Python script allows users to modify JSON files containing feed information by adding, updating, or deleting feeds directly from the command line.

Check [this](https://github.com/flare-foundation/ftso-v2-example-value-provider/blob/main/src/config/feeds.json) out for reference.

## Features

- Add new feeds with category, name, and sources.
- Update existing feeds, including changing their sources and category.
- Delete feeds by specifying their name.

## Requirements

- **Python 3.x**
- **Python Libraries**: No external libraries are required, as the script uses the standard Python libraries: `argparse` and `json`.

## Installation

### 1. Install Python

Make sure Python 3.x is installed on your machine. If you don't have it, follow the instructions below:

- **Windows**: Download and install Python from [here](https://www.python.org/downloads/).
- **Linux/macOS**: Python is usually pre-installed, but you can install it using your package manager. 
    - On Ubuntu:
      ```bash
      sudo apt-get install python3
      ```

### 2. Clone or Download the Script

You can clone the script using `git` or download it manually.

```bash
git clone https://github.com/ftso-eu/ftsofeedupdate
```

## Usage

### Running the Script

The script requires two mandatory arguments, the `source_file` (the path to the JSON file you want to modify) and the `destination_file` (where the updated JSON should be saved). Additionally, you can specify one of the following operations:

- `--add`: Adds a new feed to the JSON file.
- `--update`: Updates an existing feed's sources or category.
- `--delete`: Deletes a feed by its name.

### Command-Line Syntax

```bash
python script.py source_file destination_file [--add CATEGORY NAME SOURCES] [--update NAME NEW_SOURCES NEW_CATEGORY] [--delete NAME]
```

### Example Commands

1. **Add a New Feed**:
   ```bash
   python script.py feeds.json feeds_updated.json --add 1 "NEW/USD" '[{"exchange":"gateio","symbol":"NEW/USDT"},{"exchange":"kraken","symbol":"NEW/USD"},{"exchange":"mexc","symbol":"NEW/USDT"}]'
   ```
   This command adds a new feed with category `1`, name `"NEW_FEED/USD"`, and the specified sources.

2. **Update an Existing Feed**:
   ```bash
   python script.py feeds.json feeds_updated.json --update "NEW/USD" '[{"exchange":"nu-exchange","symbol":"NEW/USDT"},{"exchange":"kraken","symbol":"NEW/USD"},{"exchange":"mexc","symbol":"NEW/USDT"}]' 2
   ```
   This command updates the feed `"FLR/USD"` by modifying its sources and updating the category to `2`.

3. **Delete a Feed**:
   ```bash
   python script.py feeds.json feeds_updated.json --delete "NEW/USD"
   ```
   This command deletes the feed `"NEW/USD"` from the JSON file.

### Parameters

- **source_file**: Path to the source JSON file to be modified.
- **destination_file**: Path to save the updated JSON file.
- **--add**: Adds a new feed with the provided category, name, and sources. Example: `--add CATEGORY NAME SOURCES`
- **--update**: Updates the sources or category of an existing feed. Example: `--update NAME NEW_SOURCES NEW_CATEGORY`
- **--delete**: Deletes the feed by the specified name. Example: `--delete NAME`

### How It Works

1. **Loading the JSON**: The script loads the source JSON file into memory.
2. **Applying Modifications**: Based on the command provided, the script either adds, updates, or deletes the specified feed(s).
3. **Saving the Changes**: The updated data is saved into the destination file.

### Feed Structure

Each feed entry in the JSON contains:
- **Category**: An integer indicating the feed's category.
- **Name**: A string representing the feed's name.
- **Sources**: A list of sources, where each source includes an `exchange` and a `symbol`.

---

## License

This project is licensed under the MIT License.
