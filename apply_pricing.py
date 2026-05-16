import re

# FIX SCRIPT.JS FIRST
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add dynamic service JS if not present
dynamic_js = """
// ==========================================
// DYNAMIC PRICING LOGIC
// ==========================================

function updateServicePrice(selectElem, rawName) {
    const selectedOption = selectElem.options[selectElem.selectedIndex];
    const price = selectedOption.getAttribute('data-price');
    
    // Update displayed price
    const container = selectElem.closest('.service-grid-item');
    if(container) {
        const priceDisplay = container.querySelector('.service-display-price');
        if(priceDisplay) priceDisplay.innerText = price;
    }
    
    // Resync counters because duration changed
    syncGridCounters();
}

function addDynamicService(btn, rawName) {
    const container = btn.closest('.service-grid-item');
    const selectElem = container.querySelector('.service-duration-select');
    
    let duration = '';
    let basePrice = 0;
    
    if(selectElem) {
        const selectedOption = selectElem.options[selectElem.selectedIndex];
        duration = selectedOption.value;
        basePrice = parseInt(selectedOption.getAttribute('data-price'));
    } else {
        // Fallback for any static items
        basePrice = parseInt(container.querySelector('.service-display-price').innerText);
    }
    
    const cleaningModeSuffix = currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)';
    const cartItemId = rawName + (duration ? " (" + duration + ")" : "") + cleaningModeSuffix;
    
    if (!cart[cartItemId]) {
        cart[cartItemId] = { rawName: rawName + (duration ? " (" + duration + ")" : ""), count: 1, price: basePrice, timeLimit: duration };
    } else {
        cart[cartItemId].count++;
    }
    
    if (typeof showToast === "function") showToast("Success", rawName + " (" + duration + ") added to cart!", true);
    else alert(rawName + " (" + duration + ") added to cart!");
    updateCartUI();
    syncGridCounters();
}

function updateCountFromDynamicGrid(btn, rawName, change) {
    const container = btn.closest('.service-grid-item');
    const selectElem = container.querySelector('.service-duration-select');
    
    let duration = '';
    if(selectElem) {
        duration = selectElem.options[selectElem.selectedIndex].value;
    }
    
    const cleaningModeSuffix = currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)';
    const cartItemId = rawName + (duration ? " (" + duration + ")" : "") + cleaningModeSuffix;
    
    if (cart[cartItemId]) {
        cart[cartItemId].count += change;
        if (cart[cartItemId].count <= 0) {
            delete cart[cartItemId];
        }
    }
    updateCartUI();
    syncGridCounters();
}
"""

if "function addDynamicService" not in js:
    # Find a good place to insert it. Before function updateCountFromGrid
    js = js.replace('function updateCountFromGrid', dynamic_js + '\nfunction updateCountFromGrid')
    
# Update syncGridCounters to read from select, if not completely correct yet.
# It seems syncGridCounters was partly updated but I should just overwrite it to be perfectly safe.
sync_replacement = """function syncGridCounters() {
    const gridItems = document.querySelectorAll('.service-grid-item');
    gridItems.forEach(item => {
        const rawName = item.getAttribute('data-name');
        const selectElem = item.querySelector('.service-duration-select');
        let duration = '';
        if(selectElem) {
            duration = selectElem.options[selectElem.selectedIndex].value;
        }
        
        const suffix = duration ? " (" + duration + ")" : "";
        const cartItemId = rawName + suffix + (currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)');
        
        const imgContainer = item.querySelector('.img-container');
        if(!imgContainer) return;
        
        const addBtn = imgContainer.querySelector('.add-btn-small');
        const counterPill = imgContainer.querySelector('.counter-pill-grid');
        
        if (cart[cartItemId] && cart[cartItemId].count > 0) {
            if(addBtn) addBtn.style.display = 'none';
            if(counterPill) {
                counterPill.style.display = 'flex';
                counterPill.querySelector('span').innerText = cart[cartItemId].count;
                // Update onclick for counter pill to use dynamic version
                const minusBtn = counterPill.querySelector('button:first-child');
                const plusBtn = counterPill.querySelector('button:last-child');
                if(minusBtn) minusBtn.setAttribute('onclick', `updateCountFromDynamicGrid(this, '${rawName}', -1)`);
                if(plusBtn) plusBtn.setAttribute('onclick', `updateCountFromDynamicGrid(this, '${rawName}', 1)`);
            }
        } else {
            if(addBtn) addBtn.style.display = 'flex';
            if(counterPill) counterPill.style.display = 'none';
        }
    });
}"""

js = re.sub(r'function syncGridCounters\(\) \{.*?(?=\n\}\n|\n\/\/)\n\}?', sync_replacement, js, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)


# FIX INDEX.HTML
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
    
    select_html = f'<select class="custom-select custom-select-sm mb-2 service-duration-select" style="font-size: 0.85rem; border-radius: 8px; width: 100%;" onchange="updateServicePrice(this, \'{name}\')">'
    for opt in item["options"]:
        select_html += f'<option value="{opt[0]}" data-price="{opt[1]}">{opt[0]}</option>'
    select_html += '</select>'
    
    # We want to replace the part between the </h6> and the </div> closing the content, 
    # replacing the <p>₹PRICE</p> and <button> with our select, dynamic price, and dynamic button.
    # The safest way is to find the entire <div class="service-grid-item"... data-name="Name">...</div> block
    
    block_pattern = r'(<div class="service-grid-item"[^>]*data-name="' + re.escape(name) + r'".*?<h6 class="mt-2 mb-1">.*?</h6>)(.*?)(<div class="counter-pill-grid".*?</div>\s*</div>)'
    
    def replacer(match):
        part1 = match.group(1)
        part3 = match.group(3)
        
        # We need to construct part2 which is the price and the add button
        # Removing old hardcoded stuff.
        new_part2 = f"""
                            {select_html}
                            <p class="text-muted mb-2 font-weight-bold" style="font-size: 1.1rem; color: #333 !important;">₹<span class="service-display-price">{base_price}</span></p>
                            <button class="add-btn-small" style="z-index: 10;" onclick="addDynamicService(this, '{name}')">+</button>
"""
        return part1 + new_part2 + part3

    html = re.sub(block_pattern, replacer, html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Pricing script executed.")
