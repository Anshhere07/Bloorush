import re

def update_html():
    with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # In case it was already injected, don't inject again
    if 'id="newPhoneForm"' not in html:
        phone_html = """
                    <!-- Phone Section -->
                    <h6 class="font-weight-bold text-muted mb-2 mt-3" style="font-size: 0.95rem;">Contact Number:</h6>
                    <div id="savedPhoneBlock" style="display:none; margin-bottom: 5px;"></div>
                    <button class="btn btn-sm btn-outline-primary mb-3" id="togglePhoneBtn"
                        onclick="toggleNewPhoneForm()">+ Add New Number</button>

                    <div id="newPhoneForm"
                        style="display:none; border: 1px solid #eaeaea; padding: 15px; border-radius: 8px; margin-bottom: 15px; background: #fafbfc;">
                        <input type="tel" id="contactPhone" class="form-control"
                            placeholder="Mobile Number (10 digits)" pattern="[0-9]{10}"
                            style="border-radius:6px; box-shadow:inset 0 1px 3px rgba(0,0,0,0.05);">
                    </div>
"""
        time_section_marker = "<!-- Time Section -->"
        html = html.replace(time_section_marker, phone_html + "\n                    " + time_section_marker)

        with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/index.html', 'w', encoding='utf-8') as f:
            f.write(html)

def update_js():
    with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # In case it was already injected, skip
    if 'function loadSavedPhones' not in js:
        phone_helpers = """
function loadSavedPhones() {
    return JSON.parse(localStorage.getItem('bloorush_savedPhones') || "[]");
}

function saveNewPhone(phone) {
    let phones = loadSavedPhones();
    if (!phones.includes(phone)) {
        phones.unshift(phone); // Add to top
        if (phones.length > 5) phones.pop(); // Keep max 5
        localStorage.setItem('bloorush_savedPhones', JSON.stringify(phones));
    }
}

function toggleNewPhoneForm() {
    const form = document.getElementById('newPhoneForm');
    const isHidden = form.style.display === 'none';
    form.style.display = isHidden ? 'block' : 'none';
}
"""
        js = js.replace("function loadSavedAddresses() {", phone_helpers + "\nfunction loadSavedAddresses() {")

        setup_phone_ui = """
    // Setup Phone UI
    document.getElementById('newPhoneForm').style.display = 'none';
    const savedPhoneBlock = document.getElementById('savedPhoneBlock');
    const togglePhoneBtn = document.getElementById('togglePhoneBtn');
    const phones = loadSavedPhones();
    
    if (phones.length > 0) {
        let h = '';
        phones.forEach((ph, idx) => {
            h += `<div class="form-check mb-1">
                    <input class="form-check-input" type="radio" name="savedPhoneRadio" id="phoneRadio${idx}" value="${ph}" ${idx===0 ? 'checked' : ''}>
                    <label class="form-check-label text-muted" style="font-size: 0.85rem;" for="phoneRadio${idx}">${ph}</label>
                  </div>`;
        });
        savedPhoneBlock.innerHTML = h;
        savedPhoneBlock.style.display = 'block';
        togglePhoneBtn.innerText = "+ Add New Number";
        togglePhoneBtn.style.display = 'inline-block';
    } else {
        savedPhoneBlock.style.display = 'none';
        document.getElementById('newPhoneForm').style.display = 'block';
        togglePhoneBtn.style.display = 'none'; // Force they write a phone
    }
"""
        addr_block_end = "toggleAddrBtn.style.display = 'none'; // Force they write an address\n    }"
        js = js.replace(addr_block_end, addr_block_end + "\n" + setup_phone_ui)

        phone_validation = """
    // Extract Phone
    let finalPhone = "";
    if (document.getElementById('newPhoneForm').style.display === 'block') {
        const ph = document.getElementById('contactPhone').value.trim();
        if(!ph) {
            alert("Mobile Number is required!");
            return;
        }
        finalPhone = ph;
        saveNewPhone(finalPhone);
    } else {
        const selectedRadio = document.querySelector('input[name="savedPhoneRadio"]:checked');
        if(selectedRadio){
            finalPhone = selectedRadio.value;
        } else {
            alert("Please provide or select a mobile number.");
            return;
        }
    }
"""
        js = js.replace("// Extract Date", phone_validation + "\n    // Extract Date")
        
        # Proper JS template string replacement
        js = js.replace("*Customer Location:*", "*Customer Contact:* ${finalPhone}\\n*Customer Location:*")

        with open('c:/Users/saxen/OneDrive/Desktop/Bloorush/script.js', 'w', encoding='utf-8') as f:
            f.write(js)

update_html()
update_js()
print("Phone functionality added successfully.")
