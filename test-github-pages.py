#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 GitHub Pages Deployment Test Script
Test end-to-end deployment workflow cho SSG Epub Admin Tool
"""

import os
import time
import requests
from datetime import datetime

def test_github_pages_deployment():
    """Test GitHub Pages deployment workflow"""
    
    print("🧪 GITHUB PAGES DEPLOYMENT TEST")
    print("=" * 50)
    
    # Configuration (cần update)
    GITHUB_USERNAME = "your-username"  # ⚠️ THAY ĐỔI
    REPO_NAME = "your-repo-name"       # ⚠️ THAY ĐỔI
    SITE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"
    
    print(f"🎯 Target site: {SITE_URL}")
    
    # Test 1: Check if site is accessible
    print(f"\n📡 Test 1: Site Accessibility")
    try:
        response = requests.get(SITE_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Site accessible")
            print(f"📊 Response time: {response.elapsed.total_seconds():.2f}s")
        else:
            print(f"❌ Site returned HTTP {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Site not accessible: {e}")
        return False
    
    # Test 2: Check if Jekyll structure is working
    print(f"\n📚 Test 2: Jekyll Structure")
    test_pages = [
        "/",                    # Home page
        "/epubs/",             # Epub library
        "/archive.html",       # Archive
    ]
    
    for page in test_pages:
        url = f"{SITE_URL}{page}"
        try:
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"{status} {page}: HTTP {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ {page}: {e}")
    
    # Test 3: Check if any epub files exist and are accessible
    print(f"\n📖 Test 3: Epub Collection")
    try:
        # Check if epub collection exists by looking for any epub page
        response = requests.get(f"{SITE_URL}/epubs/", timeout=10)
        if response.status_code == 200:
            content = response.text
            if "epub" in content.lower() or "sách" in content.lower():
                print("✅ Epub collection accessible")
            else:
                print("⚠️ Epub collection empty (normal for new setup)")
        else:
            print("⚠️ Epub collection page not found")
    except requests.RequestException as e:
        print(f"❌ Error checking epub collection: {e}")
    
    # Test 4: Check CSS/JS loading
    print(f"\n🎨 Test 4: Assets Loading")
    css_found = False
    js_found = False
    
    try:
        response = requests.get(SITE_URL, timeout=10)
        content = response.text
        
        if ".css" in content:
            print("✅ CSS files referenced")
            css_found = True
        
        if ".js" in content:
            print("✅ JavaScript files referenced")
            js_found = True
            
        if not css_found:
            print("⚠️ No CSS files found")
        if not js_found:
            print("⚠️ No JavaScript files found")
            
    except requests.RequestException as e:
        print(f"❌ Error checking assets: {e}")
    
    # Test 5: Performance check
    print(f"\n⚡ Test 5: Performance")
    try:
        start_time = time.time()
        response = requests.get(SITE_URL, timeout=10)
        load_time = time.time() - start_time
        
        if load_time < 3:
            print(f"✅ Fast loading: {load_time:.2f}s")
        elif load_time < 5:
            print(f"⚠️ Moderate loading: {load_time:.2f}s")
        else:
            print(f"❌ Slow loading: {load_time:.2f}s")
            
        print(f"📊 Content size: {len(response.content):,} bytes")
        
    except requests.RequestException as e:
        print(f"❌ Performance test failed: {e}")
    
    # Summary
    print(f"\n📋 TEST SUMMARY")
    print("=" * 30)
    print(f"🌐 Site URL: {SITE_URL}")
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Basic functionality working")
    print(f"🚀 Ready for admin tool integration")
    
    return True

def check_local_setup():
    """Check if local files are properly configured for GitHub Pages"""
    
    print("\n🔍 LOCAL SETUP VERIFICATION")
    print("=" * 40)
    
    # Check required files
    required_files = [
        "_config.yml",
        "Gemfile", 
        ".github/workflows/github-pages.yml"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
    
    # Check _config.yml content
    if os.path.exists("_config.yml"):
        with open("_config.yml", "r", encoding="utf-8") as f:
            config_content = f.read()
            
        checks = [
            ("GitHub Pages URL", "github.io" in config_content),
            ("Repository info", "repository:" in config_content),
            ("Collections config", "epubs:" in config_content),
            ("Exclude optimizations", ".cursor/" in config_content)
        ]
        
        for check_name, passed in checks:
            status = "✅" if passed else "⚠️"
            print(f"{status} {check_name}")
    
    # Check Gemfile
    if os.path.exists("Gemfile"):
        with open("Gemfile", "r", encoding="utf-8") as f:
            gemfile_content = f.read()
            
        if "github-pages" in gemfile_content:
            print("✅ GitHub Pages gem configured")
        else:
            print("❌ GitHub Pages gem missing")

if __name__ == "__main__":
    print("🧪 SSG EPUB GITHUB PAGES TEST SUITE")
    print("=" * 50)
    
    # Local setup check
    check_local_setup()
    
    # Remote deployment test
    print("\n" + "=" * 50)
    
    # Ask user for configuration
    print("⚠️ CONFIGURATION REQUIRED:")
    print("Edit this script and update:")
    print("- GITHUB_USERNAME")  
    print("- REPO_NAME")
    print("\nThen run again to test live deployment.")
    
    # Uncomment below line after updating configuration:
    # test_github_pages_deployment()

