"""
Epub Manager - Quản lý sách điện tử
Xử lý tạo, sửa, xóa và convert sách
"""

import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import unicodedata

class EpubManager:
    def __init__(self, repo_path: str = None):
        """Initialize EpubManager"""
        self.repo_path = repo_path or self._find_repo_path()
        self.epubs_dir = os.path.join(self.repo_path, '_epubs')
        self.cache = {}
        self.load_books_cache()
    
    def _find_repo_path(self) -> str:
        """Tìm đường dẫn repository"""
        current_dir = os.getcwd()
        
        # Check if we're in Google Colab
        if '/content' in current_dir:
            # Look for cloned repo in Colab
            possible_paths = [
                '/content/SSGEpub',
                '/content/ssg-epub',
                current_dir
            ]
            for path in possible_paths:
                if os.path.exists(os.path.join(path, '_epubs')):
                    return path
        
        # Local development
        while current_dir != '/':
            if os.path.exists(os.path.join(current_dir, '_epubs')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        # Default fallback
        return os.getcwd()
    
    def load_books_cache(self):
        """Load books cache"""
        try:
            if os.path.exists(self.epubs_dir):
                self.cache = {}
                for filename in os.listdir(self.epubs_dir):
                    if filename.endswith('.md'):
                        filepath = os.path.join(self.epubs_dir, filename)
                        book_data = self._parse_markdown_file(filepath)
                        if book_data:
                            self.cache[filename] = book_data
        except Exception as e:
            print(f"Error loading books cache: {e}")
            self.cache = {}
    
    def _parse_markdown_file(self, filepath: str) -> Optional[Dict]:
        """Parse markdown file and extract frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    frontmatter['filename'] = os.path.basename(filepath)
                    frontmatter['content'] = parts[2].strip()
                    return frontmatter
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
        
        return None
    
    def get_all_books(self) -> List[Dict]:
        """Get all books"""
        return list(self.cache.values())
    
    def get_book_by_filename(self, filename: str) -> Optional[Dict]:
        """Get book by filename"""
        return self.cache.get(filename)
    
    def refresh_cache(self):
        """Refresh books cache"""
        self.load_books_cache()
    
    def create_filename(self, title: str) -> str:
        """Create filename from title"""
        # Remove Vietnamese accents and special characters
        filename = self._slugify(title)
        filename = f"{filename}.md"
        
        # Ensure unique filename
        counter = 1
        original_filename = filename
        while os.path.exists(os.path.join(self.epubs_dir, filename)):
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}-{counter}{ext}"
            counter += 1
        
        return filename
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        # Normalize unicode characters
        text = unicodedata.normalize('NFD', text)
        
        # Remove accents
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[-\s]+', '-', text)
        
        return text.strip('-')
    
    def generate_markdown(self, book_data: Dict) -> str:
        """Generate markdown content from book data"""
        # Prepare frontmatter
        frontmatter = {
            'layout': 'epub',
            'title': book_data['title'],
            'author': book_data['author'],
            'cover_image': book_data['cover_image'],
            'description': book_data['description']
        }
        
        # Add optional fields
        optional_fields = [
            'preview_image', 'isbn', 'published_date', 'genre', 
            'rating', 'pages', 'language', 'publisher', 'tags'
        ]
        
        for field in optional_fields:
            if field in book_data and book_data[field]:
                frontmatter[field] = book_data[field]
        
        # Add preview content if available
        if book_data.get('preview_content'):
            frontmatter['preview_content'] = book_data['preview_content']
        
        # Add download links
        if book_data.get('download_links'):
            frontmatter['download_links'] = []
            for link in book_data['download_links']:
                link_data = {
                    'platform': link['platform'],
                    'url': link['url'],
                    'index': link.get('index', 0)
                }
                if link.get('icon'):
                    link_data['icon'] = link['icon']
                frontmatter['download_links'].append(link_data)
        
        # Add download config URL if needed
        if book_data.get('download_config_url'):
            frontmatter['download_config_url'] = book_data['download_config_url']
        
        # Generate YAML frontmatter
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        
        # Generate full markdown
        markdown_content = f"""---
{yaml_content}---

Đây là trang chi tiết của cuốn sách "{{{{ page.title }}}}" của tác giả {{{{ page.author }}}}.
"""
        
        return markdown_content
    
    def create_book(self, book_data: Dict) -> str:
        """Create new book"""
        # Generate filename
        filename = self.create_filename(book_data['title'])
        filepath = os.path.join(self.epubs_dir, filename)
        
        # Generate markdown content
        markdown_content = self.generate_markdown(book_data)
        
        # Ensure directory exists
        os.makedirs(self.epubs_dir, exist_ok=True)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Update cache
        book_data['filename'] = filename
        self.cache[filename] = book_data
        
        return filename
    
    def update_book(self, filename: str, book_data: Dict) -> bool:
        """Update existing book"""
        try:
            filepath = os.path.join(self.epubs_dir, filename)
            
            if not os.path.exists(filepath):
                return False
            
            # Generate updated markdown content
            markdown_content = self.generate_markdown(book_data)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Update cache
            book_data['filename'] = filename
            self.cache[filename] = book_data
            
            return True
        except Exception as e:
            print(f"Error updating book {filename}: {e}")
            return False
    
    def delete_book(self, filename: str) -> bool:
        """Delete book"""
        try:
            filepath = os.path.join(self.epubs_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Remove from cache
            if filename in self.cache:
                del self.cache[filename]
            
            return True
        except Exception as e:
            print(f"Error deleting book {filename}: {e}")
            return False
    
    def extract_download_links(self, book_data: Dict) -> List[Dict]:
        """Extract download links from book data"""
        return book_data.get('download_links', [])
    
    def is_google_drive_link(self, url: str) -> bool:
        """Check if URL is Google Drive link"""
        return 'drive.google.com' in url or 'docs.google.com' in url
    
    def batch_convert_books(self, new_platform: Dict, only_google_drive: bool = True) -> Dict:
        """Convert all books to new platform"""
        from shortener_manager import ShortenerManager
        
        shortener = ShortenerManager()
        results = {
            'converted': 0,
            'errors': [],
            'skipped': 0
        }
        
        for filename, book_data in self.cache.items():
            try:
                download_links = self.extract_download_links(book_data)
                updated_links = []
                converted_any = False
                
                for link in download_links:
                    if only_google_drive and not self.is_google_drive_link(link['url']):
                        # Keep original link if not Google Drive and only_google_drive is True
                        updated_links.append(link)
                        continue
                    
                    try:
                        # Convert link using new platform
                        if self.is_google_drive_link(link['url']):
                            short_url = shortener.shorten_url(link['url'], new_platform)
                            updated_links.append({
                                'platform': new_platform['name'],
                                'url': short_url,
                                'index': new_platform['id'],
                                'icon': new_platform.get('icon', 'fas fa-download')
                            })
                            converted_any = True
                        else:
                            # For non-Google Drive links, keep original
                            updated_links.append(link)
                    except Exception as e:
                        results['errors'].append(f"{filename}: {str(e)}")
                        updated_links.append(link)  # Keep original on error
                
                if converted_any:
                    # Update book with new links
                    book_data['download_links'] = updated_links
                    if self.update_book(filename, book_data):
                        results['converted'] += 1
                    else:
                        results['errors'].append(f"{filename}: Failed to update file")
                else:
                    results['skipped'] += 1
                    
            except Exception as e:
                results['errors'].append(f"{filename}: {str(e)}")
        
        return results
    
    def get_book_statistics(self) -> Dict:
        """Get statistics about books"""
        books = self.get_all_books()
        
        stats = {
            'total_books': len(books),
            'authors': set(),
            'genres': set(),
            'languages': set(),
            'publishers': set(),
            'avg_rating': 0,
            'avg_pages': 0
        }
        
        total_rating = 0
        total_pages = 0
        rated_books = 0
        paged_books = 0
        
        for book in books:
            # Authors
            if book.get('author'):
                stats['authors'].add(book['author'])
            
            # Genres
            if book.get('genre'):
                if isinstance(book['genre'], list):
                    stats['genres'].update(book['genre'])
                else:
                    stats['genres'].add(book['genre'])
            
            # Languages
            if book.get('language'):
                stats['languages'].add(book['language'])
            
            # Publishers
            if book.get('publisher'):
                stats['publishers'].add(book['publisher'])
            
            # Rating
            if book.get('rating'):
                total_rating += float(book['rating'])
                rated_books += 1
            
            # Pages
            if book.get('pages'):
                total_pages += int(book['pages'])
                paged_books += 1
        
        # Calculate averages
        if rated_books > 0:
            stats['avg_rating'] = round(total_rating / rated_books, 2)
        
        if paged_books > 0:
            stats['avg_pages'] = round(total_pages / paged_books)
        
        # Convert sets to lists for JSON serialization
        stats['authors'] = list(stats['authors'])
        stats['genres'] = list(stats['genres'])
        stats['languages'] = list(stats['languages'])
        stats['publishers'] = list(stats['publishers'])
        
        return stats
