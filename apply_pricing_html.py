import re

html_replacements = [
    {
        "name": "Utensils Cleaning",
        "options": [("30 min", 89), ("45 min", 129), ("60 min", 169), ("90 min", 239)]
    },
    {
        "name": "Bathroom Cleaning",
        "options": [("30 min", 89), ("45 min", 149), ("60 min", 189), ("90 min", 239)]
    },
    {
        "name": "Mopping & Sweeping",
        "options": [("30 min", 79), ("45 min", 119), ("60 min", 159), ("90 min", 219)]
    },
    {
        "name": "Home Dusting",
        "options": [("30 min", 79), ("45 min", 119), ("60 min", 159), ("90 min", 219)]
    },
    {
        "name": "Fan Cleaning",
        "options": [("1 unit", 49), ("2 unit", 98), ("3 unit", 147), ("4 unit", 196)]
    },
    {
        "name": "Window Cleaning",
        "options": [("1 unit", 49), ("2 unit", 98), ("3 unit", 147), ("4 unit", 196)]
    }
]

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for item in html_replacements:
    name = item["name"]
    base_price = item["options"][0][1]
    
    select_html = f'<select class="custom-select custom-select-sm mb-1 mt-1 service-duration-select" style="font-size: 0.8rem; border-radius: 6px; width: 90%; text-align: center; margin: 0 auto; display: block;" onchange="updateServicePrice(this, \'{name}\')">'
    for opt in item["options"]:
        select_html += f'<option value="{opt[0]}" data-price="{opt[1]}">{opt[0]}</option>'
    select_html += '</select>'
    
    # regex to find the block
    pattern = r'(<div class="service-grid-item"[^>]*data-name="' + re.escape(name) + r'".*?)onclick="addFixedServiceFromGrid\(this,\s*\'[^\']+\',\s*\d+\)"(.*?onclick="updateCountFromGrid\(this,\s*\'[^\']+\',\s*-1\)")(.*?onclick="updateCountFromGrid\(this,\s*\'[^\']+\',\s*1\)")(.*?<h6 class="font-weight-bold mb-0"[^>]*>.*?</h6>)\s*<span class="font-weight-bold price-label"[^>]*>.*?</span>'
    
    def replacer(match):
        part1 = match.group(1) # up to before onclick=addFixedService...
        part2 = match.group(2) # up to before onclick=updateCount(-1)
        part3 = match.group(3) # up to before onclick=updateCount(1)
        part4 = match.group(4) # up to </h6>
        
        # reconstruct the block
        # the price span will be added after part4, along with the select
        
        res = part1 + f'onclick="addDynamicService(this, \'{name}\')"' + part2.replace('updateCountFromGrid(this', f'updateCountFromDynamicGrid(this, \'{name}\', -1)" dummy="')
        # Wait, part2 string matching captures the whole updateCountFromGrid... string.
        # Let's just do simple replacements within the entire service-grid-item block.
        return ""
    
    # Better approach: find the exact service-grid-item block using regex by matching until the next <div class="service-grid-item" or end of container.
    # Actually, let's just find the start of the item, and the closing </div> of the item.
    
    block_pattern = r'(<div class="service-grid-item"[^>]*data-name="' + re.escape(name) + r'".*?<h6[^>]*>.*?</h6>)\s*<span class="font-weight-bold price-label"[^>]*>.*?</span>'
    
    def block_replacer(m):
        block = m.group(1)
        # Fix the buttons inside this block
        block = re.sub(r'addFixedServiceFromGrid\(this,\s*\'[^\']+\',\s*\d+\)', f"addDynamicService(this, '{name}')", block)
        block = re.sub(r'updateCountFromGrid\(this,\s*\'[^\']+\',\s*-1\)', f"updateCountFromDynamicGrid(this, '{name}', -1)", block)
        block = re.sub(r'updateCountFromGrid\(this,\s*\'[^\']+\',\s*1\)', f"updateCountFromDynamicGrid(this, '{name}', 1)", block)
        
        # append select and new price span
        new_bottom = f'\n{select_html}\n<span class="font-weight-bold price-label service-display-price" style="color: #004aad; font-size: 0.95rem;">₹{base_price}</span>'
        
        return block + new_bottom

    html = re.sub(block_pattern, block_replacer, html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML pricing updated.")
