"""
Shortener Manager - Quản lý các platform rút gọn URL
Xử lý rút gọn URL và quản lý cấu hình platforms
"""

import os
import json
import requests
import subprocess
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

class ShortenerManager:
    def __init__(self, data_dir: str = None):
        """Initialize ShortenerManager"""
        self.data_dir = data_dir or os.path.join(os.getcwd(), 'admin_tool', 'data')
        self.platforms_file = os.path.join(self.data_dir, 'platforms.json')
        self.platforms = []
        self.load_platforms()
    
    def load_platforms(self):
        """Load platforms from file"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            
            if os.path.exists(self.platforms_file):
                with open(self.platforms_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.platforms = data.get('platforms', [])
            else:
                # Create default platforms
                self.platforms = self._get_default_platforms()
                self.save_platforms()
        except Exception as e:
            print(f"Error loading platforms: {e}")
            self.platforms = self._get_default_platforms()
    
    def save_platforms(self):
        """Save platforms to file"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            
            data = {
                'platforms': self.platforms,
                'last_updated': self._get_current_timestamp()
            }
            
            with open(self.platforms_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving platforms: {e}")
    
    def _get_default_platforms(self) -> List[Dict]:
        """Get default platform configurations"""
        return [
            {
                'id': 1,
                'name': 'TinyURL',
                'logo_url': 'https://tinyurl.com/app/themes/tinyurl/images/tinyurl-logo.svg',
                'api_endpoint': 'https://tinyurl.com/api-create.php',
                'curl_template': 'curl -X POST "https://tinyurl.com/api-create.php" -d "url=${link_download}"',
                'response_format': 'text',
                'response_path': '',
                'active': True,
                'icon': 'fas fa-link'
            },
            {
                'id': 2,
                'name': 'Is.gd',
                'logo_url': 'https://is.gd/images/logo.png',
                'api_endpoint': 'https://is.gd/create.php',
                'curl_template': 'curl -X POST "https://is.gd/create.php" -d "format=simple&url=${link_download}"',
                'response_format': 'text',
                'response_path': '',
                'active': True,
                'icon': 'fas fa-compress-alt'
            },
            {
                'id': 3,
                'name': 'V.gd',
                'logo_url': 'https://v.gd/images/logo.png',
                'api_endpoint': 'https://v.gd/create.php',
                'curl_template': 'curl -X POST "https://v.gd/create.php" -d "format=simple&url=${link_download}"',
                'response_format': 'text',
                'response_path': '',
                'active': True,
                'icon': 'fas fa-external-link-alt'
            }
        ]
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_platforms(self) -> List[Dict]:
        """Get all platforms"""
        return self.platforms
    
    def get_active_platforms(self) -> List[Dict]:
        """Get only active platforms"""
        return [p for p in self.platforms if p.get('active', True)]
    
    def get_platform_by_id(self, platform_id: int) -> Optional[Dict]:
        """Get platform by ID"""
        for platform in self.platforms:
            if platform['id'] == platform_id:
                return platform
        return None
    
    def add_platform(self, platform_data: Dict) -> Dict:
        """Add new platform"""
        # Generate new ID
        max_id = max([p['id'] for p in self.platforms], default=0)
        platform_data['id'] = max_id + 1
        
        # Validate required fields
        required_fields = ['name', 'api_endpoint', 'curl_template', 'response_format']
        for field in required_fields:
            if field not in platform_data or not platform_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Add default values
        platform_data.setdefault('active', True)
        platform_data.setdefault('icon', 'fas fa-link')
        platform_data.setdefault('logo_url', '')
        platform_data.setdefault('response_path', '')
        
        # Add to platforms list
        self.platforms.append(platform_data)
        self.save_platforms()
        
        return platform_data
    
    def update_platform(self, platform_id: int, platform_data: Dict) -> bool:
        """Update existing platform"""
        for i, platform in enumerate(self.platforms):
            if platform['id'] == platform_id:
                # Keep the original ID
                platform_data['id'] = platform_id
                self.platforms[i] = platform_data
                self.save_platforms()
                return True
        return False
    
    def delete_platform(self, platform_id: int) -> bool:
        """Delete platform"""
        for i, platform in enumerate(self.platforms):
            if platform['id'] == platform_id:
                del self.platforms[i]
                self.save_platforms()
                return True
        return False
    
    def shorten_url(self, long_url: str, platform_config: Dict) -> str:
        """Shorten URL using specified platform"""
        try:
            # Validate platform config
            if not platform_config or not platform_config.get('curl_template'):
                raise ValueError("Invalid platform configuration")
            
            # Replace variables in cURL template
            curl_command = platform_config['curl_template'].replace('${link_download}', long_url)
            
            # Add API key if needed (for platforms that require it)
            if '${api_key}' in curl_command:
                api_key = platform_config.get('api_key', '')
                if not api_key:
                    raise ValueError(f"API key required for {platform_config['name']}")
                curl_command = curl_command.replace('${api_key}', api_key)
            
            # Execute cURL command
            response = self._execute_curl(curl_command)
            
            # Parse response based on format
            short_url = self._parse_response(
                response,
                platform_config['response_format'],
                platform_config.get('response_path', '')
            )
            
            # Validate the shortened URL
            if not short_url or not self._is_valid_url(short_url):
                raise ValueError(f"Invalid response from {platform_config['name']}: {response}")
            
            return short_url.strip()
            
        except Exception as e:
            print(f"Error shortening URL with {platform_config.get('name', 'Unknown')}: {e}")
            # Return original URL as fallback
            return long_url
    
    def _execute_curl(self, curl_command: str) -> str:
        """Execute cURL command and return response"""
        try:
            # Parse cURL command to extract components
            if curl_command.startswith('curl '):
                # Use subprocess to execute curl
                result = subprocess.run(
                    curl_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    raise Exception(f"cURL failed: {result.stderr}")
            else:
                raise ValueError("Invalid cURL command")
                
        except subprocess.TimeoutExpired:
            raise Exception("Request timeout")
        except Exception as e:
            # Fallback to requests if cURL fails
            return self._fallback_request(curl_command)
    
    def _fallback_request(self, curl_command: str) -> str:
        """Fallback HTTP request using requests library"""
        try:
            # Simple parsing for basic POST requests
            if 'POST' in curl_command and '-d' in curl_command:
                # Extract URL
                url_match = re.search(r'"([^"]*)"', curl_command)
                if not url_match:
                    raise ValueError("Could not extract URL from cURL command")
                
                url = url_match.group(1)
                
                # Extract data
                data_match = re.search(r'-d\s+"([^"]*)"', curl_command)
                if data_match:
                    data_str = data_match.group(1)
                    # Parse form data
                    data = {}
                    for pair in data_str.split('&'):
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            data[key] = value
                    
                    response = requests.post(url, data=data, timeout=30)
                    response.raise_for_status()
                    return response.text
            
            raise ValueError("Unsupported cURL command format")
            
        except Exception as e:
            raise Exception(f"Fallback request failed: {e}")
    
    def _parse_response(self, response: str, format_type: str, path: str) -> str:
        """Parse response to extract short URL"""
        if format_type == 'text':
            # For text responses, return the response directly (after cleaning)
            return response.strip()
        
        elif format_type == 'json':
            try:
                import json
                data = json.loads(response)
                
                if not path:
                    # If no path specified, try common fields
                    common_fields = ['short_url', 'shortUrl', 'url', 'link', 'data']
                    for field in common_fields:
                        if field in data:
                            return str(data[field])
                    
                    # If it's a simple string response
                    if isinstance(data, str):
                        return data
                    
                    raise ValueError("Could not find short URL in JSON response")
                
                # Navigate JSON path: "data.short_url" -> data['data']['short_url']
                keys = path.split('.')
                current = data
                for key in keys:
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        raise ValueError(f"Path '{path}' not found in response")
                
                return str(current)
                
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON response")
        
        else:
            raise ValueError(f"Unsupported response format: {format_type}")
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return url_pattern.match(url) is not None
    
    def test_platform(self, platform_config: Dict, test_url: str = "https://www.google.com") -> Dict:
        """Test platform configuration"""
        result = {
            'success': False,
            'short_url': '',
            'error': '',
            'response_time': 0
        }
        
        try:
            import time
            start_time = time.time()
            
            short_url = self.shorten_url(test_url, platform_config)
            
            result['response_time'] = round(time.time() - start_time, 2)
            result['short_url'] = short_url
            result['success'] = short_url != test_url  # Success if URL was actually shortened
            
            if not result['success']:
                result['error'] = "URL was not shortened (returned original URL)"
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def get_platform_statistics(self) -> Dict:
        """Get statistics about platforms"""
        stats = {
            'total_platforms': len(self.platforms),
            'active_platforms': len(self.get_active_platforms()),
            'inactive_platforms': len([p for p in self.platforms if not p.get('active', True)]),
            'platforms_by_format': {},
            'platforms_list': []
        }
        
        # Count by response format
        for platform in self.platforms:
            format_type = platform.get('response_format', 'unknown')
            stats['platforms_by_format'][format_type] = stats['platforms_by_format'].get(format_type, 0) + 1
        
        # Platform details
        for platform in self.platforms:
            stats['platforms_list'].append({
                'id': platform['id'],
                'name': platform['name'],
                'active': platform.get('active', True),
                'format': platform.get('response_format', 'unknown')
            })
        
        return stats
