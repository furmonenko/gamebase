# GameBase 🎮

A personal analytics system for exploring and analyzing video game data — inspired by Letterboxd, but for gamers.

## 👥 Team

| Member | Role | Status |
|--------|------|--------|
| **Zakharii Furmanets** | Data Engineer | ✅ **COMPLETED** |
| **Adam Pabianiak** | Data Analyst | 🔄 **READY TO START** |

---

## 📊 Project Status

### ✅ Data Engineering Pipeline (COMPLETED)
- [x] RAWG API data fetching
- [x] JSON → CSV transformation  
- [x] SQLite database schema & loading
- [x] End-to-end testing
- [x] Documentation

### 🔄 Data Analysis Phase (NEXT)
- [ ] Exploratory data analysis
- [ ] SQL queries & insights
- [ ] Data visualizations
- [ ] Final report & presentation

---

## 🚀 Quick Start for Adam

### 1. **First Time Setup**

#### Prerequisites
- Python 3.8+
- Git

#### Installation
```bash
# Clone repository
git clone https://github.com/yourname/gamebase.git
cd gamebase

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Get RAWG API Key
1. Go to https://rawg.io/apidocs
2. Register and get your free API key
3. Create `.env` file in project root:
```bash
RAWG_API_KEY=your_api_key_here
```

### 2. **Generate Data**

Since raw data is not stored in Git, you need to fetch it first:

```bash
# 1. Fetch raw data from API (takes ~30 seconds)
python src/fetch/fetch_games.py

# 2. Transform JSON to CSV
python src/transform/transform_to_csv.py

# 3. Create database schema
python src/database/database_schema.py

# 4. Load data into SQLite database
python src/database/load_csv_to_db.py

# 5. Test everything works
python src/test_pipeline.py
```

**Expected output:**
```
✅ Data fetch test PASSED: 3 files, 120 total games
✅ Data transform test PASSED
✅ Database schema test PASSED  
✅ Database loading test PASSED
✅ Data integrity test PASSED
🎉 ALL TESTS PASSED - Pipeline is working correctly!
```

### 3. **Start Analysis**

Your data is now ready! Check:
- Database: `db/games.db` (120 games)
- CSV files: `data/transformed/`
- Analysis guide: `ANALYST_GUIDE.md`

---

## 📁 Project Structure

```
gamebase/
├── src/
│   ├── fetch/              # 🔧 Data fetching (Zakharii)
│   │   └── fetch_games.py      # RAWG API data fetcher
│   ├── transform/          # 🔧 Data transformation (Zakharii)  
│   │   └── transform_to_csv.py # JSON to CSV converter
│   ├── database/           # 🔧 Database setup (Zakharii)
│   │   ├── database_schema.py  # SQLite schema creation
│   │   └── load_csv_to_db.py   # CSV to database loader
│   ├── analysis/           # 📊 Your analysis scripts (Adam)
│   │   └── README.md           # Analysis guidelines
│   └── test_pipeline.py    # 🧪 End-to-end testing
├── data/                   # 📁 Data files (not in Git)
│   ├── raw/               # JSON files from API
│   └── transformed/       # Clean CSV files
├── db/                    # 💾 Database (not in Git)
│   └── games.db          # SQLite database
├── results/               # 📈 Analysis outputs (not in Git)
│   ├── exports/          # Data exports
│   ├── charts/           # Visualizations  
│   └── reports/          # Final reports
├── notebooks/             # 📓 Jupyter notebooks (Adam)
├── docs/                  # 📚 Documentation
├── .env                   # 🔐 API keys (not in Git)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── ANALYST_GUIDE.md     # Detailed guide for Adam
└── project_plan.md      # Original project plan
```

---

## 🗄️ Available Data

### Database Tables
- **`games`** - Main game information (120 records)
  - Rating, release date, metacritic score, playtime
  - Categorized ratings and popularity
- **`genres`** - Game genres (17 unique)
- **`platforms`** - Gaming platforms (11 unique)
- **`stores`** - Digital stores (9 unique)
- **`tags`** - Game tags (182 unique)

### Relationship Tables
- **`game_genres`** - Games ↔ Genres (329 relationships)
- **`game_platforms`** - Games ↔ Platforms (525 relationships)  
- **`game_stores`** - Games ↔ Stores (383 relationships)
- **`game_tags`** - Games ↔ Tags (1162 relationships)
- **`game_ratings_detail`** - Detailed rating breakdown (480 records)

### CSV Files (Alternative Access)
All database tables are also available as CSV files in `data/transformed/`:
- `games.csv`, `game_genres.csv`, `platforms_lookup.csv`, etc.

---

## 🔍 How to Access Data

### Option 1: SQLite Database (Recommended)
```bash
# Open database  
sqlite3 db/games.db

# Example queries
.tables
SELECT name, rating, primary_genre FROM games ORDER BY rating DESC LIMIT 10;
SELECT genre_name, COUNT(*) FROM game_genres GROUP BY genre_name;
.quit
```

### Option 2: Python + Pandas
```python
import pandas as pd
import sqlite3

# From database
conn = sqlite3.connect('db/games.db')
games = pd.read_sql('SELECT * FROM games', conn)

# From CSV
games = pd.read_csv('data/transformed/games.csv')
```

### Option 3: External Tools
- **DB Browser for SQLite** - https://sqlitebrowser.org/
- **DBeaver** - Universal database tool
- **Any tool that supports SQLite**

---

## 📊 Sample Analysis Questions

### Basic Statistics
- What's the average game rating across all games?
- Which year had the most game releases?
- What are the most popular genres and platforms?
- Distribution of ESRB ratings?

### Advanced Analysis
- How do ratings correlate with metacritic scores?
- Rating trends over the years (2020-2024)
- Which platforms have the highest-rated games?
- Genre popularity by release year
- Most successful combinations (genre + platform)

### Visualizations to Create
- Rating distribution histogram
- Games by release year
- Genre popularity comparison
- Platform market share
- Rating vs Metacritic scatter plot
- Top 20 highest-rated games

---

## 🛠️ Development Workflow

### For Data Pipeline Updates (Zakharii)
```bash
# Modify fetching parameters if needed
vim src/fetch/fetch_games.py

# Re-run pipeline
python src/fetch/fetch_games.py
python src/transform/transform_to_csv.py  
python src/database/load_csv_to_db.py
python src/test_pipeline.py
```

### For Analysis Work (Adam)
```bash
# Start analysis
cd src/analysis/
python your_analysis_script.py

# Or use Jupyter
jupyter notebook

# Save results
# Charts → results/charts/
# Reports → results/reports/
# Data exports → results/exports/
```

---

## 🎯 Adam's Deliverables

Based on `project_plan.md`, your tasks:

### Phase 4: Analysis & Queries
- [ ] Define relevant analytical questions
- [ ] Write SQL queries to answer them  
- [ ] Export fixed tables to `/results/exports/`

### Phase 5: Visualization
- [ ] Create pivot tables (e.g. genre vs rating)
- [ ] Generate visualizations with plotly/seaborn
- [ ] (Optional) Connect Google Data Studio or Tableau

### Phase 7: Finalization  
- [ ] Write final report & documentation
- [ ] Create presentation (slides, charts, findings)

---

## 📚 Documentation

- **`ANALYST_GUIDE.md`** - Detailed guide for data analysis
- **`project_plan.md`** - Original project roadmap
- **`src/analysis/README.md`** - Analysis scripts guidelines
- **`results/reports/README.md`** - Report templates

---

## 🔧 Technical Details

### Dependencies
```txt
pandas>=2.1.4
requests>=2.31.0
python-dotenv>=1.0.0
sqlite3 (built-in)
matplotlib>=3.8.0
seaborn>=0.12.2
plotly>=5.17.0
jupyter>=1.0.0
```

### Data Pipeline Flow
```
RAWG API → JSON files → CSV files → SQLite database
    ↓          ↓           ↓            ↓
fetch_games.py → transform_to_csv.py → load_csv_to_db.py
```

### Testing
- Run `python src/test_pipeline.py` to verify data integrity
- Validates entire ETL pipeline end-to-end
- Checks for orphaned records and referential integrity

---

## 🆘 Troubleshooting

### Common Issues

**"No JSON files found"**
```bash
# Make sure you ran the fetcher first
python src/fetch/fetch_games.py
```

**"Database not found"**
```bash
# Create database schema first
python src/database/database_schema.py
```

**"API key error"**
```bash
# Check your .env file exists and has correct key
cat .env
```

**"Permission denied"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Getting Help
- **Data pipeline issues**: Contact Zakharii
- **API problems**: Check RAWG API documentation
- **Analysis questions**: See `ANALYST_GUIDE.md`

---

## 📞 Contact

- **Zakharii Furmanets** - Data Engineer (Pipeline & Infrastructure)
- **Adam Pabianiak** - Data Analyst (Analysis & Insights)

---

## 🚀 Ready to Start?

Adam, follow these steps:
1. ✅ Complete the "Quick Start" section above
2. ✅ Verify data is generated with `python src/test_pipeline.py`  
3. ✅ Read `ANALYST_GUIDE.md` for detailed analysis instructions
4. ✅ Start exploring the data!

Good luck with the analysis! 🎮📊