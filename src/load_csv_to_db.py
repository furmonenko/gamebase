import pandas as pd
import sqlite3
from pathlib import Path

class CSVToDatabaseLoader:
    def __init__(self):
        # Paths relative to src/ directory
        self.db_path = Path("../db/games.db")
        self.csv_dir = Path("../data/transformed")
        
        print(f"Looking for database at: {self.db_path.absolute()}")
        print(f"Looking for CSV files at: {self.csv_dir.absolute()}")
        
        if not self.db_path.exists():
            print("ERROR: Database not found. Run database_schema.py first.")
            return
        
        if not self.csv_dir.exists():
            print("ERROR: Transformed CSV directory not found. Run transform_to_csv.py first.")
            return
        
        print("✓ All paths found")
    
    def load_lookup_tables(self):
        """Load reference/lookup tables first"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Load genres
            genres_df = pd.read_csv(self.csv_dir / 'genres_lookup.csv')
            genres_df.to_sql('genres', conn, if_exists='replace', index=False)
            print(f"✓ genres: {len(genres_df)} records")
            
            # Load platforms
            platforms_df = pd.read_csv(self.csv_dir / 'platforms_lookup.csv')
            platforms_df.to_sql('platforms', conn, if_exists='replace', index=False)
            print(f"✓ platforms: {len(platforms_df)} records")
            
            # Load stores
            stores_df = pd.read_csv(self.csv_dir / 'stores_lookup.csv')
            stores_df.to_sql('stores', conn, if_exists='replace', index=False)
            print(f"✓ stores: {len(stores_df)} records")
            
            # Load tags (from game_tags.csv, get unique tags)
            tags_df = pd.read_csv(self.csv_dir / 'game_tags.csv')
            unique_tags = tags_df[['tag_id', 'tag_name', 'tag_slug', 'tag_language', 'tag_games_count']].drop_duplicates()
            unique_tags.columns = ['id', 'name', 'slug', 'language', 'games_count']
            unique_tags.to_sql('tags', conn, if_exists='replace', index=False)
            print(f"✓ tags: {len(unique_tags)} records")
            
        except Exception as e:
            print(f"ERROR loading lookup tables: {e}")
        finally:
            conn.close()
    
    def load_main_games_table(self):
        """Load the main games table"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            games_df = pd.read_csv(self.csv_dir / 'games.csv')
            
            # Handle NaN values - replace with None for SQL
            games_df = games_df.where(pd.notnull(games_df), None)
            
            games_df.to_sql('games', conn, if_exists='replace', index=False)
            print(f"✓ games: {len(games_df)} records")
            
        except Exception as e:
            print(f"ERROR loading games table: {e}")
        finally:
            conn.close()
    
    def load_junction_tables(self):
        """Load many-to-many relationship tables"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Load game_genres
            game_genres_df = pd.read_csv(self.csv_dir / 'game_genres.csv')
            game_genres_clean = game_genres_df[['game_id', 'genre_id']].dropna()
            game_genres_clean.to_sql('game_genres', conn, if_exists='replace', index=False)
            print(f"✓ game_genres: {len(game_genres_clean)} records")
            
            # Load game_platforms
            game_platforms_df = pd.read_csv(self.csv_dir / 'game_platforms.csv')
            game_platforms_clean = game_platforms_df[['game_id', 'platform_id']].dropna()
            game_platforms_clean.to_sql('game_platforms', conn, if_exists='replace', index=False)
            print(f"✓ game_platforms: {len(game_platforms_clean)} records")
            
            # Load game_stores
            game_stores_df = pd.read_csv(self.csv_dir / 'game_stores.csv')
            game_stores_clean = game_stores_df[['game_id', 'store_id']].dropna()
            game_stores_clean.to_sql('game_stores', conn, if_exists='replace', index=False)
            print(f"✓ game_stores: {len(game_stores_clean)} records")
            
            # Load game_tags
            game_tags_df = pd.read_csv(self.csv_dir / 'game_tags.csv')
            game_tags_clean = game_tags_df[['game_id', 'tag_id', 'tag_language']].dropna()
            game_tags_clean.to_sql('game_tags', conn, if_exists='replace', index=False)
            print(f"✓ game_tags: {len(game_tags_clean)} records")
            
        except Exception as e:
            print(f"ERROR loading junction tables: {e}")
        finally:
            conn.close()
    
    def load_ratings_detail(self):
        """Load detailed ratings breakdown"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            ratings_df = pd.read_csv(self.csv_dir / 'game_ratings_detail.csv')
            ratings_clean = ratings_df.dropna()
            ratings_clean.to_sql('game_ratings_detail', conn, if_exists='replace', index=False)
            print(f"✓ game_ratings_detail: {len(ratings_clean)} records")
            
        except Exception as e:
            print(f"ERROR loading ratings detail: {e}")
        finally:
            conn.close()
    
    def verify_data_integrity(self):
        """Verify that data was loaded correctly"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("\n=== DATA VERIFICATION ===")
        
        # Count records in each table
        tables = ['games', 'genres', 'platforms', 'stores', 'tags', 
                 'game_genres', 'game_platforms', 'game_stores', 
                 'game_tags', 'game_ratings_detail']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")
        
        # Check for referential integrity issues
        print("\n=== INTEGRITY CHECKS ===")
        
        # Check orphaned records in junction tables
        cursor.execute("""
            SELECT COUNT(*) FROM game_genres gg 
            LEFT JOIN games g ON gg.game_id = g.id 
            WHERE g.id IS NULL
        """)
        orphaned_game_genres = cursor.fetchone()[0]
        if orphaned_game_genres > 0:
            print(f"⚠️  {orphaned_game_genres} orphaned records in game_genres")
        else:
            print("✓ game_genres referential integrity OK")
        
        # Sample data check
        cursor.execute("SELECT name, rating, primary_genre FROM games LIMIT 5")
        sample_games = cursor.fetchall()
        print(f"\n=== SAMPLE DATA ===")
        for game in sample_games:
            print(f"- {game[0]} | Rating: {game[1]} | Genre: {game[2]}")
        
        conn.close()
    
    def run_full_load(self):
        """Run the complete CSV to database loading process"""
        print("Starting CSV to Database loading...")
        
        # Load in correct order (due to foreign key constraints)
        print("\n1. Loading lookup tables...")
        self.load_lookup_tables()
        
        print("\n2. Loading main games table...")
        self.load_main_games_table()
        
        print("\n3. Loading junction tables...")
        self.load_junction_tables()
        
        print("\n4. Loading ratings detail...")
        self.load_ratings_detail()
        
        print("\n5. Verifying data integrity...")
        self.verify_data_integrity()
        
        print("\n✅ Database loading completed successfully!")

if __name__ == "__main__":
    loader = CSVToDatabaseLoader()
    loader.run_full_load()