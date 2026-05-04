import sys

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'a', encoding='utf-8') as f:
    f.write("""\n
// ==========================================
// NEW GRID COUNTER LOGIC
// ==========================================

function addFixedServiceFromGrid(btn, rawName, basePrice) {
    let finalPrice = basePrice;
    if (currentCleaningMode === 'deep') finalPrice += 50;

    const cartItemId = rawName + (currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)');
    
    if (!cart[cartItemId]) {
        cart[cartItemId] = { rawName: rawName, count: 1, price: finalPrice, timeLimit: 'N/A' };
    } else {
        cart[cartItemId].count++;
    }
    
    showToast("Success", rawName + ' added to cart!', true);
    updateCartUI();
    syncGridCounters();
}

function updateCountFromGrid(btn, rawName, change) {
    const cartItemId = rawName + (currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)');
    
    if (cart[cartItemId]) {
        cart[cartItemId].count += change;
        if (cart[cartItemId].count <= 0) {
            delete cart[cartItemId];
        }
    }
    updateCartUI();
    syncGridCounters();
}

function syncGridCounters() {
    const gridItems = document.querySelectorAll('.service-grid-item');
    gridItems.forEach(item => {
        const rawName = item.getAttribute('data-name');
        const cartItemId = rawName + (currentCleaningMode === 'deep' ? ' (Deep Clean)' : ' (Regular)');
        
        const btnWrapper = item.querySelector('.grid-btn-wrapper');
        if(!btnWrapper) return;
        
        const addBtn = btnWrapper.querySelector('.add-btn-small');
        const counterPill = btnWrapper.querySelector('.counter-pill-grid');
        
        if (cart[cartItemId] && cart[cartItemId].count > 0) {
            addBtn.style.display = 'none';
            counterPill.style.display = 'flex';
            counterPill.querySelector('span').innerText = cart[cartItemId].count;
        } else {
            addBtn.style.display = 'flex';
            counterPill.style.display = 'none';
        }
    });
}

// Ensure grid counters stay synced when cart updates from right panel
const originalUpdateCartUI = updateCartUI;
updateCartUI = function() {
    originalUpdateCartUI();
    if(typeof syncGridCounters === 'function') syncGridCounters();
}

// INTERSECTION OBSERVER FOR FLOATING CART BUTTON
document.addEventListener('DOMContentLoaded', () => {
    const cartSection = document.querySelector('.services-right');
    const floatingBtn = document.getElementById('floatingCartBtn');
    
    if (cartSection && floatingBtn) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                // Cart is in view, hide floating button
                floatingBtn.style.opacity = '0';
                floatingBtn.style.pointerEvents = 'none';
            } else {
                // Cart is not in view, show floating button (if items > 0)
                floatingBtn.style.opacity = '1';
                floatingBtn.style.pointerEvents = 'auto';
            }
        }, { threshold: 0.1 });
        
        observer.observe(cartSection);
    }
});
""")

with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/style.css', 'a', encoding='utf-8') as f:
    f.write("""\n
.center-60 { width: 60%; margin: 0 auto; }
@media (max-width: 768px) {
    .center-60 { width: 95%; }
}
#floatingCartBtn {
    transition: opacity 0.3s ease;
}
""")
print('CSS and JS logic appended.')
