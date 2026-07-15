import re

HTML_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/index.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the Support column to include the Admin Link
support_search = r'<!-- Col 3: Support -->\s*<div class="footer-col">\s*<h5 class="footer-heading">Support</h5>\s*<ul class="footer-links">\s*<li><a href="#">Privacy Policy</a></li>\s*<li><a href="#">Terms & Conditions</a></li>\s*</ul>\s*</div>'

support_replace = """<!-- Col 3: Support -->
              <div class="footer-col">
                  <h5 class="footer-heading">Support</h5>
                  <ul class="footer-links">
                      <li><a href="#">Privacy Policy</a></li>
                      <li><a href="#">Terms & Conditions</a></li>
                      <li><a href="#" style="opacity: 0.3;" onclick="promptAdminLogin(event)">Admin Access</a></li>
                  </ul>
              </div>"""

html = re.sub(support_search, support_replace, html)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
