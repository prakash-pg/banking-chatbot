# Advanced Banking Chatbot
# Requires Flask: pip install flask

from flask import Flask, render_template, request, jsonify
import random
import re
from datetime import datetime, timedelta
import json
import uuid

app = Flask(__name__)

# Mock database for demonstration
USERS_DB = {
    "demo@bank.com": {
        "password": "demo123",
        "name": "Prakash",
        "accounts": {
            "savings-001": {
                "type": "savings",
                "balance": 15000.50,
                "account_number": "****5678",
                "transactions": [
                    {"date": "2025-05-01", "type": "credit", "amount": 1000, "description": "Salary deposit"},
                    {"date": "2025-05-03", "type": "debit", "amount": 500, "description": "ATM withdrawal"},
                ]
            },
            "checking-001": {
                "type": "checking",
                "balance": 5000.00,
                "account_number": "****1234",
                "transactions": [
                    {"date": "2025-05-02", "type": "debit", "amount": 150, "description": "Grocery store"},
                    {"date": "2025-05-04", "type": "credit", "amount": 200, "description": "Transfer from savings"},
                ]
            }
        },
        "loans": [
            {"id": "loan-001", "type": "car loan", "balance": 20000, "monthly_payment": 450, "next_due": "2025-05-15"}
        ],
        "cards": [
            {"id": "card-001", "type": "credit", "number": "****4321", "balance": 1200, "limit": 5000}
        ]
    }
}

class BankingChatbot:
    def __init__(self):
        self.name = "BankBot"
        self.context = {}
        self.sessions = {}
        
        # Categorize intents for banking queries
        self.intents = {
            # Authentication
            'login': r'log(?: )?in|sign in|authenticate|access account',
            'logout': r'log(?: )?out|sign out|exit',
            
            # Account inquiries
            'balance': r'balance|how much|fund|available',
            'transactions': r'transaction|history|statement|recent',
            'account_info': r'account.*(?:detail|info)|my account',
            
            # Money transfers
            'transfer': r'transfer|send money|move fund',
            'payment': r'pay|payment|bill',
            
            # Card services
            'card_balance': r'card.*balance|credit.*balance',
            'card_payment': r'pay.*card|card.*payment',
            'card_limit': r'card.*limit|credit.*limit',
            'block_card': r'block.*card|(?:freeze|stop) card',
            
            # Loan information
            'loan_info': r'loan|(?:loan )?(?:balance|payment|due)',
            
            # Branch and ATM
            'branch': r'branch|office|(?:nearest )?(?:bank|atm)',
            'atm': r'atm|cash.*withdraw',
            
            # Help and support
            'help': r'help|support|assist|customer|service',
            'complaints': r'complain|issue|problem|wrong',
            
            # Interest rates
            'interest_rates': r'(?:interest|saving) rate|deposit.*rate|loan.*rate'
        }
        
        # Responses with personality
        self.responses = {
            'greeting': [
                "Welcome to SecureBank! I'm BankBot, your digital banking assistant. How can I help you today?",
                "Hello! I'm here to assist with your banking needs. Please login to continue.",
                "Hi there! I'm BankBot. For personalized assistance, please log in to your account."
            ],
            'need_login': [
                "I'll need you to log in first. Please type 'login' to access your account.",
                "For security reasons, please log in to view your account details.",
                "To assist you better, let's log you in. Type 'login' when ready."
            ],
            'login_success': [
                "Welcome back! How can I assist you with your banking today?",
                "Great to see you again! What can I help you with?",
                "Successfully logged in. How may I serve you today?"
            ],
            'error': [
                "I apologize for the inconvenience. Let's try that again.",
                "I encountered an issue. Could you rephrase your request?",
                "Something went wrong. Please try again or contact support."
            ]
        }
    
    def create_session(self, user_id):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'user_id': user_id,
            'authenticated': True,
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        return session_id
    
    def get_session(self, session_id):
        return self.sessions.get(session_id)
    
    def detect_intent(self, message):
        message = message.lower()
        detected_intents = []
        
        for intent, pattern in self.intents.items():
            if re.search(pattern, message):
                detected_intents.append(intent)
        
        return detected_intents[0] if detected_intents else 'unknown'
    
    def handle_login(self, message, session_id=None):
    # Simple login simulation
        match = re.search(r'(?:login\s+)?(?:user(?:name)?:?\s*|email:?\s*)?([\w\.-]+@[\w\.-]+)', message.lower())
        if match:
            email = match.group(1)
            if email in USERS_DB:
                session_id = self.create_session(email)
                user = USERS_DB[email]
                return f"Welcome back, {user['name']}! You're now logged in.", session_id 
        
        return "Please provide valid login credentials. Example: 'login demo@bank.com'", None
    def format_currency(self, amount):
        return f"${amount:,.2f}"
    
    def get_account_balance(self, user_id, session):
        user = USERS_DB.get(user_id)
        if not user:
            return "User not found."
        
        balances = []
        for acc_id, acc_data in user['accounts'].items():
            balances.append(
                f"{acc_data['type'].title()} Account ({acc_data['account_number']}): {self.format_currency(acc_data['balance'])}"
            )
        
        return "Your account balances:\n\n" + "\n".join(balances)
    
    def get_transactions(self, user_id, session):
        user = USERS_DB.get(user_id)
        if not user:
            return "User not found."
        
        all_transactions = []
        for acc_id, acc_data in user['accounts'].items():
            for trans in acc_data['transactions'][-5:]:  # Last 5 transactions
                all_transactions.append(
                    f"{trans['date']} - {trans['type'].title()}: {self.format_currency(trans['amount'])} - {trans['description']}"
                )
        
        return "Recent transactions:\n\n" + "\n".join(all_transactions)
    
    def handle_transfer(self, message, user_id, session):
        # Extract transfer details (simplified)
        amount_match = re.search(r'(?:\$|dollar)?(\d+(?:,\d{3})*(?:\.\d{2})?)', message)
        account_match = re.search(r'to\s+(savings|checking)', message)
        
        if amount_match and account_match:
            amount = float(amount_match.group(1).replace(',', ''))
            to_account = account_match.group(1)
            
            # Simulate transfer (simplified)
            return f"Transfer of {self.format_currency(amount)} to {to_account} account initiated. You'll receive a confirmation shortly."
        
        return "Please specify the amount and account type. Example: 'transfer $500 to savings'"
    
    def handle_card_info(self, user_id, session):
        user = USERS_DB.get(user_id)
        if not user:
            return "User not found."
        
        card_info = []
        for card in user['cards']:
            card_info.append(
                f"{card['type'].title()} Card ({card['number']})\n"
                f"Balance: {self.format_currency(card['balance'])}\n"
                f"Credit Limit: {self.format_currency(card['limit'])}\n"
                f"Available Credit: {self.format_currency(card['limit'] - card['balance'])}"
            )
        
        return "Your card information:\n\n" + "\n\n".join(card_info)
    
    def handle_loan_info(self, user_id, session):
        user = USERS_DB.get(user_id)
        if not user:
            return "User not found."
        
        loan_info = []
        for loan in user['loans']:
            loan_info.append(
                f"{loan['type'].title()} (ID: {loan['id']})\n"
                f"Balance: {self.format_currency(loan['balance'])}\n"
                f"Monthly Payment: {self.format_currency(loan['monthly_payment'])}\n"
                f"Next Due: {loan['next_due']}"
            )
        
        return "Your loan information:\n\n" + "\n\n".join(loan_info)
    
    def get_branch_info(self):
        # Simulated branch information
        return ("Nearest Branch Locations:\n\n"
                "1. Main Street Branch\n   123 Main St, Downtown\n   Open: Mon-Fri 9AM-5PM\n\n"
                "2. Westfield Mall Branch\n   Westfield Shopping Center\n   Open: Mon-Sat 10AM-8PM")
    
    def get_atm_info(self):
        # Simulated ATM information
        return ("Nearest ATM Locations:\n\n"
                "1. 7-Eleven Store - 0.3 miles\n"
                "2. Gas Station - 0.5 miles\n"
                "3. Shopping Mall - 0.8 miles\n\n"
                "All ATMs available 24/7")
    
    def process_message(self, message, session_id=None):
        session = self.get_session(session_id) if session_id else None
        
        # Detect intent
        intent = self.detect_intent(message)
        
        # Handle authentication
        if intent == 'login':
            return self.handle_login(message, session_id)
        
        if intent == 'logout' and session:
            self.sessions.pop(session_id, None)
            return "You have been logged out successfully.", None
        
        # Require login for most operations
        if not session and intent != 'help' and intent != 'unknown':
            return random.choice(self.responses['need_login']), None
        
        # Process authenticated requests
        if session and 'user_id' in session:
            user_id = session['user_id']
            
            if intent == 'balance':
                return self.get_account_balance(user_id, session), session_id
            
            elif intent == 'transactions':
                return self.get_transactions(user_id, session), session_id
            
            elif intent == 'transfer':
                return self.handle_transfer(message, user_id, session), session_id
            
            elif intent == 'card_balance' or intent == 'card_info':
                return self.handle_card_info(user_id, session), session_id
            
            elif intent == 'loan_info':
                return self.handle_loan_info(user_id, session), session_id
        
        # Handle non-authenticated requests
        if intent == 'branch':
            return self.get_branch_info(), session_id
        
        elif intent == 'atm':
            return self.get_atm_info(), session_id
        
        elif intent == 'help':
            return self.get_help_message(), session_id
        
        elif intent == 'interest_rates':
            return self.get_interest_rates(), session_id
        
        elif intent == 'unknown':
            if session:
                return ("I can help you with:\n"
                       "• Check account balance\n"
                       "• View recent transactions\n"
                       "• Transfer money\n"
                       "• Card information and payments\n"
                       "• Loan information\n"
                       "• Find nearest branch or ATM\n\n"
                       "What would you like to do?"), session_id
            else:
                return random.choice(self.responses['greeting']), session_id
        
        return "How else can I assist you today?", session_id
    
    def get_help_message(self):
        return ("I'm here to help you with your banking needs:\n\n"
                "🔐 ACCOUNT SERVICES\n"
                "• Login/logout\n"
                "• Check balance\n"
                "• View transactions\n"
                "• Transfer money\n\n"
                "💳 CARD SERVICES\n"
                "• Check card balance\n"
                "• View credit limit\n"
                "• Make card payments\n\n"
                "🏛️ INFORMATION\n"
                "• Find branches\n"
                "• Locate ATMs\n"
                "• Interest rates\n"
                "• Loan information\n\n"
                "📞 SUPPORT\n"
                "• Report issues\n"
                "• File complaints\n"
                "• Customer service\n\n"
                "Type any request to get started!")
    
    def get_interest_rates(self):
        return ("Current Interest Rates:\n\n"
                "💰 SAVINGS ACCOUNTS\n"
                "• Regular Savings: 2.5% APY\n"
                "• High-Yield Savings: 4.5% APY\n"
                "• Money Market: 3.8% APY\n\n"
                "🏠 LOANS\n"
                "• Mortgage (30-year): 6.8%\n"
                "• Car Loan: 5.5%\n"
                "• Personal Loan: 8.9%\n\n"
                "💳 CREDIT CARDS\n"
                "• Standard: 18.9%\n"
                "• Rewards: 19.9%\n"
                "• Cash Back: 17.9%\n\n"
                "Rates are subject to change.")

# Create chatbot instance
chatbot = BankingChatbot()

@app.route('/')
def index():
    return render_template('banking_index.html')

@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.json.get('message', '')
    session_id = request.json.get('session_id', None)
    
    response, new_session_id = chatbot.process_message(user_message, session_id)
    
    return jsonify({
        'response': response,
        'session_id': new_session_id
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)