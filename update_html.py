import sys

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_html = """            <!-- LEFT: SERVICES WRAPPER CARD -->
            <div class="services-main-card px-3" style="background: transparent; box-shadow: none;">
                
                <div class="d-flex align-items-center mb-1">
                    <div style="background: #008060; padding: 10px; border-radius: 12px; margin-right: 15px;">
                        <i class="fas fa-broom" style="color: white; font-size: 1.2rem;"></i>
                    </div>
                    <div>
                        <h4 class="font-weight-bold mb-0" style="font-family: 'Comic Sans MS', cursive, sans-serif;">Cleaning Mode</h4>
                        <p class="text-muted mb-0" style="font-size: 0.9rem;">Regular or deep cleaning for your home</p>
                    </div>
                </div>

                <!-- Toggle -->
                <div class="cleaning-mode-toggle mt-4 mb-4" style="background: #f8f9fa; border-radius: 30px; display: flex; padding: 5px; box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);">
                    <div class="mode-btn active" id="regularModeBtn" onclick="toggleCleaningMode('regular')" style="flex: 1; text-align: center; padding: 12px; border-radius: 25px; background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); color: #004aad; font-weight: bold; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-spray-can mr-2"></i> Regular
                    </div>
                    <div class="mode-btn" id="deepModeBtn" onclick="toggleCleaningMode('deep')" style="flex: 1; text-align: center; padding: 12px; border-radius: 25px; color: #888; font-weight: bold; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-sparkles mr-2"></i> Deep Clean
                    </div>
                </div>

                <h5 class="font-weight-bold" style="color: #004aad;">Everyday upkeep</h5>
                <p class="text-muted mb-4" style="font-size: 0.9rem;">Quick surface cleaning for daily upkeep.</p>

                <!-- Grid -->
                <div class="services-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    
                    <!-- Item 1 -->
                    <div class="service-grid-item" style="text-align: center;">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <span class="badge badge-warning" style="position: absolute; top: -5px; right: -5px; font-size: 0.6rem;">46% OFF</span>
                            <img src="assets/service_utensils_icon.png" alt="Utensils" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" onclick="addFixedService('Utensils Cleaning', 89)" style="position: absolute; bottom: -10px; right: -5px; background: white; border: 1px solid #004aad; color: #004aad; border-radius: 8px; width: 30px; height: 30px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">+</button>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Utensils</h6>
                        <span class="font-weight-bold" style="color: #004aad; font-size: 0.9rem;" id="price-utensils">₹89</span>
                    </div>

                    <!-- Item 2 -->
                    <div class="service-grid-item" style="text-align: center;">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_bathroom_icon.png" alt="Bathroom" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" onclick="addFixedService('Bathroom Cleaning', 99)" style="position: absolute; bottom: -10px; right: -5px; background: white; border: 1px solid #004aad; color: #004aad; border-radius: 8px; width: 30px; height: 30px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">+</button>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Bathroom</h6>
                        <span class="font-weight-bold" style="color: #004aad; font-size: 0.9rem;" id="price-bathroom">₹99</span>
                    </div>

                    <!-- Item 3 -->
                    <div class="service-grid-item" style="text-align: center;">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_dusting_icon.png" alt="Dusting" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" onclick="addFixedService('Home Dusting', 79)" style="position: absolute; bottom: -10px; right: -5px; background: white; border: 1px solid #004aad; color: #004aad; border-radius: 8px; width: 30px; height: 30px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">+</button>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Dusting</h6>
                        <span class="font-weight-bold" style="color: #004aad; font-size: 0.9rem;" id="price-dusting">₹79</span>
                    </div>

                    <!-- Item 4 -->
                    <div class="service-grid-item" style="text-align: center;">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_mopping_icon.png" alt="Mopping" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" onclick="addFixedService('Mopping & Sweeping', 79)" style="position: absolute; bottom: -10px; right: -5px; background: white; border: 1px solid #004aad; color: #004aad; border-radius: 8px; width: 30px; height: 30px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">+</button>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Mopping</h6>
                        <span class="font-weight-bold" style="color: #004aad; font-size: 0.9rem;" id="price-mopping">₹79</span>
                    </div>

                    <!-- Item 5 -->
                    <div class="service-grid-item" style="text-align: center;">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_fan_icon.png" alt="Fan" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" onclick="addFixedService('Fan Cleaning', 49)" style="position: absolute; bottom: -10px; right: -5px; background: white; border: 1px solid #004aad; color: #004aad; border-radius: 8px; width: 30px; height: 30px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">+</button>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Fan</h6>
                        <span class="font-weight-bold" style="color: #004aad; font-size: 0.9rem;" id="price-fan">₹49</span>
                    </div>

                    <!-- Item 6 -->
                    <div class="service-grid-item" style="text-align: center;">
                        <div class="img-container" style="background: #f8f9fa; border-radius: 16px; padding: 15px; position: relative; margin-bottom: 8px;">
                            <img src="assets/service_window_icon.png" alt="Window" style="width: 100%; object-fit: contain; height: 60px;">
                            <button class="add-btn-small" onclick="addFixedService('Window Cleaning', 49)" style="position: absolute; bottom: -10px; right: -5px; background: white; border: 1px solid #004aad; color: #004aad; border-radius: 8px; width: 30px; height: 30px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">+</button>
                        </div>
                        <h6 class="font-weight-bold mb-0" style="font-size: 0.85rem;">Window</h6>
                        <span class="font-weight-bold" style="color: #004aad; font-size: 0.9rem;" id="price-window">₹49</span>
                    </div>

                </div>
            </div> <!-- End services-main-card -->\n"""

# find start and end index
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<!-- LEFT: SERVICES WRAPPER CARD -->' in line:
        start_idx = i
    if '</div> <!-- End services-main-card -->' in line and start_idx != -1:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [new_html] + lines[end_idx+1:]
    with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Successfully replaced HTML.')
else:
    print('Could not find start/end bounds.')
