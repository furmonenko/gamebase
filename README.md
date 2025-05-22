
# GameBase 🎮

A personal analytics system for exploring and analyzing video game data — inspired by Letterboxd, but for gamers.

## 📦 Features

- Fetch data from public APIs (e.g. RAWG.io)
- Store and transform using pandas + SQL
- Run queries for gaming insights
- Visualize results with Python or BI tools
- (Optional) Telegram bot and ML recommendations

---

## 🚀 Getting Started

### ✅ 1. Clone the repository

```bash
git clone https://github.com/yourname/gamebase.git
cd gamebase
```

### ✅ 2. Set up virtual environment

#### For macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

### ✅ 3. Install dependencies

```bash
pip install -r requirements.txt
```

### ✅ 4. Run the project

Start with scripts inside `src/`, e.g.:

```bash
python src/fetch/fetch_games.py
```

---

## 📁 Project Structure

```
gamebase/
├── src/
│   ├── fetch/
│   ├── transform/
├── data/
│   ├── raw/
│   ├── transformed/
├── db/
├── results/
│   └── exports/
├── notebooks/
├── bot/
├── reports/
├── venv/
├── README.md
├── requirements.txt
├── project_plan.md
```

---

## 👨‍💻 Authors

- [Zakharii Furmanets]
- [Adam Pabianiak]
