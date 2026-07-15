import re

HTML_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/index.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject userPhone and Coupon/Offers UI into the slotBookingModal
# The slotBookingModal has: `<div class="mb-3">\n                        <h6 class="font-weight-bold text-muted mb-2 mt-3" style="font-size: 0.95rem;">Preferred Date:</h6>`

missing_ui = """
                    <!-- Phone Number -->
                    <div class="mb-3">
                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-phone-alt mr-2"></i>Phone Number</label>
                        <input type="tel" id="userPhone" class="form-control" placeholder="10-digit Mobile Number" style="border-radius: 8px;">
                    </div>
                    
                    <!-- Available Offers -->
                    <div class="mb-3" id="availableOffersContainer" style="display: none;">
                        <label class="font-weight-bold mb-2" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-tags mr-2"></i>Available Offers</label>
                        <div id="publicCouponsList" class="d-flex overflow-auto pb-2" style="gap: 10px;">
                            <!-- Injected Dynamically -->
                        </div>
                    </div>

                    <!-- Coupon Code -->
                    <div class="mb-3 p-3 bg-light" style="border-radius: 12px; border: 1px dashed #ccc;">
                        <label class="font-weight-bold mb-1" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-ticket-alt mr-2"></i>Apply Coupon</label>
                        <div class="input-group">
                            <input type="text" id="couponInput" class="form-control text-uppercase" placeholder="Enter Code">
                            <div class="input-group-append">
                                <button class="btn btn-outline-primary" id="applyCouponBtn" onclick="applyCoupon()">Apply</button>
                            </div>
                        </div>
                        <small id="couponMessage" class="form-text text-success" style="display:none;"></small>
                    </div>

"""

date_section_pattern = r'<!-- Date Section -->\s*<h6 class="font-weight-bold text-muted mb-2 mt-3"'

if 'id="userPhone"' not in html:
    html = re.sub(date_section_pattern, missing_ui + '\n<!-- Date Section -->\n<h6 class="font-weight-bold text-muted mb-2 mt-3"', html)


# 2. Inject Chart.js into head
if 'chart.js' not in html:
    html = html.replace('</head>', '\n<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>')


# 3. Add Canvas for Charts in Admin Dashboard
charts_ui = """
                <div class="row mb-4">
                    <div class="col-md-6 mb-3">
                        <div class="card shadow-sm border-0" style="border-radius: 12px;">
                            <div class="card-body">
                                <h6 class="font-weight-bold">Revenue Growth</h6>
                                <canvas id="revenueChart" style="max-height: 250px;"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="card shadow-sm border-0" style="border-radius: 12px;">
                            <div class="card-body">
                                <h6 class="font-weight-bold">Coupons Redeemed</h6>
                                <canvas id="bookingsChart" style="max-height: 250px;"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
"""
# Insert charts right above User Management tab definition, wait no, inside admin-dashboard tab.
admin_dash_end_pattern = r'<!-- User Management -->'
if 'revenueChart' not in html:
    html = html.replace('<!-- User Management -->', charts_ui + '\n<!-- User Management -->')


# 4. Add User Action Modals (Edit/Delete User in CRUD)
crud_modals = """
<!-- Admin Edit User Modal -->
<div class="modal fade" id="adminEditUserModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header bg-primary text-white">
        <h5 class="modal-title">Edit Customer</h5>
      </div>
      <div class="modal-body">
        <input type="hidden" id="editUserPhone">
        <div class="form-group">
            <label>Name</label>
            <input type="text" id="editUserName" class="form-control">
        </div>
        <div class="form-group">
            <label>Total Bookings</label>
            <input type="number" id="editUserBookings" class="form-control">
        </div>
        <button class="btn btn-primary btn-block" onclick="saveAdminUserEdit()">Save Changes</button>
      </div>
    </div>
  </div>
</div>
"""
if 'adminEditUserModal' not in html:
    html = html.replace('<!-- Floating View Cart Button (Mobile Only) -->', crud_modals + '\n<!-- Floating View Cart Button (Mobile Only) -->')

# Update script version
html = re.sub(r'script\.js\?v=\d+', 'script.js?v=14', html)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated with UserPhone, Coupon UI, Charts, and CRUD Modals")
