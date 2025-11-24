# WikiQuick

WikiQuick is a Python script designed to easily convert standard tabular CSV data into a format compatible with QuickStatements (QS) v1 commands, ensuring proper data normalization for various Wikidata data types.


## ⚙️ Usage

To start the application:

1. Clone this repository locally or copy the `main.py` file.
2. Execute the script based on your operating system:

| Platform | Command |
| --- | --- |
| Linux (Debian/Ubuntu) | `python3 main.py` |
| Windows | Double-click `main.py` | 
| macOS | `python3 main.py` |

3. A file dialog will open. Select your CSV file to process
4. The script performs automatic conversion. Upon successful completion, a new .tsv file (e.g., original_file_qs.tsv) containing the QuickStatements commands will be created in the same directory and automatically opened in your default text editor.


### Import Steps (QuickStatements)

1. Copy the content from the opened .tsv file
2. Navigate to the QuickStatements interface
3. Paste the content
4. Start the import selecting the "Import commands CSV V1" option



## 🗂️ Preparing Your CSV File (Header Mapping)

QuickStatements requires specific formatting (e.g., quotes for strings, specific date formats, prefixes for coordinates). To determine the correct normalization for a column, you must append a type suffix or use a specific prefix in your CSV header.


### Special Fields (Labels, Sitelinks, Qualifiers)

These fields use specific prefixes and formatting:

| Field | Type | Example Header | Example Value | Normalized Output |
| --- | --- | --- | --- | --- |
| Lxx |	Label (Multilingual) |	Len	| Hello world |	`Len,'Hello world'` |
| Dxx |	Description | Den |	Hello world | `Den,'Hello world'` |
| Axx |	Alias |	Afr | Hello world | `Afr,'Hello world'` |
| xxwiki |	Sitelink | frwiki |	Temple de Chêne-Bougeries |	`sitelink,frwiki,"Temple de Chêne-Bougeries"` |
| Sxx |	Qualifier |	S854 | `https://example.com` |


### Data Type Suffixes

The following suffixes must be appended to the property ID (e.g., P21) to trigger the correct data type formatting:

| Suffix | Type | Example Header | Example Value | Normalized Output |
| --- | --- | --- | --- | --- |
| | Item/Element | P31 | Q123 | Q123 |
| _STR | String Literal | P31_STR | Dante | "Dante" |
| _NUM | Number (Float) | P1082_NUM | "12,53" | 12.53 |
| _DATE |Datestamp | P569_DATE | 10-06-2024 | +2025-06-10T00:00:00Z/11 |
| _GEO | Geo Coordinates | P625_GEO | 45.466944/9.19 | @45.466944/9.19 |


### Important Note on Qualifiers

All qualifiers (Sxx) in a given CSV row are automatically attached to the first property (Pxx) encountered in that same row. If you have multiple properties in one row, only the first will carry the qualifiers.