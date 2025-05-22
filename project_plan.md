
# Project Plan – GameBase: Personal Gaming Analytics & Discovery Tool

## 🧠 Project Summary

A two-person team is developing a small analytical system that collects, processes, stores, and visualizes video game data. The system is similar to Letterboxd, but for games. Data will be fetched from public APIs, transformed, analyzed, and optionally enhanced with a Telegram bot or ML features.

---

## 👥 Team Roles

| Member | Role | Responsibilities |
|--------|------|------------------|
| ZAKHARII (Z) | Data Engineer | API fetching, data transformation, database schema, ETL, optional: Telegram bot |
| ADAM (A) | Data Analyst | SQL queries, data analysis, visualization, reporting, documentation |

---

## ✅ Task List

### Phase 1: Project Setup & Planning

- [ ] Create Git repository and folder structure
- [ ] Define API(s) to use (e.g. RAWG.io)
- [ ] Assign tasks and responsibilities
- [ ] Set up virtual environment and requirements.txt

### Phase 2: Data Loading

- [ ] Write script to fetch game data from API (Z)
- [ ] Save JSON responses to `/data/raw/` (Z)
- [ ] Optionally, implement periodic data fetching (e.g. cron job) (Z)

### Phase 3: Data Transformation

- [ ] Clean and normalize data using pandas (Z)
- [ ] Extract year/month from release date (Z)
- [ ] Classify ratings and popularity (Z)
- [ ] Design SQL database schema (Z)
- [ ] Load transformed data into SQLite/PostgreSQL (Z)

### Phase 4: Analysis & Queries

- [ ] Define relevant analytical questions (A)
- [ ] Write SQL queries to answer them (A)
- [ ] Export fixed tables to `/results/exports/` (A)

### Phase 5: Visualization

- [ ] Create pivot tables (e.g. genre vs rating) (A)
- [ ] Generate visualizations with plotly / seaborn (A)
- [ ] (Optional) Connect Google Data Studio or Tableau (A)

### Phase 6: Optional Features

- [ ] Implement basic Telegram bot to show new releases or user favorites (Z)
- [ ] Add basic recommendation logic (ML: clustering, content-based filtering) (A)

### Phase 7: Finalization

- [ ] Write final report & documentation (A)
- [ ] Clean up repository (remove unnecessary files) (Z)
- [ ] Test scripts and database loading end-to-end (Both)
- [ ] Create presentation (slides, charts, findings) (A)

---

## 📆 Timeline Suggestion (10 Days)

| Day | Task |
|-----|------|
| 1 | Setup project, assign roles, research API |
| 2–3 | Fetch + store raw data |
| 4 | Transform data + load into DB |
| 5–6 | Write SQL queries, analyze trends |
| 7 | Visualizations |
| 8 | (Optional) Bot or ML |
| 9 | Final checks, testing |
| 10 | Report + submit project |

