
# JSON Feed Modification Script

This Python script allows users to modify JSON feed data by adding, updating, or removing sources with specific base pairs (`USD` or `USDT`) for different exchange groups.

## Features

- **Add Sources with Specific Base Pairs**: Add sources for exchanges with either `USD` or `USDT` pairs only, based on user-specified groups.
- **Avoid Duplicates**: Ensures no duplicate entries and no conflicting pairs (e.g., an exchange won't have both `USD` and `USDT` for the same asset).
- **Selective Updates**: Allows updates for all pairs in a specified category or a single specified pair.

## Requirements

- **Python 3.x**
- **Python Libraries**: Uses the standard Python libraries: `argparse` and `json`.

## Usage

### Command-Line Arguments

| Argument         | Description                                                                                               |
|------------------|-----------------------------------------------------------------------------------------------------------|
| `--category`     | The category of feeds to update.                                                                          |
| `--exchange-pairs` | Specify exchange groups and base pairs (e.g., `exchange1 exchange2 USD`). Multiple groups can be specified.|
| `--source-file`  | Path to the source JSON file to be modified.                                                              |
| `--dest-file`    | Path to save the updated JSON file.                                                                       |
| `--all`          | Update all pairs in the specified category.                                                               |
| `--pair`         | Update only a specific pair (e.g., `BTC`) instead of all.                                                 |

### Examples

1. **Update All Pairs with USD and USDT Separately**:
   ```bash
   python3 ftsofeedupdate.py --category 1 --all    --exchange-pairs bitstamp coinbase kraken USD    --exchange-pairs bybit gate binance USDT    --source-file feeds.json --dest-file updated_feeds.json
   ```
   - This command updates all pairs in category `1`, adding only `USD` pairs for `bitstamp`, `coinbase`, `kraken`, and only `USDT` pairs for `bybit`, `gate`, and `binance`.

2. **Update a Specific Pair (e.g., BTC)**:
   ```bash
   python3 ftsofeedupdate.py --category 1 --pair BTC    --exchange-pairs bitstamp coinbase kraken USD    --exchange-pairs bybit gate binance USDT    --source-file feeds.json --dest-file updated_feeds.json
   ```
   - This command updates only the `BTC` pair in category `1`, assigning `USD` pairs for `bitstamp`, `coinbase`, `kraken` and `USDT` pairs for `bybit`, `gate`, and `binance`.

### How It Works

1. **Loading the JSON**: Loads the source JSON file into memory.
2. **Applying Modifications**:
   - Adds the specified `USD` and `USDT` pairs exclusively to the designated exchanges.
   - Removes any conflicting entries (e.g., if an exchange has both `USD` and `USDT` for the same asset, the conflicting pair is removed).
3. **Saving the Changes**: Writes the modified JSON data to the destination file.

---

## License

This project is licensed under the MIT License.
