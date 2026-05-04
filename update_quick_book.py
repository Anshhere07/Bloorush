import sys

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

quick_html = """        <div class="quick-book-slider d-flex"
                style="gap: 12px; overflow-x: auto; padding-bottom: 15px; -webkit-overflow-scrolling: touch; scrollbar-width: none;">

                <div class="quick-card" data-name="30 min"
                    style="min-width: 130px; border: 1px solid #c2e0ff; border-radius: 12px; padding: 15px; background: #f4f9ff; text-align: center; position: relative;">
                    <h6 class="font-weight-bold mb-1">30 min</h6>
                    <p class="text-muted mb-2" style="font-size: 0.8rem;">Express</p>
                    <h5 class="font-weight-bold" style="color: #333;">₹89</h5>
                    <button class="add-btn-small" style="z-index: 10;" onclick="addQuickBookFromGrid(this, '30 min', 89)">+</button>
                    <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '30 min', -1)">-</button>
                        <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '30 min', 1)">+</button>
                        <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                    </div>
                </div>

                <div class="quick-card" data-name="1 hr"
                    style="min-width: 130px; border: 1px solid #c2e0ff; border-radius: 12px; padding: 15px; background: #fcfdfe; text-align: center; position: relative;">
                    <h6 class="font-weight-bold mb-1 mt-1">1 hr</h6>
                    <p class="text-muted mb-2" style="font-size: 0.8rem;">Standard</p>
                    <h5 class="font-weight-bold" style="color: #333;">₹159</h5>
                    <button class="add-btn-small" style="z-index: 10;" onclick="addQuickBookFromGrid(this, '1 hr', 159)">+</button>
                    <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '1 hr', -1)">-</button>
                        <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '1 hr', 1)">+</button>
                        <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                    </div>
                </div>

                <div class="quick-card" data-name="1.5 hr"
                    style="min-width: 130px; border: 1px solid #c2e0ff; border-radius: 12px; padding: 15px; background: #fcfdfe; text-align: center; position: relative;">
                    <h6 class="font-weight-bold mb-1">1.5 hr</h6>
                    <p class="text-muted mb-2" style="font-size: 0.8rem;">Plus</p>
                    <h5 class="font-weight-bold" style="color: #333;">₹240</h5>
                    <button class="add-btn-small" style="z-index: 10;" onclick="addQuickBookFromGrid(this, '1.5 hr', 240)">+</button>
                    <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '1.5 hr', -1)">-</button>
                        <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '1.5 hr', 1)">+</button>
                        <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                    </div>
                </div>

                <div class="quick-card" data-name="120 min"
                    style="min-width: 130px; border: 1px solid #c2e0ff; border-radius: 12px; padding: 15px; background: #fcfdfe; text-align: center; position: relative;">
                    <h6 class="font-weight-bold mb-1">120 min</h6>
                    <p class="text-muted mb-2" style="font-size: 0.8rem;">Deep</p>
                    <h5 class="font-weight-bold" style="color: #333;">₹299</h5>
                    <button class="add-btn-small" style="z-index: 10;" onclick="addQuickBookFromGrid(this, '120 min', 299)">+</button>
                    <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '120 min', -1)">-</button>
                        <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                        <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromQuickBook(this, '120 min', 1)">+</button>
                        <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                    </div>
                </div>

            </div>
"""

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="quick-book-slider d-flex"' in line:
        start_idx = i
    if '</section>' in line and start_idx != -1 and i > start_idx and end_idx == -1:
        end_idx = i

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [quick_html] + lines[end_idx:]

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
    
print("Replaced quick book slider HTML")
