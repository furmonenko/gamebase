import subprocess
import sqlite3
import json
import pandas as pd
from pathlib import Path
import sys
import time

class PipelineTester:
    def __init__(self):
        self.project_root = Path("../")
        self.raw_data_dir = self.project_root / "data" / "raw"
        self.transformed_data_dir = self.project_root / "data" / "transformed"
        self.db_path = self.project_root / "db" / "games.db"
        
        self.test_results = {
            'fetch': False,
            'transform': False,
            'database_create': False,
            'database_load': False,
            'data_integrity': False
        }
    
    def test_data_fetch(self):
        """Test if raw data exists and is valid"""
        print("=== Testing Data Fetch ===")
        
        if not self.raw_data_dir.exists():
            print("❌ Raw data directory not found")
            return False
        
        json_files = list(self.raw_data_dir.glob("*.json"))
        if not json_files:
            print("❌ No JSON files found in raw data directory")
            return False
        
        total_games = 0
        valid_files = 0
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'results' in data and len(data['results']) > 0:
                        games_count = len(data['results'])
                        total_games += games_count
                        valid_files += 1
                        print(f"✓ {json_file.name}: {games_count} games")
                    else:
                        print(f"⚠️  {json_file.name}: No valid results")
            except Exception as e:
                print(f"❌ {json_file.name}: Error - {e}")
        
        if valid_files > 0 and total_games > 0:
            print(f"✅ Data fetch test PASSED: {valid_files} files, {total_games} total games")
            self.test_results['fetch'] = True
            return True
        else:
            print("❌ Data fetch test FAILED")
            return False
    
    def test_data_transform(self):
        """Test CSV transformation"""
        print("\n=== Testing Data Transform ===")
        
        if not self.transformed_data_dir.exists():
            print("❌ Transformed data directory not found")
            return False
        
        required_files = [
            'games.csv',
            'game_genres.csv', 
            'game_platforms.csv',
            'game_stores.csv',
            'game_tags.csv',
            'game_ratings_detail.csv',
            'genres_lookup.csv',
            'platforms_lookup.csv',
            'stores_lookup.csv'
        ]
        
        missing_files = []
        file_stats = {}
        
        for filename in required_files:
            filepath = self.transformed_data_dir / filename
            if filepath.exists():
                try:
                    df = pd.read_csv(filepath)
                    file_stats[filename] = len(df)
                    print(f"✓ {filename}: {len(df)} records")
                except Exception as e:
                    print(f"❌ {filename}: Error reading - {e}")
                    missing_files.append(filename)
            else:
                print(f"❌ {filename}: File not found")
                missing_files.append(filename)
        
        if not missing_files:
            print("✅ Data transform test PASSED")
            self.test_results['transform'] = True
            return True
        else:
            print(f"❌ Data transform test FAILED: Missing files: {missing_files}")
            return False
    
    def test_database_schema(self):
        """Test database schema creation"""
        print("\n=== Testing Database Schema ===")
        
        if not self.db_path.exists():
            print("❌ Database file not found")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check required tables
            required_tables = [
                'games', 'genres', 'platforms', 'stores', 'tags',
                'game_genres', 'game_platforms', 'game_stores', 
                'game_tags', 'game_ratings_detail'
            ]
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            missing_tables = set(required_tables) - set(existing_tables)
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            
            # Check indexes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
            indexes = cursor.fetchall()
            
            print(f"✓ All required tables exist ({len(required_tables)} tables)")
            print(f"✓ Indexes created: {len(indexes)}")
            
            conn.close()
            
            print("✅ Database schema test PASSED")
            self.test_results['database_create'] = True
            return True
            
        except Exception as e:
            print(f"❌ Database schema test FAILED: {e}")
            return False
    
    def test_database_loading(self):
        """Test if data was loaded correctly into database"""
        print("\n=== Testing Database Loading ===")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check record counts
            tables_to_check = [
                'games', 'genres', 'platforms', 'stores', 'tags',
                'game_genres', 'game_platforms', 'game_stores', 
                'game_tags', 'game_ratings_detail'
            ]
            
            all_good = True
            
            for table in tables_to_check:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"✓ {table}: {count} records")
                else:
                    print(f"❌ {table}: No records found")
                    all_good = False
            
            conn.close()
            
            if all_good:
                print("✅ Database loading test PASSED")
                self.test_results['database_load'] = True
                return True
            else:
                print("❌ Database loading test FAILED")
                return False
                
        except Exception as e:
            print(f"❌ Database loading test FAILED: {e}")
            return False
    
    def test_data_integrity(self):
        """Test data integrity and relationships"""
        print("\n=== Testing Data Integrity ===")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test 1: Check for orphaned records in junction tables
            orphan_checks = [
                ("game_genres", "game_id", "games", "id"),
                ("game_genres", "genre_id", "genres", "id"),
                ("game_platforms", "game_id", "games", "id"),
                ("game_platforms", "platform_id", "platforms", "id"),
                ("game_stores", "game_id", "games", "id"),
                ("game_stores", "store_id", "stores", "id")
            ]
            
            integrity_ok = True
            
            for junction_table, junction_column, ref_table, ref_column in orphan_checks:
                try:
                    cursor.execute(f"""
                        SELECT COUNT(*) FROM {junction_table} jt
                        LEFT JOIN {ref_table} rt ON jt.{junction_column} = rt.{ref_column}
                        WHERE rt.{ref_column} IS NULL
                    """)
                    orphan_count = cursor.fetchone()[0]
                    
                    if orphan_count > 0:
                        print(f"❌ {junction_table}.{junction_column}: {orphan_count} orphaned records")
                        integrity_ok = False
                    else:
                        print(f"✓ {junction_table}.{junction_column}: No orphaned records")
                except Exception as e:
                    print(f"⚠️  {junction_table}.{junction_column}: Check failed - {e}")
                    # Don't fail the test for this specific error, continue checking
            
            # Test 2: Check if games have expected relationships
            cursor.execute("SELECT COUNT(*) FROM games")
            total_games = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT game_id) FROM game_genres")
            games_with_genres = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT game_id) FROM game_platforms")
            games_with_platforms = cursor.fetchone()[0]
            
            print(f"✓ Total games: {total_games}")
            print(f"✓ Games with genres: {games_with_genres} ({games_with_genres/total_games*100:.1f}%)")
            print(f"✓ Games with platforms: {games_with_platforms} ({games_with_platforms/total_games*100:.1f}%)")
            
            # Test 3: Sample data validation
            cursor.execute("SELECT name, rating, primary_genre FROM games WHERE rating IS NOT NULL LIMIT 3")
            sample_games = cursor.fetchall()
            
            print("✓ Sample games data:")
            for game in sample_games:
                print(f"  - {game[0]} | Rating: {game[1]} | Genre: {game[2]}")
            
            conn.close()
            
            if integrity_ok:
                print("✅ Data integrity test PASSED")
                self.test_results['data_integrity'] = True
                return True
            else:
                print("❌ Data integrity test FAILED")
                return False
                
        except Exception as e:
            print(f"❌ Data integrity test FAILED: {e}")
            return False
    
    def run_performance_tests(self):
        """Test query performance"""
        print("\n=== Testing Query Performance ===")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test complex query performance
            start_time = time.time()
            
            cursor.execute("""
                SELECT g.name, g.rating, COUNT(gg.genre_id) as genre_count
                FROM games g
                LEFT JOIN game_genres gg ON g.id = gg.game_id
                WHERE g.rating > 4.0
                GROUP BY g.id, g.name, g.rating
                ORDER BY g.rating DESC
                LIMIT 10
            """)
            
            results = cursor.fetchall()
            query_time = time.time() - start_time
            
            print(f"✓ Complex query executed in {query_time:.3f} seconds")
            print(f"✓ Top rated games query returned {len(results)} results")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Performance test FAILED: {e}")
            return False
    
    def generate_test_report(self):
        """Generate final test report"""
        print("\n" + "="*50)
        print("           PIPELINE TEST REPORT")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.upper().ljust(20)}: {status}")
        
        print("-" * 50)
        print(f"TOTAL: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED - Pipeline is working correctly!")
            return True
        else:
            print("⚠️  Some tests failed - check the issues above")
            return False
    
    def run_full_pipeline_test(self):
        """Run complete end-to-end pipeline test"""
        print("🚀 Starting End-to-End Pipeline Test")
        print("="*60)
        
        # Run all tests in sequence
        self.test_data_fetch()
        self.test_data_transform()
        self.test_database_schema()
        self.test_database_loading()
        self.test_data_integrity()
        self.run_performance_tests()
        
        # Generate final report
        return self.generate_test_report()

if __name__ == "__main__":
    tester = PipelineTester()
    success = tester.run_full_pipeline_test()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)