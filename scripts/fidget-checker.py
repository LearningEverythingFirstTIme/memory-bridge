#!/usr/bin/env python3
"""
Fidget Toy Change Detector
Checks https://www.plantswakeyouup.com/collections/fidget-toys for new items
"""

import json
import os
import sys
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Config
URL = "https://www.plantswakeyouup.com/collections/fidget-toys"
STATE_FILE = Path("/root/.openclaw/workspace/.cache/fidget-state.json")

def fetch_page_with_retry(retries=3, delay=2):
    """Fetch the fidget toys page using curl with retries"""
    for attempt in range(retries):
        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "30", "-A", 
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
             URL],
            capture_output=True,
            text=True
        )
        
        html = result.stdout
        
        # Check if we got a valid page
        if html and len(html) > 5000 and "product" in html.lower():
            return html
        
        if attempt < retries - 1:
            time.sleep(delay)
    
    return None

def extract_products(html):
    """Extract product slugs from the page HTML"""
    products = set()
    
    # Look for product links: href="/products/product-slug"
    pattern = r'href="/products/([^"]+)"'
    matches = re.findall(pattern, html, re.IGNORECASE)
    
    for slug in matches:
        # Clean up the slug and remove duplicates
        clean_slug = slug.strip().lower()
        if clean_slug and len(clean_slug) > 3:
            products.add(clean_slug)
    
    return products

def load_previous_state():
    """Load the previous product list"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_state(products):
    """Save the current product list"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(sorted(list(products)), f, indent=2)

def main():
    try:
        # Fetch the page with retries
        html = fetch_page_with_retry()
        
        if html is None:
            # Silently fail - don't alert on temporary fetch issues
            sys.exit(0)
        
        # Extract current products
        current_products = extract_products(html)
        
        if not current_products:
            # No products found - might be a temporary issue, don't alert
            sys.exit(0)
        
        # Load previous state
        previous_products = load_previous_state()
        
        # Find new products
        new_products = current_products - previous_products
        
        # Save current state
        save_state(current_products)
        
        # Output results
        if new_products:
            print(f"🆕 New fidget toys detected at Plants Wake You Up!")
            print()
            for product in sorted(new_products):
                # Convert slug to readable name
                readable = product.replace('-', ' ').title()
                print(f"  • {readable}")
            print()
            print(f"Check them out: {URL}")
            sys.exit(0)
        else:
            # No changes - silent exit
            sys.exit(0)
            
    except Exception as e:
        # Silently fail on errors - don't spam with error messages
        sys.exit(0)

if __name__ == "__main__":
    main()
