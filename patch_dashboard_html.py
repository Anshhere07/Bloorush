import re

HTML_PATH = "C:/Users/saxen/OneDrive/Desktop/Bloorush/Bloorush/index.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Public Offers UI
offers_ui = """
                    <!-- Available Offers -->
                    <div class="mb-3" id="availableOffersContainer" style="display: none;">
                        <label class="font-weight-bold mb-2" style="color:var(--primary); font-size: 0.9rem;"><i class="fas fa-tags mr-2"></i>Available Offers</label>
                        <div id="publicCouponsList" class="d-flex overflow-auto pb-2" style="gap: 10px;">
                            <!-- Injected Dynamically -->
                        </div>
                    </div>
"""

# Insert before Coupon Code
html = html.replace('<!-- Coupon Code -->', offers_ui + '\n                    <!-- Coupon Code -->')


# 2. Complete Admin Dashboard Tabbed UI
admin_regex = r'<div id="adminPanelSection" .*?<!-- Floating View Cart Button \(Mobile Only\) -->'
new_admin_ui = """<div id="adminPanelSection" style="display: none; padding: 40px 15px; background: #f8f9fa; min-height: 100vh;">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="font-weight-bold text-primary"><i class="fas fa-chart-line mr-2"></i> Bloorush Admin</h2>
            <button class="btn btn-outline-danger" onclick="exitAdmin()"><i class="fas fa-sign-out-alt mr-1"></i> Exit</button>
        </div>
        
        <!-- Admin Tabs -->
        <ul class="nav nav-tabs mb-4" id="adminTab" role="tablist">
            <li class="nav-item">
                <a class="nav-link active font-weight-bold" id="dashboard-tab" data-toggle="tab" href="#admin-dashboard" role="tab"><i class="fas fa-chart-pie mr-2"></i>Overview</a>
            </li>
            <li class="nav-item">
                <a class="nav-link font-weight-bold" id="users-tab" data-toggle="tab" href="#admin-users" role="tab"><i class="fas fa-users mr-2"></i>Customers</a>
            </li>
            <li class="nav-item">
                <a class="nav-link font-weight-bold" id="coupons-tab" data-toggle="tab" href="#admin-coupons" role="tab"><i class="fas fa-ticket-alt mr-2"></i>Coupons</a>
            </li>
            <li class="nav-item">
                <a class="nav-link font-weight-bold" id="slots-tab" data-toggle="tab" href="#admin-slots" role="tab"><i class="far fa-clock mr-2"></i>Slots</a>
            </li>
        </ul>
        
        <div class="tab-content" id="adminTabContent">
            <!-- Analytics Dashboard -->
            <div class="tab-pane fade show active" id="admin-dashboard" role="tabpanel">
                <div class="row">
                    <div class="col-md-4 mb-3">
                        <div class="card shadow-sm border-0 bg-primary text-white" style="border-radius: 12px;">
                            <div class="card-body">
                                <h6>Total Revenue</h6>
                                <h3 class="font-weight-bold">₹<span id="statRevenue">0</span></h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card shadow-sm border-0 bg-success text-white" style="border-radius: 12px;">
                            <div class="card-body">
                                <h6>Total Bookings</h6>
                                <h3 class="font-weight-bold" id="statBookings">0</h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card shadow-sm border-0 bg-warning text-white" style="border-radius: 12px;">
                            <div class="card-body">
                                <h6>Coupons Redeemed</h6>
                                <h3 class="font-weight-bold" id="statCouponsUsed">0</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- User Management -->
            <div class="tab-pane fade" id="admin-users" role="tabpanel">
                <div class="card shadow-sm border-0" style="border-radius: 15px;">
                    <div class="card-body">
                        <h5 class="font-weight-bold mb-3">Customer Database</h5>
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Phone</th>
                                        <th>Total Bookings</th>
                                        <th>Last Booking</th>
                                    </tr>
                                </thead>
                                <tbody id="adminUsersTable">
                                    <tr><td colspan="4" class="text-center text-muted">No users found.</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Advanced Coupon Manager -->
            <div class="tab-pane fade" id="admin-coupons" role="tabpanel">
                <div class="card shadow-sm border-0" style="border-radius: 15px;">
                    <div class="card-body">
                        <h5 class="font-weight-bold mb-3">Generate Advanced Coupon</h5>
                        <div class="row">
                            <div class="col-md-3 mb-2">
                                <label>Code (e.g. FESTIVE50)</label>
                                <input type="text" id="newCouponCode" class="form-control text-uppercase">
                            </div>
                            <div class="col-md-3 mb-2">
                                <label>Discount Type</label>
                                <select id="newCouponType" class="form-control">
                                    <option value="flat">Flat Amount (₹)</option>
                                    <option value="percent">Percentage (%)</option>
                                </select>
                            </div>
                            <div class="col-md-3 mb-2">
                                <label>Discount Value</label>
                                <input type="number" id="newCouponDiscount" class="form-control">
                            </div>
                            <div class="col-md-3 mb-2">
                                <label>Expiry Date</label>
                                <input type="date" id="newCouponExpiry" class="form-control">
                            </div>
                            <div class="col-md-4 mb-2">
                                <label>Global Usage Limit (0 = Unlimited)</label>
                                <input type="number" id="newCouponGlobalLimit" class="form-control" value="0">
                            </div>
                            <div class="col-md-4 mb-2">
                                <label>Per-Customer Limit</label>
                                <input type="number" id="newCouponUserLimit" class="form-control" value="1">
                            </div>
                            <div class="col-md-4 mb-2 d-flex align-items-end">
                                <button class="btn btn-success btn-block" onclick="createAdvancedCoupon()">Create Coupon</button>
                            </div>
                        </div>
                        <hr>
                        <h6 class="font-weight-bold">Active Coupons</h6>
                        <div id="adminCouponsContainer"></div>
                    </div>
                </div>
            </div>
            
            <!-- Slot Manager -->
            <div class="tab-pane fade" id="admin-slots" role="tabpanel">
                <div class="card shadow-sm border-0" style="border-radius: 15px;">
                    <div class="card-body">
                        <h5 class="font-weight-bold mb-3">Slot Capacity Manager</h5>
                        <input type="date" id="adminSlotDate" class="form-control mb-3" onchange="loadAdminSlots()">
                        <div id="adminSlotsContainer">
                            <p class="text-muted text-center py-4"><small>Select a date to manage slots.</small></p>
                        </div>
                        <button class="btn btn-primary mt-3" onclick="saveAdminSlots()">Save Capacity</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Floating View Cart Button (Mobile Only) -->"""

html = re.sub(admin_regex, new_admin_ui, html, flags=re.DOTALL)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
