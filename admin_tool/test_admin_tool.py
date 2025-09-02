#!/usr/bin/env python3
"""
Test script for SSG Epub Admin Tool
Kiểm tra các chức năng chính của admin tool
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add admin_tool to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub_manager import EpubManager
from shortener_manager import ShortenerManager
from git_manager import GitManager

def test_epub_manager():
    """Test EpubManager functionality"""
    print("🧪 Testing EpubManager...")
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test _epubs directory
        epubs_dir = os.path.join(temp_dir, '_epubs')
        os.makedirs(epubs_dir)
        
        # Initialize manager
        manager = EpubManager(temp_dir)
        
        # Test book data
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'cover_image': 'https://example.com/cover.jpg',
            'description': 'This is a test book',
            'genre': ['Test', 'Fiction'],
            'rating': 4.5,
            'pages': 200,
            'language': 'Tiếng Việt',
            'publisher': 'Test Publisher',
            'download_links': [
                {
                    'platform': 'Test Platform',
                    'url': 'https://test.com/download',
                    'index': 1,
                    'icon': 'fas fa-download'
                }
            ]
        }
        
        try:
            # Test create book
            filename = manager.create_book(book_data)
            print(f"✅ Created book: {filename}")
            
            # Test get book
            retrieved_book = manager.get_book_by_filename(filename)
            assert retrieved_book is not None, "Book not found after creation"
            print("✅ Retrieved book successfully")
            
            # Test filename generation
            test_filename = manager.create_filename("Test Book with Special Characters!@#$%")
            assert test_filename.endswith('.md'), "Filename should end with .md"
            print(f"✅ Generated filename: {test_filename}")
            
            # Test markdown generation
            markdown = manager.generate_markdown(book_data)
            assert 'title: "Test Book"' in markdown, "Title not found in markdown"
            assert 'author: "Test Author"' in markdown, "Author not found in markdown"
            print("✅ Generated markdown successfully")
            
            # Test statistics
            stats = manager.get_book_statistics()
            assert stats['total_books'] >= 1, "Statistics should show at least 1 book"
            print(f"✅ Statistics: {stats['total_books']} books")
            
            print("✅ EpubManager tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ EpubManager test failed: {e}")
            return False

def test_shortener_manager():
    """Test ShortenerManager functionality"""
    print("\n🧪 Testing ShortenerManager...")
    
    try:
        # Create temporary data directory
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ShortenerManager(temp_dir)
            
            # Test get platforms
            platforms = manager.get_platforms()
            assert len(platforms) > 0, "Should have default platforms"
            print(f"✅ Found {len(platforms)} default platforms")
            
            # Test add platform
            new_platform = {
                'name': 'Test Platform',
                'api_endpoint': 'https://test.com/api',
                'curl_template': 'curl -X POST "https://test.com/api" -d "url=${link_download}"',
                'response_format': 'text',
                'response_path': '',
                'active': True
            }
            
            added_platform = manager.add_platform(new_platform)
            assert added_platform['id'] > 0, "Platform should have an ID"
            print(f"✅ Added platform with ID: {added_platform['id']}")
            
            # Test get platform by ID
            retrieved_platform = manager.get_platform_by_id(added_platform['id'])
            assert retrieved_platform is not None, "Platform not found after adding"
            assert retrieved_platform['name'] == 'Test Platform', "Platform name mismatch"
            print("✅ Retrieved platform by ID")
            
            # Test active platforms
            active_platforms = manager.get_active_platforms()
            assert len(active_platforms) > 0, "Should have active platforms"
            print(f"✅ Found {len(active_platforms)} active platforms")
            
            # Test URL validation
            valid_url = manager._is_valid_url('https://example.com')
            invalid_url = manager._is_valid_url('not-a-url')
            assert valid_url == True, "Valid URL should pass validation"
            assert invalid_url == False, "Invalid URL should fail validation"
            print("✅ URL validation works")
            
            # Test statistics
            stats = manager.get_platform_statistics()
            assert stats['total_platforms'] > 0, "Should have platforms in statistics"
            print(f"✅ Statistics: {stats['total_platforms']} total platforms")
            
            print("✅ ShortenerManager tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ ShortenerManager test failed: {e}")
        return False

def test_git_manager():
    """Test GitManager functionality"""
    print("\n🧪 Testing GitManager...")
    
    try:
        # Create temporary git repository
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize git repo
            os.system(f'cd {temp_dir} && git init')
            
            manager = GitManager(temp_dir)
            
            # Test repository status
            status = manager.get_repo_status()
            print(f"✅ Got repository status: {status.get('current_branch', 'unknown')}")
            
            # Test git configuration
            result = manager.configure_git("Test User", "test@example.com")
            assert result == True, "Git configuration should succeed"
            print("✅ Git configuration successful")
            
            # Create a test file
            test_file = os.path.join(temp_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('Test content')
            
            # Test add file
            result = manager.add_file('test.txt')
            assert result == True, "Adding file should succeed"
            print("✅ Added file to git")
            
            # Test commit
            result = manager.commit('Test commit')
            assert result == True, "Commit should succeed"
            print("✅ Committed changes")
            
            print("✅ GitManager tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ GitManager test failed: {e}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing Integration...")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Setup test environment
            epubs_dir = os.path.join(temp_dir, '_epubs')
            os.makedirs(epubs_dir)
            
            # Initialize managers
            epub_manager = EpubManager(temp_dir)
            shortener_manager = ShortenerManager(os.path.join(temp_dir, 'data'))
            
            # Test workflow: create book with platform
            platforms = shortener_manager.get_active_platforms()
            assert len(platforms) > 0, "Need at least one platform for integration test"
            
            selected_platform = platforms[0]
            
            book_data = {
                'title': 'Integration Test Book',
                'author': 'Test Author',
                'cover_image': 'https://example.com/cover.jpg',
                'description': 'Integration test book',
                'download_links': [
                    {
                        'platform': selected_platform['name'],
                        'url': 'https://example.com/download',
                        'index': selected_platform['id'],
                        'icon': selected_platform.get('icon', 'fas fa-download')
                    }
                ]
            }
            
            # Create book
            filename = epub_manager.create_book(book_data)
            print(f"✅ Created integration test book: {filename}")
            
            # Verify file exists
            filepath = os.path.join(epubs_dir, filename)
            assert os.path.exists(filepath), "Book file should exist"
            
            # Read and verify content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'Integration Test Book' in content, "Book title should be in file"
                assert selected_platform['name'] in content, "Platform name should be in file"
            
            print("✅ Integration test passed!")
            return True
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🎯 SSG Epub Admin Tool - Test Suite")
    print("=" * 50)
    
    tests = [
        ("EpubManager", test_epub_manager),
        ("ShortenerManager", test_shortener_manager),
        ("GitManager", test_git_manager),
        ("Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Admin tool is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
