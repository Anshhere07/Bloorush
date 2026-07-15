import re

# 1. Update JS Analytics
JS_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/script.js"

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the Analytics injection
wa_search = r"let msg = `Hi, I am \$\{document\.getElementById\('userName'\)\.value\}, this is my first booking request:\\n\\n`;"
wa_replace = """// -- LOG ANALYTICS & USER DATA --
      if(typeof recordAnalyticsAndUser === 'function') {
          recordAnalyticsAndUser(document.getElementById('userName').value, document.getElementById('userPhone').value, finalTotal);
      }
      if (typeof appliedCouponCode !== 'undefined' && appliedCouponCode !== "") {
          if(typeof recordCouponUsage === 'function') {
              recordCouponUsage(appliedCouponCode, document.getElementById('userPhone').value);
          }
      }
      
      let msg = `Hi, I am ${document.getElementById('userName').value}, this is my first booking request:\\n\\n`;"""

js = re.sub(wa_search, wa_replace, js)

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update HTML Glassmorphism
HTML_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/index.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Inject CSS
glass_css = """
    <style>
        /* Glassmorphism Admin Dashboard */
        #adminPanelSection {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%) !important;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.45) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
            border-radius: 20px !important;
        }
        .glass-text {
            color: #2c3e50 !important;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }
        /* Make nav tabs glassy too */
        #adminTab .nav-link {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px 12px 0 0;
            margin-right: 5px;
            color: #2c3e50;
            backdrop-filter: blur(5px);
        }
        #adminTab .nav-link.active {
            background: rgba(255, 255, 255, 0.6);
            border-bottom-color: transparent;
            font-weight: 800;
        }
    </style>
"""

if '/* Glassmorphism Admin Dashboard */' not in html:
    html = html.replace('</head>', glass_css + '\n</head>')

# Replace Card classes with glass-card
# Revenue Card
html = html.replace('<div class="card shadow-sm border-0 bg-primary text-white" style="border-radius: 12px;">', '<div class="card glass-card text-center text-dark">')
# Bookings Card
html = html.replace('<div class="card shadow-sm border-0 bg-success text-white" style="border-radius: 12px;">', '<div class="card glass-card text-center text-dark">')
# Coupons Card
html = html.replace('<div class="card shadow-sm border-0 bg-warning text-white" style="border-radius: 12px;">', '<div class="card glass-card text-center text-dark">')

# Other standard cards
html = html.replace('<div class="card shadow-sm border-0" style="border-radius: 12px;">', '<div class="card glass-card">')
html = html.replace('<div class="card shadow-sm border-0" style="border-radius: 15px;">', '<div class="card glass-card">')

# Dashboard title
html = html.replace('<h2 class="font-weight-bold text-primary">', '<h2 class="font-weight-bold glass-text">')

# Update script version
html = re.sub(r'script\.js\?v=\d+', 'script.js?v=15', html)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Analytics patched and Glassmorphism applied successfully!")
