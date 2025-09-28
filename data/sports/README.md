# Sports Datasets

CSV files providing canonical teams per league with common fields for parsing and joining.

Schema (per row):
- league: normalized league code (e.g., basketball_nba)
- team_key: canonical snake_case key (e.g., boston_celtics)
- city: city/region (e.g., Boston)
- name: team nickname (e.g., Celtics)
- full_name: full display name (e.g., Boston Celtics)
- abbr: primary 2–4 letter abbreviation (e.g., BOS)
- aliases: pipe-delimited alternate names/phrases (e.g., celtics|boston celtics)
- conference: optional (e.g., East)
- division: optional (e.g., Atlantic)

Notes:
- Keep aliases lowercase, separated by `|`.
- Use one CSV per league for clarity and simpler diffs.
- Upstream sources: official league stats APIs (NBA/MLB/NHL), TheSportsDB, and curated entries.
