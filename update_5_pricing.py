import re
import json

# Define the HTML updates for the 6 service items
html_replacements = [
    {
        "name": "Utensils Cleaning",
        "options": [
            ("30 min", 89),
            ("45 min", 129),
            ("60 min", 169),
            ("90 min", 239)
        ]
    },
    {
        "name": "Bathroom Cleaning",
        "options": [
            ("30 min", 89),
            ("45 min", 149),
            ("60 min", 189),
            ("90 min", 239)
        ]
    },
    {
        "name": "Mopping & Sweeping",
        "options": [
            ("30 min", 79),
            ("45 min", 119),
            ("60 min", 159),
            ("90 min", 219)
        ]
    },
    {
        "name": "Home Dusting",
        "options": [
            ("30 min", 79),
            ("45 min", 119),
            ("60 min", 159),
            ("90 min", 219)
        ]
    },
    {
        "name": "Fan Cleaning",
        "options": [
            ("1 unit", 49),
            ("2 unit", 98),
            ("3 unit", 147),
            ("4 unit", 196)
        ]
    },
    {
        "name": "Window Cleaning",
        "options": [
            ("1 unit", 49),
            ("2 unit", 98),
            ("3 unit", 147),
            ("4 unit", 196)
        ]
    }
]

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for item in html_replacements:
    name = item["name"]
    base_price = item["options"][0][1]
    
    # Create select HTML
    select_html = f'<select class="custom-select custom-select-sm mb-2 service-duration-select" style="font-size: 0.8rem; border-radius: 8px; width: 100%;" onchange="updateServicePrice(this, \'{name}\')">'
    for opt in item["options"]:
        select_html += f'<option value="{opt[0]}" data-price="{opt[1]}">{opt[0]}</option>'
    select_html += '</select>'
    
    # We want to replace the price text and onclick event.
    # We will use regex to find the service item block.
    # Match the block starting with data-name="{name}"
    pattern = r'(<div class="service-grid-item text-center"[^>]*data-name="' + re.escape(name) + r'".*?<div class="img-container".*?>.*?<h6 class="mt-2 mb-1">.*?</h6>).*?(<p class="text-muted mb-2 font-weight-bold".*?>)₹\d+(</p>).*?(<button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid\(this, \'.*?\', )\d+(, \'.*?\'\)".*?>\+</button>)'
    
    def replacer(match):
        part1 = match.group(1) # up to h6
        part2 = match.group(2) # <p class="...">
        part3 = match.group(3) # </p>
        part4 = match.group(4) # <button ... addFixedServiceFromGrid(this, 'name', 
        part5 = match.group(5) # , 'duration')">...</button>
        
        # Replace the price and insert the select dropdown before the price
        # Also remove the hardcoded price in the onclick, we will read it dynamically in JS
        
        # Actually, let's just make the addFixedServiceFromGrid not need basePrice and timeLimit passed in HTML,
        # it will read from the select directly.
        new_btn = f'<button class="add-btn-small" style="z-index: 10;" onclick="addDynamicService(this, \'{name}\')">+</button>'
        
        return f'{part1}\n{select_html}\n{part2}₹<span class="service-display-price">{base_price}</span>{part3}\n{new_btn}'
    
    html = re.sub(pattern, replacer, html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
# NOW SCRIPT.JS
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add dynamic service JS
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
    const cartItemId = rawName + " (" + duration + ")" + cleaningModeSuffix;
    
    if (!cart[cartItemId]) {
        cart[cartItemId] = { rawName: rawName + " (" + duration + ")", count: 1, price: basePrice, timeLimit: duration };
    } else {
        cart[cartItemId].count++;
    }
    
    if (typeof showToast === "function") showToast("Success", rawName + " (" + duration + ") added to cart!", true);
    else alert(rawName + " (" + duration + ") added to cart!");
    updateCartUI();
}

function updateCountFromDynamicGrid(btn, rawName, change) {
    const container = btn.closest('.service-grid-item');
    const selectElem = container.querySelector('.service-duration-select');
    
    let duration = '';
    if(selectElem) {
        duration = selectElem.options[selectElem.selectedIndex].value;
    }
    
    const cleaningModeSuffix = currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)';
    const cartItemId = rawName + " (" + duration + ")" + cleaningModeSuffix;
    
    if (cart[cartItemId]) {
        cart[cartItemId].count += change;
        if (cart[cartItemId].count <= 0) {
            delete cart[cartItemId];
        }
    }
    updateCartUI();
}
"""

js = js.replace('// GRID COUNTER LOGIC', dynamic_js + '\n// GRID COUNTER LOGIC')

# Update syncGridCounters to read from select
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

js = re.sub(r'function syncGridCounters\(\) \{.*?\n\}', sync_replacement, js, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Dynamic pricing updated.")
