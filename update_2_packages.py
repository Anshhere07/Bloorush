import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_cards = """
                <!-- Offer Card 1 -->
                <div class="offer-card text-left"
                    style="min-width: 85vw; max-width: 400px; width: 100%; scroll-snap-align: center; background: linear-gradient(135deg, #0099ff, #004aad); border-radius: 16px; padding: 20px; color: white; position: relative; overflow: hidden; box-shadow: 0 4px 15px rgba(0,74,173,0.3);">
                    <h3 class="font-weight-bold" style="font-family: 'Open Sans', 'IBM Plex Sans', sans-serif;">First Order?</h3>
                    <div
                        style="background: rgba(255,255,255,0.2); padding: 10px 15px; border-radius: 10px; display: inline-block; margin: 10px 0; border: 1px solid rgba(255,255,255,0.4);">
                        <span style="font-size: 0.9rem;">Pay only</span><br>
                        <span class="font-weight-bold" style="font-size: 2rem;">₹49</span>
                    </div>
                    <p style="font-size: 0.85rem; margin-bottom: 15px;">Experience our premium service.</p>
                    <button class="btn btn-dark" style="border-radius: 20px; font-weight: bold; padding: 5px 20px;">BOOK NOW</button>
                    <i class="fas fa-gift"
                        style="position: absolute; right: -10px; bottom: -20px; font-size: 120px; opacity: 0.2;"></i>
                </div>

                <!-- Offer Card 2 -->
                <div class="offer-card text-left"
                    style="min-width: 85vw; max-width: 400px; width: 100%; scroll-snap-align: center; background: linear-gradient(135deg, #a18cd1, #fbc2eb); border-radius: 16px; padding: 20px; color: white; position: relative; overflow: hidden; box-shadow: 0 4px 15px rgba(161,140,209,0.3);">
                    <h3 class="font-weight-bold" style="font-family: 'Open Sans', 'IBM Plex Sans', sans-serif;">Premium Subscriptions</h3>
                    <div
                        style="background: rgba(255,255,255,0.2); padding: 10px 15px; border-radius: 10px; display: inline-block; margin: 10px 0; border: 1px solid rgba(255,255,255,0.4);">
                        <span style="font-size: 0.9rem;">Monthly plans</span><br>
                        <span class="font-weight-bold" style="font-size: 1.5rem;">coming soon</span>
                    </div>
                    <p style="font-size: 0.85rem; margin-bottom: 15px;">Regular clean, less hassle.</p>
                    <button class="btn btn-dark"
                        style="border-radius: 20px; font-weight: bold; padding: 5px 20px; opacity: 0.7;" disabled>COMING SOON</button>
                    <i class="fas fa-calendar-alt"
                        style="position: absolute; right: -10px; bottom: -20px; font-size: 120px; opacity: 0.2;"></i>
                </div>
"""

# Replace in slider
html = re.sub(r'(<div id="offersSlider"[^>]*>).*?(</div>\s*<!-- Dot Indicators -->)', r'\1' + new_cards + r'\2', html, flags=re.DOTALL)

# Replace in packages grid
html = re.sub(r'(<div id="packagesContentGrid"[^>]*>).*?(</div>\s*</div>\s*</div> <!-- End packagesView -->)', r'\1' + new_cards.replace('min-width: 85vw; ', '') + r'\2', html, flags=re.DOTALL)

# Update dots to 2
html = re.sub(r'<div id="offerDotsContainer"[^>]*>.*?</div>', 
              r'<div id="offerDotsContainer" class="d-flex justify-content-center mt-2" style="gap: 5px;">\n                <div class="offer-dot" style="width: 20px; height: 6px; border-radius: 3px; background: #333; transition: all 0.3s ease;"></div>\n                <div class="offer-dot" style="width: 6px; height: 6px; border-radius: 3px; background: #ccc; transition: all 0.3s ease;"></div>\n            </div>', 
              html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Packages updated.")
