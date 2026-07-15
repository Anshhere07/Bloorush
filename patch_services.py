import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Bathroom Cleaning
bathroom_old = """<div class="service-grid-item" style="text-align: center;" data-name="Bathroom Cleaning"
                            data-base-price="99">"""
bathroom_new = """<div class="service-grid-item" style="text-align: center;" data-name="Bathroom Cleaning"
                            data-base-price="89">"""
html = html.replace(bathroom_old, bathroom_new)

bathroom_opts_old = """<option value="30 min" data-price="89">30 min</option>
                                <option value="45 min" data-price="149">45 min</option>
                                <option value="60 min" data-price="189">60 min</option>
                                <option value="90 min" data-price="239">90 min</option>"""

bathroom_opts_new = """<option value="1 unit" data-price="89">1 unit</option>
                                <option value="2 unit" data-price="178">2 unit</option>
                                <option value="3 unit" data-price="267">3 unit</option>
                                <option value="4 unit" data-price="356">4 unit</option>"""
html = html.replace(bathroom_opts_old, bathroom_opts_new)


# 2. Update Fan Cleaning
fan_old = """<!-- Item 5 -->
                        <div class="service-grid-item" style="text-align: center;" data-name="Fan Cleaning"
                            data-base-price="49">"""
fan_new = """<!-- Item 5 -->
                        <div class="service-grid-item" style="text-align: center; position: relative; opacity: 0.6; pointer-events: none;" data-name="Fan Cleaning"
                            data-base-price="49">
                            <div style="position:absolute; top:-8px; left:50%; transform:translateX(-50%); background:linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); color:#d81b60; font-size:10px; padding:3px 10px; border-radius:12px; font-weight:800; white-space:nowrap; z-index:10; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">Coming Soon</div>"""
html = html.replace(fan_old, fan_new)

# 3. Update Window Cleaning
window_old = """<!-- Item 6 -->
                        <div class="service-grid-item" style="text-align: center;" data-name="Window Cleaning"
                            data-base-price="49">"""
window_new = """<!-- Item 6 -->
                        <div class="service-grid-item" style="text-align: center; position: relative; opacity: 0.6; pointer-events: none;" data-name="Window Cleaning"
                            data-base-price="49">
                            <div style="position:absolute; top:-8px; left:50%; transform:translateX(-50%); background:linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); color:#d81b60; font-size:10px; padding:3px 10px; border-radius:12px; font-weight:800; white-space:nowrap; z-index:10; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">Coming Soon</div>"""
html = html.replace(window_old, window_new)


with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully.")
