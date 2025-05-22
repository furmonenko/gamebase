import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class GameDataToCSV:
    def __init__(self):
        self.raw_data_dir = Path("../../data/raw")
        self.transformed_data_dir = Path("../../data/transformed")
        self.transformed_data_dir.mkdir(parents=True, exist_ok=True)
        
    def load_raw_data(self):
        """Load all JSON files from raw data directory"""
        all_games = []
        
        # Look for all JSON files in raw data directory
        json_files = list(self.raw_data_dir.glob("*.json"))
        
        if not json_files:
            print(f"ERROR: No JSON files found in {self.raw_data_dir}")
            return all_games
        
        print(f"Found {len(json_files)} JSON files")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'results' in data:
                        games_count = len(data['results'])
                        all_games.extend(data['results'])
                        print(f"✓ {json_file.name}: {games_count} games")
                    else:
                        print(f"✗ {json_file.name}: No 'results' key found")
            except Exception as e:
                print(f"✗ {json_file.name}: ERROR - {e}")
        
        if not all_games:
            print("ERROR: No games loaded from any file")
        else:
            print(f"Total games loaded: {len(all_games)}")
        
        return all_games
    
    def transform_main_games_data(self, raw_games):
        """Transform main game information"""
        games_data = []
        
        for game in raw_games:
            # Basic game info
            game_record = {
                'id': game.get('id'),
                'name': game.get('name'),
                'slug': game.get('slug'),
                'released': game.get('released'),
                'rating': game.get('rating'),
                'rating_top': game.get('rating_top'),
                'ratings_count': game.get('ratings_count'),
                'metacritic': game.get('metacritic'),
                'playtime': game.get('playtime'),
                'suggestions_count': game.get('suggestions_count'),
                'updated': game.get('updated'),
                'background_image': game.get('background_image'),
                'reviews_count': game.get('reviews_count'),
                'added': game.get('added'),
                'tba': game.get('tba')
            }
            
            # Extract release year and month
            if game.get('released'):
                try:
                    release_date = datetime.strptime(game['released'], '%Y-%m-%d')
                    game_record['release_year'] = release_date.year
                    game_record['release_month'] = release_date.month
                    game_record['release_day'] = release_date.day
                except ValueError:
                    game_record['release_year'] = None
                    game_record['release_month'] = None
                    game_record['release_day'] = None
            else:
                game_record['release_year'] = None
                game_record['release_month'] = None
                game_record['release_day'] = None
            
            # Rating categories
            rating = game.get('rating', 0)
            if rating >= 4.5:
                game_record['rating_category'] = 'Excellent'
            elif rating >= 4.0:
                game_record['rating_category'] = 'Great'
            elif rating >= 3.5:
                game_record['rating_category'] = 'Good'
            elif rating >= 3.0:
                game_record['rating_category'] = 'Average'
            else:
                game_record['rating_category'] = 'Poor'
            
            # Popularity based on ratings_count
            ratings_count = game.get('ratings_count', 0)
            if ratings_count >= 10000:
                game_record['popularity_category'] = 'Very Popular'
            elif ratings_count >= 1000:
                game_record['popularity_category'] = 'Popular'
            elif ratings_count >= 100:
                game_record['popularity_category'] = 'Moderately Popular'
            else:
                game_record['popularity_category'] = 'Niche'
            
            # ESRB rating
            if game.get('esrb_rating'):
                game_record['esrb_rating'] = game['esrb_rating'].get('name')
                game_record['esrb_rating_slug'] = game['esrb_rating'].get('slug')
            else:
                game_record['esrb_rating'] = None
                game_record['esrb_rating_slug'] = None
            
            # Count genres and platforms
            game_record['genres_count'] = len(game.get('genres', []))
            game_record['platforms_count'] = len(game.get('platforms', []))
            game_record['stores_count'] = len(game.get('stores', []))
            
            # Extract first genre and platform (most common)
            if game.get('genres'):
                game_record['primary_genre'] = game['genres'][0]['name']
                game_record['primary_genre_slug'] = game['genres'][0]['slug']
            else:
                game_record['primary_genre'] = None
                game_record['primary_genre_slug'] = None
            
            if game.get('platforms'):
                game_record['primary_platform'] = game['platforms'][0]['platform']['name']
                game_record['primary_platform_slug'] = game['platforms'][0]['platform']['slug']
            else:
                game_record['primary_platform'] = None
                game_record['primary_platform_slug'] = None
            
            games_data.append(game_record)
        
        return pd.DataFrame(games_data)
    
    def extract_genres(self, raw_games):
        """Extract all genres with game relationships"""
        genre_game_relationships = []
        
        for game in raw_games:
            game_id = game.get('id')
            for genre in game.get('genres', []):
                genre_game_relationships.append({
                    'game_id': game_id,
                    'genre_id': genre.get('id'),
                    'genre_name': genre.get('name'),
                    'genre_slug': genre.get('slug')
                })
        
        return pd.DataFrame(genre_game_relationships)
    
    def extract_platforms(self, raw_games):
        """Extract all platforms with game relationships"""
        platform_game_relationships = []
        
        for game in raw_games:
            game_id = game.get('id')
            for platform_data in game.get('platforms', []):
                platform = platform_data.get('platform', {})
                platform_game_relationships.append({
                    'game_id': game_id,
                    'platform_id': platform.get('id'),
                    'platform_name': platform.get('name'),
                    'platform_slug': platform.get('slug')
                })
        
        return pd.DataFrame(platform_game_relationships)
    
    def extract_stores(self, raw_games):
        """Extract all stores with game relationships"""
        store_game_relationships = []
        
        for game in raw_games:
            game_id = game.get('id')
            for store_data in game.get('stores', []):
                store = store_data.get('store', {})
                store_game_relationships.append({
                    'game_id': game_id,
                    'store_id': store.get('id'),
                    'store_name': store.get('name'),
                    'store_slug': store.get('slug')
                })
        
        return pd.DataFrame(store_game_relationships)
    
    def extract_ratings_breakdown(self, raw_games):
        """Extract detailed ratings breakdown"""
        ratings_data = []
        
        for game in raw_games:
            game_id = game.get('id')
            for rating in game.get('ratings', []):
                ratings_data.append({
                    'game_id': game_id,
                    'rating_id': rating.get('id'),
                    'rating_title': rating.get('title'),
                    'rating_count': rating.get('count'),
                    'rating_percent': rating.get('percent')
                })
        
        return pd.DataFrame(ratings_data)
    
    def extract_tags(self, raw_games):
        """Extract top tags for each game"""
        tag_game_relationships = []
        
        for game in raw_games:
            game_id = game.get('id')
            # Get top 10 tags to avoid too much data
            for tag in game.get('tags', [])[:10]:
                tag_game_relationships.append({
                    'game_id': game_id,
                    'tag_id': tag.get('id'),
                    'tag_name': tag.get('name'),
                    'tag_slug': tag.get('slug'),
                    'tag_language': tag.get('language'),
                    'tag_games_count': tag.get('games_count')
                })
        
        return pd.DataFrame(tag_game_relationships)
    
    def run_transformation(self):
        """Run the complete transformation to CSV"""
        print("Starting transformation...")
        
        # Load raw data
        raw_games = self.load_raw_data()
        
        if not raw_games:
            print("ERROR: No data to transform")
            return
        
        try:
            # Transform data
            games_df = self.transform_main_games_data(raw_games)
            games_df.to_csv(self.transformed_data_dir / 'games.csv', index=False, encoding='utf-8')
            print(f"✓ games.csv: {len(games_df)} records")
            
            genres_df = self.extract_genres(raw_games)
            genres_df.to_csv(self.transformed_data_dir / 'game_genres.csv', index=False, encoding='utf-8')
            print(f"✓ game_genres.csv: {len(genres_df)} records")
            
            platforms_df = self.extract_platforms(raw_games)
            platforms_df.to_csv(self.transformed_data_dir / 'game_platforms.csv', index=False, encoding='utf-8')
            print(f"✓ game_platforms.csv: {len(platforms_df)} records")
            
            stores_df = self.extract_stores(raw_games)
            stores_df.to_csv(self.transformed_data_dir / 'game_stores.csv', index=False, encoding='utf-8')
            print(f"✓ game_stores.csv: {len(stores_df)} records")
            
            ratings_df = self.extract_ratings_breakdown(raw_games)
            ratings_df.to_csv(self.transformed_data_dir / 'game_ratings_detail.csv', index=False, encoding='utf-8')
            print(f"✓ game_ratings_detail.csv: {len(ratings_df)} records")
            
            tags_df = self.extract_tags(raw_games)
            tags_df.to_csv(self.transformed_data_dir / 'game_tags.csv', index=False, encoding='utf-8')
            print(f"✓ game_tags.csv: {len(tags_df)} records")
            
            # Create unique lookup tables
            unique_genres = genres_df[['genre_id', 'genre_name', 'genre_slug']].drop_duplicates()
            unique_genres.to_csv(self.transformed_data_dir / 'genres_lookup.csv', index=False, encoding='utf-8')
            print(f"✓ genres_lookup.csv: {len(unique_genres)} records")
            
            unique_platforms = platforms_df[['platform_id', 'platform_name', 'platform_slug']].drop_duplicates()
            unique_platforms.to_csv(self.transformed_data_dir / 'platforms_lookup.csv', index=False, encoding='utf-8')
            print(f"✓ platforms_lookup.csv: {len(unique_platforms)} records")
            
            unique_stores = stores_df[['store_id', 'store_name', 'store_slug']].drop_duplicates()
            unique_stores.to_csv(self.transformed_data_dir / 'stores_lookup.csv', index=False, encoding='utf-8')
            print(f"✓ stores_lookup.csv: {len(unique_stores)} records")
            
            print(f"SUCCESS: All files saved to {self.transformed_data_dir}")
            
            return {
                'games': games_df,
                'genres': genres_df,
                'platforms': platforms_df,
                'stores': stores_df,
                'ratings': ratings_df,
                'tags': tags_df
            }
            
        except Exception as e:
            print(f"ERROR during transformation: {e}")
            return None

if __name__ == "__main__":
    transformer = GameDataToCSV()
    transformer.run_transformation()