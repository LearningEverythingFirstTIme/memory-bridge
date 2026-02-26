#!/usr/bin/env python3
"""
Fidget Toy Change Detector
Checks plantswakeyouup.com for new fidget toys and reports changes.
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: requests and beautifulsoup4 required")
    print("Install: pip install requests beautifulsoup4")
    sys.exit(1)

# Config
URL = "https://www.plantswakeyouup.com/collections/fidget-toys"
SNAPSHOT_FILE = Path("/root/.openclaw/workspace/memory/fidget-snapshot.json")

def fetch_products():
    """Fetch and extract product data from the page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        return None, f"Failed to fetch page: {e}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract products - Shopify stores typically have product cards
    products = []
    
    # Try multiple selectors for product cards
    selectors = [
        '.product-card',
        '.product-item',
        '.grid__item',
        '[data-product]',
        '.product',
        '.card-wrapper',
    ]
    
    product_elements = []
    for selector in selectors:
        product_elements = soup.select(selector)
        if product_elements:
            break
    
    # If no specific selectors work, look for links containing /products/
    if not product_elements:
        all_links = soup.find_all('a', href=True)
        product_links = [a for a in all_links if '/products/' in a['href']]
        # Get parent containers
        seen = set()
        for link in product_links:
            parent = link.find_parent(['div', 'li', 'article'])
            if parent and parent not in seen:
                seen.add(parent)
                product_elements.append(parent)
    
    for elem in product_elements:
        product = {}
        
        # Try to find title
        title_elem = elem.select_one('.product-title, .card__title, h2, h3, .product__title, a[href*="/products/"]')
        if title_elem:
            product['title'] = title_elem.get_text(strip=True)
        
        # Try to find price
        price_elem = elem.select_one('.price, .product-price, .money, [data-price]')
        if price_elem:
            product['price'] = price_elem.get_text(strip=True)
        
        # Try to find URL
        link_elem = elem.select_one('a[href*="/products/"]')
        if link_elem:
            href = link_elem.get('href', '')
            if href.startswith('/'):
                href = f"https://www.plantswakeyouup.com{href}"
            product['url'] = href
        
        # Try to find image
        img_elem = elem.select_one('img')
        if img_elem:
            product['image'] = img_elem.get('src', img_elem.get('data-src', ''))
        
        if product.get('title'):
            products.append(product)
    
    # Also try to extract from JSON-LD if present
    json_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Product':
                products.append({
                    'title': data.get('name', ''),
                    'price': data.get('offers', {}).get('price', ''),
                    'url': data.get('url', ''),
                })
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'Product':
                        products.append({
                            'title': item.get('name', ''),
                            'price': item.get('offers', {}).get('price', ''),
                            'url': item.get('url', ''),
                        })
        except (json.JSONDecodeError, AttributeError, KeyError):
            pass
    
    # Remove duplicates by title
    seen_titles = set()
    unique_products = []
    for p in products:
        title = p.get('title', '').lower().strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_products.append(p)
    
    return unique_products, None

def load_snapshot():
    """Load the previous snapshot from disk."""
    if not SNAPSHOT_FILE.exists():
        return None
    
    try:
        with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load snapshot: {e}")
        return None

def save_snapshot(products):
    """Save the current product list to disk."""
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'url': URL,
        'products': products,
        'count': len(products)
    }
    
    try:
        with open(SNAPSHOT_FILE, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2)
    except Exception as e:
        print(f"Error: Could not save snapshot: {e}")
        sys.exit(1)

def detect_changes(current, previous):
    """Compare current and previous product lists."""
    if not previous:
        return {
            'is_first_run': True,
            'added': current,
            'removed': [],
            'changed': [],
            'total_current': len(current),
            'total_previous': 0
        }
    
    prev_products = {p.get('title', '').lower().strip(): p for p in previous.get('products', [])}
    curr_products = {p.get('title', '').lower().strip(): p for p in current}
    
    added = []
    removed = []
    changed = []
    
    # Find added products
    for title, product in curr_products.items():
        if title not in prev_products:
            added.append(product)
    
    # Find removed products
    for title, product in prev_products.items():
        if title not in curr_products:
            removed.append(product)
    
    # Find price changes
    for title, curr_product in curr_products.items():
        if title in prev_products:
            prev_price = prev_products[title].get('price', '')
            curr_price = curr_product.get('price', '')
            if prev_price and curr_price and prev_price != curr_price:
                changed.append({
                    'title': curr_product.get('title'),
                    'old_price': prev_price,
                    'new_price': curr_price,
                    'url': curr_product.get('url', '')
                })
    
    return {
        'is_first_run': False,
        'added': added,
        'removed': removed,
        'changed': changed,
        'total_current': len(current),
        'total_previous': len(prev_products)
    }

def format_discord_message(changes):
    """Format the changes for Discord notification."""
    lines = ["🧸 **Fidget Toy Update Detected!**"]
    lines.append(f"<{URL}>")
    lines.append("")
    
    if changes.get('is_first_run'):
        lines.append(f"📊 **Initial scan complete:** Found {changes['total_current']} products")
        lines.append("Future checks will detect new items, removals, and price changes.")
        return "\n".join(lines)
    
    has_changes = changes['added'] or changes['removed'] or changes['changed']
    
    if not has_changes:
        return None  # No notification needed
    
    if changes['added']:
        lines.append(f"✨ **{len(changes['added'])} New Product(s):**")
        for p in changes['added'][:5]:  # Limit to 5
            price = f" - {p.get('price', '')}" if p.get('price') else ""
            lines.append(f"• {p.get('title', 'Unknown')}{price}")
        if len(changes['added']) > 5:
            lines.append(f"_...and {len(changes['added']) - 5} more_")
        lines.append("")
    
    if changes['removed']:
        lines.append(f"🗑️ **{len(changes['removed'])} Removed:**")
        for p in changes['removed'][:3]:
            lines.append(f"• ~~{p.get('title', 'Unknown')}~~")
        lines.append("")
    
    if changes['changed']:
        lines.append(f"💰 **{len(changes['changed'])} Price Change(s):**")
        for c in changes['changed'][:3]:
            lines.append(f"• {c['title']}: {c['old_price']} → {c['new_price']}")
        lines.append("")
    
    lines.append(f"📊 Total products: {changes['total_previous']} → {changes['total_current']}")
    
    return "\n".join(lines)

def main():
    print(f"[{datetime.now().isoformat()}] Checking {URL}...")
    
    # Fetch current products
    current_products, error = fetch_products()
    
    if error:
        print(f"Error: {error}")
        # Don't exit with error - cron shouldn't spam on temporary failures
        sys.exit(0)
    
    print(f"Found {len(current_products)} products")
    
    # Load previous snapshot
    previous = load_snapshot()
    
    # Detect changes
    changes = detect_changes(current_products, previous)
    
    # Format message
    message = format_discord_message(changes)
    
    # Save current snapshot
    save_snapshot(current_products)
    
    # Output result
    if message:
        print(message)
        # Also write to a file that the cron job can read
        result_file = Path("/root/.openclaw/workspace/memory/fidget-result.txt")
        result_file.write_text(message)
        sys.exit(0)  # Success with notification
    else:
        print("No changes detected - no notification needed")
        sys.exit(0)  # Success, no notification

if __name__ == "__main__":
    main()
