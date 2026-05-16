import re

# UPDATE INDEX.HTML
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change Cleaning Mode font
html = html.replace('<h5 class="font-weight-bold mb-3"><i class="fas fa-broom text-primary"></i> Cleaning Mode</h5>', 
                    '<h5 class="font-weight-bold mb-3" style="font-family: \'Open Sans\', sans-serif;"><i class="fas fa-broom text-primary"></i> Cleaning Mode</h5>')

# Add Deep Clean Coming Soon Placeholder
placeholder = """
            <div id="deepCleanPlaceholder" class="text-center py-5" style="display: none; background: #fcfdfe; border-radius: 12px; border: 1px dashed #c2e0ff; margin-bottom: 20px;">
                <i class="fas fa-sparkles mb-3" style="font-size: 50px; color: var(--primary);"></i>
                <h4 class="font-weight-bold" style="color: var(--primary-dark);">Deep Clean Services</h4>
                <p class="text-muted">Our premium deep clean packages are launching very soon. Stay tuned!</p>
            </div>
"""
# Insert before service grid
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
        grid.style.display = 'none';
        placeholder.style.display = 'block';
    } else {
        grid.style.display = 'flex';
        placeholder.style.display = 'none';
        syncGridCounters(); // Re-sync counters for regular mode
    }
}"""

js = re.sub(r'function setCleaningMode\(mode\) \{.*?syncGridCounters\(\);\n\}', new_set_cleaning_mode, js, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Deep Clean Coming Soon updated.")
