import re

# UPDATE INDEX.HTML
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Deep Clean Coming Soon Placeholder
placeholder = """
            <div id="deepCleanPlaceholder" class="text-center py-5" style="display: none; background: #fcfdfe; border-radius: 12px; border: 1px dashed #c2e0ff; margin-bottom: 20px;">
                <i class="fas fa-sparkles mb-3" style="font-size: 50px; color: var(--primary);"></i>
                <h4 class="font-weight-bold" style="color: var(--primary-dark);">Deep Clean Services</h4>
                <p class="text-muted">Our premium deep clean packages are launching very soon. Stay tuned!</p>
            </div>
"""
# If not already present, insert it before service grid
if 'id="deepCleanPlaceholder"' not in html:
    html = re.sub(r'(<div class="service-grid d-flex")', placeholder + r'\1', html)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# UPDATE SCRIPT.JS
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace setCleaningMode function
new_set_cleaning_mode = """function setCleaningMode(mode) {
    currentCleaningMode = mode;
    
    // Update button styles
    const buttons = document.querySelectorAll('.cleaning-mode-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.innerText.toLowerCase().includes(mode)) {
            btn.classList.add('active');
        }
    });

    const grid = document.querySelector('.service-grid');
    const placeholder = document.getElementById('deepCleanPlaceholder');

    if (mode === 'deep') {
        if(grid) grid.style.display = 'none';
        if(placeholder) placeholder.style.display = 'block';
    } else {
        if(grid) grid.style.display = 'flex';
        if(placeholder) placeholder.style.display = 'none';
        if(typeof syncGridCounters === 'function') syncGridCounters();
    }
}"""

js = re.sub(r'function setCleaningMode\(mode\) \{.*?(?=\n\}|\nfunction|\n//)\n\}?', new_set_cleaning_mode, js, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Deep Clean updated.")
