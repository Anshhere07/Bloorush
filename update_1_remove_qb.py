import re

# Remove quick book HTML
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Quick Book section
html = re.sub(r'<!-- QUICK BOOK SECTION -->\s*<section class="quick-book-section.*?</section>', '', html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Remove Quick Book JS
with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove addQuickBookFromGrid
js = re.sub(r'function addQuickBookFromGrid.*?\n}', '', js, flags=re.DOTALL)
# Remove updateCountFromQuickBook
js = re.sub(r'function updateCountFromQuickBook.*?\n}', '', js, flags=re.DOTALL)
# Remove syncQuickBookCounters
js = re.sub(r'function syncQuickBookCounters.*?\n}', '', js, flags=re.DOTALL)

# Remove QUICK BOOK COUNTER LOGIC comment block
js = re.sub(r'// ==========================================\n// QUICK BOOK COUNTER LOGIC\n// ==========================================', '', js)

# Remove call to syncQuickBookCounters
js = js.replace("if(typeof syncQuickBookCounters === 'function') syncQuickBookCounters();\n", "")

# Remove querySelector for quick-book-section
js = re.sub(r'if \(document\.querySelector\(\'\.quick-book-section\'\)\) document\.querySelector\(\'\.quick-book-section\'\)\.style\.display = \'.*?\';\n', '', js)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Quick Book logic removed.")
