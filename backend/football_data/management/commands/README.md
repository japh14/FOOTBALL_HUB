# ⚽ Player Data Seeder Command

This command is a Django management utility used to populate the `Player` model in the database by fetching player information from the **API-Football** service.


## 🚀 How to Run the Command

The command is executed using `python manage.py <command_name>`. Assuming the file containing the `Command` class is named `seed_players.py`, the command name is **`seed_players`**.

### Basic Usage

Run the command without any arguments to use the default settings configured in `APIFootballClient` and the command definitions.

```bash
python manage.py seed_players
```

### Example 1: Seeding Specific Leagues

Specify a list of league IDs to focus the data fetch:

```bash
python manage.py seed_players --league_ids 39 140 78
```

  * **Result:** Seeds players for League IDs 39 (e.g., Premier League), 140 (e.g., La Liga), and 78 (e.g., Bundesliga) using the **default season (2023)** and **default max page (2)**.

### Example 2: Seeding a Historical Season

Specify both the league ID and a past season:

```bash
python manage.py seed_players --league_ids 61 --season 2021
```

  * **Result:** Seeds players for League ID 61 (e.g., Ligue 1) specifically for the **2021** season.

### Example 3: Increasing API Pages

Increase the maximum number of pages to retrieve for the paginated API call to ensure you get more data:

```bash
python manage.py seed_players --league_ids 39 --max_page 5
```

  * **Result:** Seeds players for League ID 39, retrieving data up to **Page 5** of the API response.

-----

## ⚙️ Argument Reference

| Argument | Requirement | Type | Default Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`--league_ids`** | Optional | Integer List | `client.league_ids` | A space-separated list of league IDs to retrieve player data from. |
| **`--season`** | Optional | Integer | `2023` | The specific year/season to fetch player data for. |
| **`--max_page`** | Optional | Integer | `2` | The maximum page number to iterate through during the paginated API call for players. |


<br>

-----

# 🏟️ Team Data Seeder Command

This command is a Django management utility that populates the **`Team`** model in the database by fetching team information from the **API-Football** service.


## 🚀 How to Run the Command

The command is executed using `python manage.py seed_teams`. Since the `--league_ids` argument is optional, you can run it with defaults or specify which leagues to target.

### Basic Usage (Using Client Defaults)

If you omit the `--league_ids` flag, the command will use the default league IDs defined within your `APIFootballClient` class.

```bash
python manage.py seed_teams
```

  * **Result:** Seeds teams for the leagues defined by `client.league_ids`.

### Example: Seeding Specific Leagues

Provide a space-separated list of league IDs to focus the data fetch:

```bash
python manage.py seed_teams --league_ids 39 135 140
```

  * **Result:** Seeds teams specifically for League IDs 39 (e.g., Premier League), 135 (e.g., Brazilian Série A), and 140 (e.g., La Liga).

-----

## ⚙️ Argument Reference

| Argument | Requirement | Type | Default Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`--league_ids`** | Optional | Integer List | `client.league_ids` | A space-separated list of league primary keys (IDs) to retrieve team data from. If omitted, the client's internal list of default IDs is used. |

-----

## ⚠️ Important Notes

  * **Data Integrity Check:** The command explicitly checks for the existence of **`Country`** and **`League`** records before creating a team. If a team's country or league ID is not found, that team record will be **skipped**, and an error message will be printed to the console.
  * **Idempotency:** The command uses `Team.objects.get_or_create()`, which makes it **idempotent**. This means you can run the command multiple times without duplicating data; it will create new teams but simply report that existing teams already exist.


<br>

-----

# 🏆 League and Country Data Seeder Command

This command is a Django management utility used to populate the **`League`** and **`Country`** models in the database by fetching data from the **API-Football** service.


## 🚀 How to Run the Command

The command requires **no arguments**. It retrieves the complete list of available leagues and their associated countries from the API and processes them.

### Basic Usage

Execute the command directly from your project's root directory:

```bash
python manage.py seed_leagues
```

  * **Result:** The command will make a request to the API, then iterate through the data, creating or updating records for both the `Country` models.

-----

## 💡 Command Behavior

This command is designed to be **idempotent**, meaning you can run it multiple times without creating duplicate data.

### 1\. Data Source

The command queries the primary `/leagues` endpoint of the API-Football service.

### 2\. Country Creation

The command first processes the country data linked to each league:

  * If a **Country Code** is provided by the API, it uses that code to check if the country already exists or creates a new `Country` record.
  * If the code is missing, it attempts to find an existing country based only on the **Country Name**.

### 3\. League Creation

  * The command uses **`League.objects.get_or_create()`** to ensure the league is unique, using the API's unique league `id` as the lookup key.
  * Existing leagues will be reported as "already exists." New leagues will be marked as "Created."


<br>

-----

# 🌍 Country Data Seeder Command

This command is a Django management utility used to populate the **`Country`** model in the database by fetching country data from the **API-Football** service.


## 🚀 How to Run the Command

The command requires **no arguments**. It retrieves the complete list of countries and their details from the API-Football `/countries` endpoint.

### Basic Usage

Execute the command directly from your project's root directory:

```bash
python manage.py seed_countries
```

  * **Result:** The command will make a request to the API, then iterate through the data, creating or updating `Country` records based on the unique country code.

-----

## 💡 Command Behavior

This command is designed to be **idempotent**, meaning you can run it multiple times without creating duplicate data.