import os

files = {
    "models/client.py": """from datetime import datetime
import uuid

class Client:
    def __init__(self, first_name, last_name, email, phone):
        self.client_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.kyc_status = 'pending'
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_kyc(self, status):
        self.kyc_status = status
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'client_id': self.client_id,
            'name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'kyc_status': self.kyc_status
        }
""",

    "templates/onboarding/step1-personal.html": """<div class="onboarding-container" style="background-color: #0a1628; color: #fff; padding: 40px; border-radius: 8px;">
    <h2 style="color: #e5b13b;">Step 1: Personal Information</h2>
    <form id="onboardingForm">
        <div class="form-group">
            <label for="firstName">First Name</label>
            <input type="text" id="firstName" name="firstName" required class="form-control">
        </div>
        <div class="form-group">
            <label for="lastName">Last Name</label>
            <input type="text" id="lastName" name="lastName" required class="form-control">
        </div>
        <button type="submit" class="btn" style="background-color: #e5b13b; color: #0a1628; font-weight: bold; padding: 10px 20px; border: none; border-radius: 4px; margin-top: 20px;">Continue</button>
    </form>
</div>
""",

    "assets/js/onboarding.js": """document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('onboardingForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('Onboarding step 1 submitted.');
            // Proceed to next step...
        });
    }
});
""",

    "models/portfolio.py": """from datetime import datetime

class Portfolio:
    def __init__(self, client_id):
        self.client_id = client_id
        self.total_value = 0.0
        self.assets = []
        self.last_updated = datetime.utcnow()

    def add_asset(self, symbol, quantity, current_price):
        self.assets.append({'symbol': symbol, 'quantity': quantity, 'price': current_price})
        self.recalculate()

    def recalculate(self):
        self.total_value = sum(asset['quantity'] * asset['price'] for asset in self.assets)
        self.last_updated = datetime.utcnow()
""",

    "templates/portfolio/dashboard.html": """<div class="portfolio-dashboard" style="padding: 20px;">
    <h1 style="color: #0a1628;">Portfolio Overview</h1>
    <div class="summary-cards" style="display: flex; gap: 20px; margin-bottom: 30px;">
        <div class="card" style="border-left: 4px solid #e5b13b; padding: 20px; background: #f9f9f9; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>Total Value</h3>
            <p id="totalValue" style="font-size: 24px; font-weight: bold;">$0.00</p>
        </div>
    </div>
    <div id="portfolioChart" style="height: 300px; width: 100%;"></div>
</div>
""",

    "assets/js/portfolio.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Portfolio dashboard initialized.');
    // Init Chart.js or similar visualization here
    const totalValueEl = document.getElementById('totalValue');
    if(totalValueEl) {
        totalValueEl.innerText = '$124,500.00'; // Mock data
    }
});
""",

    "templates/vault/index.html": """<div class="vault-container" style="padding: 20px;">
    <h2 style="color: #0a1628;">Secure Document Vault</h2>
    <div class="upload-area" style="border: 2px dashed #e5b13b; padding: 40px; text-align: center; border-radius: 8px; margin-top: 20px;">
        <p>Drag & drop documents here or <button class="btn btn-link" style="color: #e5b13b;">Browse</button></p>
    </div>
    <ul id="documentList" style="list-style: none; padding: 0; margin-top: 20px;">
        <li style="padding: 10px; border-bottom: 1px solid #ddd;">KYC_Document.pdf <span style="color: green; float: right;">Verified</span></li>
    </ul>
</div>
""",

    "assets/js/vault.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Secure Vault initialized.');
});
""",

    "templates/messages/index.html": """<div class="messages-container" style="display: flex; height: 500px; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
    <div class="sidebar" style="width: 30%; background: #0a1628; color: #fff; padding: 20px;">
        <h3 style="color: #e5b13b;">Advisors</h3>
        <ul style="list-style: none; padding: 0;">
            <li style="padding: 10px 0; border-bottom: 1px solid #1a2a40;">Sarah Jenkins</li>
        </ul>
    </div>
    <div class="chat-area" style="width: 70%; padding: 20px; display: flex; flex-direction: column;">
        <div class="history" style="flex-grow: 1; overflow-y: auto;">
            <p><strong>Sarah:</strong> Welcome! How can I help you today?</p>
        </div>
        <div class="input-area" style="margin-top: 20px; display: flex;">
            <input type="text" placeholder="Type a message..." style="flex-grow: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
            <button style="background: #e5b13b; border: none; padding: 10px 20px; border-radius: 4px; margin-left: 10px; color: #0a1628; font-weight: bold;">Send</button>
        </div>
    </div>
</div>
""",

    "assets/js/messages.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Messaging system initialized.');
});
""",

    "templates/scheduler/index.html": """<div class="scheduler-container" style="padding: 20px;">
    <h2 style="color: #0a1628;">Schedule a Meeting</h2>
    <div id="calendar" style="margin-top: 20px; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
        <p>Select a date and time...</p>
        <!-- Mock calendar grid -->
    </div>
    <button style="margin-top: 20px; background: #e5b13b; color: #0a1628; border: none; padding: 10px 20px; border-radius: 4px; font-weight: bold;">Confirm Booking</button>
</div>
""",

    "assets/js/scheduler.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Meeting Scheduler initialized.');
});
""",

    "templates/billing/index.html": """<div class="billing-container" style="padding: 20px;">
    <h2 style="color: #0a1628;">Billing & Invoices</h2>
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
            <tr style="background: #0a1628; color: #fff;">
                <th style="padding: 10px; text-align: left;">Invoice ID</th>
                <th style="padding: 10px; text-align: left;">Date</th>
                <th style="padding: 10px; text-align: left;">Amount</th>
                <th style="padding: 10px; text-align: left;">Status</th>
                <th style="padding: 10px; text-align: left;">Action</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">INV-001</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">2026-08-01</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;">$150.00</td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><span style="color: green;">Paid</span></td>
                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><button style="background: transparent; border: 1px solid #e5b13b; color: #e5b13b; padding: 5px 10px; border-radius: 4px;">Download</button></td>
            </tr>
        </tbody>
    </table>
</div>
""",

    "assets/js/billing.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Billing module initialized.');
});
""",

    "templates/reports/index.html": """<div class="reports-container" style="padding: 20px;">
    <h2 style="color: #0a1628;">Client Reports</h2>
    <div class="filters" style="margin-top: 20px; display: flex; gap: 10px;">
        <select style="padding: 10px; border-radius: 4px; border: 1px solid #ddd;">
            <option>Q3 2026</option>
            <option>Q2 2026</option>
        </select>
        <button style="background: #e5b13b; color: #0a1628; border: none; padding: 10px 20px; border-radius: 4px; font-weight: bold;">Generate PDF</button>
    </div>
</div>
""",

    "assets/js/reports.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Reporting engine initialized.');
});
""",

    "templates/admin/dashboard.html": """<div class="admin-dashboard" style="padding: 20px; display: flex;">
    <div class="sidebar" style="width: 250px; background: #0a1628; color: #fff; min-height: 100vh; padding: 20px;">
        <h3 style="color: #e5b13b; margin-top: 0;">CRM Admin</h3>
        <ul style="list-style: none; padding: 0;">
            <li style="padding: 10px 0;"><a href="#" style="color: #fff; text-decoration: none;">Clients</a></li>
            <li style="padding: 10px 0;"><a href="#" style="color: #fff; text-decoration: none;">Compliance</a></li>
            <li style="padding: 10px 0;"><a href="#" style="color: #fff; text-decoration: none;">Settings</a></li>
        </ul>
    </div>
    <div class="main-content" style="flex-grow: 1; padding: 20px;">
        <h2>Dashboard Overview</h2>
        <div style="display: flex; gap: 20px; margin-top: 20px;">
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; flex: 1; border-top: 4px solid #e5b13b;">
                <h4>Active Clients</h4>
                <p style="font-size: 24px; font-weight: bold;">1,204</p>
            </div>
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; flex: 1; border-top: 4px solid #e5b13b;">
                <h4>Pending KYC</h4>
                <p style="font-size: 24px; font-weight: bold;">45</p>
            </div>
        </div>
    </div>
</div>
""",

    "assets/js/admin.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Admin dashboard CRM initialized.');
});
""",

    "templates/auth/2fa-setup.html": """<div class="2fa-setup-container" style="max-width: 400px; margin: 40px auto; padding: 30px; background: #f9f9f9; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <h2 style="color: #0a1628; text-align: center;">Set Up Two-Factor Authentication</h2>
    <p style="text-align: center; color: #666;">Scan this QR code with your authenticator app.</p>
    <div style="width: 200px; height: 200px; background: #ddd; margin: 20px auto; display: flex; align-items: center; justify-content: center;">
        [QR CODE]
    </div>
    <div class="form-group" style="margin-top: 20px;">
        <label>Enter 6-digit code</label>
        <input type="text" id="token2fa" class="form-control" style="width: 100%; padding: 10px; margin-top: 5px;">
    </div>
    <button style="width: 100%; background: #e5b13b; color: #0a1628; padding: 12px; border: none; border-radius: 4px; font-weight: bold; margin-top: 20px;">Verify & Enable</button>
</div>
""",

    "assets/js/2fa.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('2FA Setup initialized.');
});
""",

    "api/client.py": """from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/clients', methods=['GET'])
def get_clients():
    # Mock data
    return jsonify({'status': 'success', 'data': []})

@api.route('/portfolio/<client_id>', methods=['GET'])
def get_portfolio(client_id):
    return jsonify({'status': 'success', 'total_value': 124500.00})
""",

    ".env.example": """# CRM Ecosystem Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=secret
JWT_SECRET=super_secret_key
TWO_FACTOR_SECRET_KEY=replace_this
API_BASE_URL=https://api.amana-capital-ea.co.tz/v1
""",

    "docs/API_INTEGRATION.md": """# Amana Capital EA API Integration

## Overview
This document outlines the API endpoints available for the Enterprise CRM and Client Portal.

## Authentication
All API requests must include a valid JWT token in the `Authorization` header.
`Authorization: Bearer <token>`

## Endpoints

### `GET /api/v1/clients`
Retrieves a list of clients (Admin only).

### `GET /api/v1/portfolio/{client_id}`
Retrieves the portfolio summary for a specific client.
"""
}

# Ensure directories exist and write files
for file_path, content in files.items():
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Successfully generated {len(files)} Phase 5 files.")

# Update style.css safely
style_path = "style.css"
if os.path.exists(style_path):
    with open(style_path, "a", encoding="utf-8", errors="ignore") as f:
        f.write("\n/* Phase 5: CRM & Portal Extensions */\n")
        f.write(".vault-container .upload-area:hover { background-color: rgba(229, 177, 59, 0.1); cursor: pointer; }\n")
        f.write(".messages-container .history p { margin: 5px 0; }\n")

# Update assets/js/auth.js safely
auth_js_path = "assets/js/auth.js"
if os.path.exists(auth_js_path):
    with open(auth_js_path, "a", encoding="utf-8") as f:
        f.write("\n// Added during Phase 5 for 2FA integration\n")
        f.write("function init2FA() { console.log('2FA hook active'); }\n")
else:
    if not os.path.exists("assets/js"):
        os.makedirs("assets/js")
    with open(auth_js_path, "w", encoding="utf-8") as f:
        f.write("// Auth module\n")
        f.write("function init2FA() { console.log('2FA hook active'); }\n")

print("Updated style.css and auth.js")
