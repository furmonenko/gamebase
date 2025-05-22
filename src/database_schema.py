import sqlite3
from pathlib import Path

class GameDatabaseSchema:
    def __init__(self, db_path="../db/games.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def create_schema(self):
        """Create the complete database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Main games table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT UNIQUE,
                released DATE,
                rating REAL,
                rating_top INTEGER,
                ratings_count INTEGER,
                metacritic INTEGER,
                playtime INTEGER,
                suggestions_count INTEGER,
                updated DATETIME,
                background_image TEXT,
                reviews_count INTEGER,
                added INTEGER,
                tba BOOLEAN,
                release_year INTEGER,
                release_month INTEGER,
                release_day INTEGER,
                rating_category TEXT CHECK (rating_category IN ('Excellent', 'Great', 'Good', 'Average', 'Poor')),
                popularity_category TEXT CHECK (popularity_category IN ('Very Popular', 'Popular', 'Moderately Popular', 'Niche')),
                esrb_rating TEXT,
                esrb_rating_slug TEXT,
                genres_count INTEGER DEFAULT 0,
                platforms_count INTEGER DEFAULT 0,
                stores_count INTEGER DEFAULT 0,
                primary_genre TEXT,
                primary_genre_slug TEXT,
                primary_platform TEXT,
                primary_platform_slug TEXT
            )
        ''')
        
        # Genres lookup table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Platforms lookup table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platforms (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Stores lookup table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Tags lookup table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                language TEXT,
                games_count INTEGER DEFAULT 0,
                UNIQUE(id, language)
            )
        ''')
        
        # Game-Genre junction table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_genres (
                game_id INTEGER,
                genre_id INTEGER,
                PRIMARY KEY (game_id, genre_id),
                FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
            )
        ''')
        
        # Game-Platform junction table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_platforms (
                game_id INTEGER,
                platform_id INTEGER,
                PRIMARY KEY (game_id, platform_id),
                FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
                FOREIGN KEY (platform_id) REFERENCES platforms(id) ON DELETE CASCADE
            )
        ''')
        
        # Game-Store junction table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stores (
                game_id INTEGER,
                store_id INTEGER,
                PRIMARY KEY (game_id, store_id),
                FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
                FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE
            )
        ''')
        
        # Game-Tag junction table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_tags (
                game_id INTEGER,
                tag_id INTEGER,
                tag_language TEXT,
                PRIMARY KEY (game_id, tag_id, tag_language),
                FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id, tag_language) REFERENCES tags(id, language) ON DELETE CASCADE
            )
        ''')
        
        # Game ratings detail table (one-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_ratings_detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                rating_id INTEGER,
                rating_title TEXT CHECK (rating_title IN ('exceptional', 'recommended', 'meh', 'skip')),
                rating_count INTEGER DEFAULT 0,
                rating_percent REAL DEFAULT 0.0,
                FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
                UNIQUE(game_id, rating_id)
            )
        ''')
        
        # Create indexes for better performance
        self.create_indexes(cursor)
        
        conn.commit()
        conn.close()
        
        print("✓ Database schema created successfully")
        print(f"✓ Database location: {self.db_path}")
    
    def create_indexes(self, cursor):
        """Create indexes for better query performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_games_rating ON games(rating)",
            "CREATE INDEX IF NOT EXISTS idx_games_release_year ON games(release_year)",
            "CREATE INDEX IF NOT EXISTS idx_games_ratings_count ON games(ratings_count)",
            "CREATE INDEX IF NOT EXISTS idx_games_metacritic ON games(metacritic)",
            "CREATE INDEX IF NOT EXISTS idx_games_rating_category ON games(rating_category)",
            "CREATE INDEX IF NOT EXISTS idx_games_popularity_category ON games(popularity_category)",
            "CREATE INDEX IF NOT EXISTS idx_game_genres_game_id ON game_genres(game_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_genres_genre_id ON game_genres(genre_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_platforms_game_id ON game_platforms(game_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_platforms_platform_id ON game_platforms(platform_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_stores_game_id ON game_stores(game_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_stores_store_id ON game_stores(store_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_tags_game_id ON game_tags(game_id)",
            "CREATE INDEX IF NOT EXISTS idx_game_tags_tag_id ON game_tags(tag_id)",
            "CREATE INDEX IF NOT EXISTS idx_ratings_detail_game_id ON game_ratings_detail(game_id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
    
    def show_schema_info(self):
        """Display information about the created schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n=== DATABASE SCHEMA INFO ===")
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, name, data_type, not_null, default, primary_key = col
                pk_marker = " (PK)" if primary_key else ""
                null_marker = " NOT NULL" if not_null else ""
                default_marker = f" DEFAULT {default}" if default else ""
                print(f"  - {name}: {data_type}{pk_marker}{null_marker}{default_marker}")
        
        conn.close()
    
    def validate_schema(self):
        """Validate that the schema was created correctly"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        required_tables = [
            'games', 'genres', 'platforms', 'stores', 'tags',
            'game_genres', 'game_platforms', 'game_stores', 
            'game_tags', 'game_ratings_detail'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = set(required_tables) - set(existing_tables)
        
        if missing_tables:
            print(f"✗ Missing tables: {missing_tables}")
            return False
        else:
            print("✓ All required tables exist")
            return True
        
        conn.close()

if __name__ == "__main__":
    schema = GameDatabaseSchema()
    schema.create_schema()
    schema.validate_schema()
    schema.show_schema_info()