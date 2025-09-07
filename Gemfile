source "https://rubygems.org"

# 🚀 GitHub Pages gem - Essential cho deployment
gem "github-pages", group: :jekyll_plugins

# Jekyll plugins supported by GitHub Pages
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-paginate"
  gem "jekyll-sitemap"
  gem "jemoji"
end

# Windows and JRuby support
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# 🔧 Ruby 3.4 Compatibility Fixes
gem "bigdecimal", "~> 3.1"    # Required for Ruby 3.4+
gem "webrick", "~> 1.8"       # Required for Jekyll local server

# Lock the version of Listen and related tools
gem "listen", "~> 3.3"
