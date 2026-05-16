import re

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_trust_section = """
        <!-- TRUSTED SECTION -->
        <section class="trusted-section center-60 px-3 mb-5 mt-5">
            <h2 class="font-weight-bold text-center mb-5" style="color: var(--primary-dark);">Trusted Home Help for Thousands of Families</h2>
            <div class="row">
                <!-- Left Pink Box -->
                <div class="col-md-5 mb-4 mb-md-0">
                    <div class="trusted-pink-box text-white" style="background: linear-gradient(135deg, #e91e63, #c2185b); border-radius: 20px; padding: 40px 30px; height: 100%; box-shadow: 0 10px 30px rgba(233, 30, 99, 0.3);">
                        <i class="fas fa-shield-alt mb-3" style="font-size: 30px; opacity: 0.8;"></i>
                        <h3 class="font-weight-bold mb-3">Trusted by Nagpur's Families</h3>
                        <p class="mb-4" style="font-size: 0.95rem; opacity: 0.9;">Every Expert is background checked, Aadhaar verified & professionally trained before their first booking.</p>
                        
                        <div class="row mt-4">
                            <div class="col-6 mb-3">
                                <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 15px;">
                                    <h4 class="font-weight-bold mb-0">500+</h4>
                                    <small style="opacity: 0.8;">Families Served</small>
                                </div>
                            </div>
                            <div class="col-6 mb-3">
                                <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 15px;">
                                    <h4 class="font-weight-bold mb-0">4.7</h4>
                                    <small style="opacity: 0.8;">Average Rating</small>
                                </div>
                            </div>
                            <div class="col-6">
                                <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 15px;">
                                    <h4 class="font-weight-bold mb-0">1000+</h4>
                                    <small style="opacity: 0.8;">Bookings Done</small>
                                </div>
                            </div>
                            <div class="col-6">
                                <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 15px;">
                                    <h4 class="font-weight-bold mb-0">15 Min</h4>
                                    <small style="opacity: 0.8;">Average Arrival</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Features Grid -->
                <div class="col-md-7">
                    <div class="row h-100">
                        <div class="col-6 mb-4">
                            <div class="trust-feature-card h-100" style="background: white; border-radius: 20px; padding: 25px 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
                                <div style="width: 40px; height: 40px; background: #fff0f5; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                    <i class="fas fa-award" style="color: #e91e63;"></i>
                                </div>
                                <h6 class="font-weight-bold" style="color: var(--primary-dark);">Background Verified & Trusted</h6>
                                <p class="text-muted mb-0" style="font-size: 0.85rem;">Aadhaar and PAN are verified, and every Expert is put through a multi-step verification process before being onboarded.</p>
                            </div>
                        </div>
                        <div class="col-6 mb-4">
                            <div class="trust-feature-card h-100" style="background: white; border-radius: 20px; padding: 25px 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
                                <div style="width: 40px; height: 40px; background: #fff0f5; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                    <i class="fas fa-female" style="color: #e91e63;"></i>
                                </div>
                                <h6 class="font-weight-bold" style="color: var(--primary-dark);">Powered by Women Workforce</h6>
                                <p class="text-muted mb-0" style="font-size: 0.85rem;">A 100% female workforce is maintained - trained, empowered, and trusted by families.</p>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="trust-feature-card h-100" style="background: white; border-radius: 20px; padding: 25px 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
                                <div style="width: 40px; height: 40px; background: #fff0f5; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                    <i class="fas fa-rupee-sign" style="color: #e91e63;"></i>
                                </div>
                                <h6 class="font-weight-bold" style="color: var(--primary-dark);">No Hidden Charges</h6>
                                <p class="text-muted mb-0" style="font-size: 0.85rem;">Transparent pricing is ensured, with no hidden charges.</p>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="trust-feature-card h-100" style="background: white; border-radius: 20px; padding: 25px 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
                                <div style="width: 40px; height: 40px; background: #fff0f5; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                                    <i class="fas fa-star" style="color: #e91e63;"></i>
                                </div>
                                <h6 class="font-weight-bold" style="color: var(--primary-dark);">Top Rated Experts</h6>
                                <p class="text-muted mb-0" style="font-size: 0.85rem;">Experts are rated and trusted by people just like you.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
"""

html = re.sub(r'<section class="testimonial-section[^>]*>.*?</section>', new_trust_section, html, flags=re.DOTALL)

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Trust section updated.")
