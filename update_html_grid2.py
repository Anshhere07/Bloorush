import sys

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_grid_html = """                <!-- Grid -->
                <div class="services-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    
                    <!-- Item 1 -->
                    <div class="service-grid-item" style="text-align: center;" data-name="Utensils Cleaning" data-base-price="89">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <span class="badge badge-warning" style="position: absolute; top: -5px; right: -5px; font-size: 0.6rem;">46% OFF</span>
                            <img src="assets/service_utensils_icon.png" alt="Utensils" style="width: 100%; object-fit: contain; height: 60px;">
                            
                            <button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid(this, 'Utensils Cleaning', 89)">+</button>
                            <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Utensils Cleaning', -1)">-</button>
                                <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Utensils Cleaning', 1)">+</button>
                                <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                            </div>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Utensils</h6>
                        <span class="font-weight-bold price-label" style="color: #004aad; font-size: 0.9rem;" id="price-utensils">₹89</span>
                    </div>

                    <!-- Item 2 -->
                    <div class="service-grid-item" style="text-align: center;" data-name="Bathroom Cleaning" data-base-price="99">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_bathroom_icon.png" alt="Bathroom" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid(this, 'Bathroom Cleaning', 99)">+</button>
                            <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Bathroom Cleaning', -1)">-</button>
                                <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Bathroom Cleaning', 1)">+</button>
                                <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                            </div>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Bathroom</h6>
                        <span class="font-weight-bold price-label" style="color: #004aad; font-size: 0.9rem;" id="price-bathroom">₹99</span>
                    </div>

                    <!-- Item 3 -->
                    <div class="service-grid-item" style="text-align: center;" data-name="Home Dusting" data-base-price="79">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_dusting_icon.png" alt="Dusting" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid(this, 'Home Dusting', 79)">+</button>
                            <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Home Dusting', -1)">-</button>
                                <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Home Dusting', 1)">+</button>
                                <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                            </div>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Dusting</h6>
                        <span class="font-weight-bold price-label" style="color: #004aad; font-size: 0.9rem;" id="price-dusting">₹79</span>
                    </div>

                    <!-- Item 4 -->
                    <div class="service-grid-item" style="text-align: center;" data-name="Mopping & Sweeping" data-base-price="79">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_mopping_icon.png" alt="Mopping" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid(this, 'Mopping & Sweeping', 79)">+</button>
                            <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Mopping & Sweeping', -1)">-</button>
                                <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Mopping & Sweeping', 1)">+</button>
                                <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                            </div>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Mopping</h6>
                        <span class="font-weight-bold price-label" style="color: #004aad; font-size: 0.9rem;" id="price-mopping">₹79</span>
                    </div>

                    <!-- Item 5 -->
                    <div class="service-grid-item" style="text-align: center;" data-name="Fan Cleaning" data-base-price="49">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_fan_icon.png" alt="Fan" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid(this, 'Fan Cleaning', 49)">+</button>
                            <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Fan Cleaning', -1)">-</button>
                                <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Fan Cleaning', 1)">+</button>
                                <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                            </div>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Fan</h6>
                        <span class="font-weight-bold price-label" style="color: #004aad; font-size: 0.9rem;" id="price-fan">₹49</span>
                    </div>

                    <!-- Item 6 -->
                    <div class="service-grid-item" style="text-align: center;" data-name="Window Cleaning" data-base-price="49">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_window_icon.png" alt="Window" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" style="z-index: 10;" onclick="addFixedServiceFromGrid(this, 'Window Cleaning', 49)">+</button>
                            <div class="counter-pill-grid" style="display:none; position: absolute; bottom: -10px; right: -5px; background: white; border: 1.5px solid #38b6ff; border-radius: 6px; color: #38b6ff; font-weight: bold; padding: 0px 4px; height: 28px; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 65px; z-index: 10;">
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Window Cleaning', -1)">-</button>
                                <span style="font-size: 0.95rem; padding: 0; line-height: 1; color: #004aad;">1</span>
                                <button style="border:none; background:none; color:#38b6ff; font-size: 1.2rem; line-height: 1; padding: 0 2px; margin-top: -2px;" onclick="updateCountFromGrid(this, 'Window Cleaning', 1)">+</button>
                                <div style="position: absolute; bottom: -6px; left: 50%; transform: translateX(-50%); background: white; padding: 0 2px; font-size: 0.55rem; color: #666; font-weight: normal; line-height: 1; white-space: nowrap;">items</div>
                            </div>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Window</h6>
                        <span class="font-weight-bold price-label" style="color: #004aad; font-size: 0.9rem;" id="price-window">₹49</span>
                    </div>

                </div>
            </div> <!-- End services-main-card -->
"""

# Replace Grid HTML
grid_start = -1
grid_end = -1
for i, line in enumerate(lines):
    if '<!-- Grid -->' in line:
        grid_start = i
    if '</div> <!-- End services-main-card -->' in line and grid_start != -1:
        grid_end = i
        break

if grid_start != -1 and grid_end != -1:
    lines = lines[:grid_start] + [new_grid_html] + lines[grid_end+1:]

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
    
print('HTML grid wrapper removal done.')
