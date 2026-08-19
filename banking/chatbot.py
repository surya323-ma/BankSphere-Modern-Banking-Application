"""
Simple rule-based BankSwift assistant.
Keyword-matched intents; personalized where a user is available.
"""
import re


def get_bot_response(message, profile=None):
    text = message.lower().strip()

    def has(*words):
        return any(w in text for w in words)

    if has('hi', 'hello', 'hey', 'namaste', 'namaskar'):
        name = profile.user.first_name or profile.user.username if profile else 'there'
        return f"Hello {name}! I'm the BankSwift Assistant. I can help with balance, transfers, transaction history, or account details. What do you need?"

    if has('balance', 'kitna paisa', 'kitne paise', 'account balance'):
        if profile:
            return f"Your current available balance is ₹{profile.balance:,.2f} in account ending {profile.account_number[-4:]}."
        return "Please log in to check your balance."

    if has('transfer', 'send money', 'paise bhejo', 'paisa bhejna', 'how to send'):
        return ("To transfer money: go to Dashboard → Transfer Money, enter the recipient's "
                "account number or username, the amount, and an optional note, then confirm with your password-free quick transfer. "
                "Funds move instantly between BankSwift accounts.")

    if has('history', 'transaction', 'statement', 'recent payments'):
        return "You can view your full transaction history under 'Transactions' in the left menu, with filters by date and type."

    if has('account number', 'my account', 'ifsc'):
        if profile:
            return f"Your account number is {profile.account_number} and IFSC code is {profile.ifsc}."
        return "Please log in to view your account details."

    if has('interest rate', 'fd', 'fixed deposit', 'rd'):
        return "BankSwift Savings Account offers 3.5% p.a. interest, and Fixed Deposits currently offer up to 7.1% p.a. for tenures of 1-2 years (demo rates)."

    if has('block', 'freeze', 'lost card', 'stolen', 'fraud', 'dispute'):
        return "For security concerns, blocked cards, or disputed transactions, please contact BankSwift support at support@bankswift.example or call our 24x7 helpline 1800-123-4567."

    if has('minimum balance', 'charges', 'fee'):
        return "There is no minimum balance requirement on BankSwift Savings Accounts in this demo, and fund transfers between BankSwift users are free of charge."

    if has('bye', 'thanks', 'thank you', 'dhanyavad', 'shukriya'):
        return "You're welcome! Have a great day. Feel free to reach out anytime you need help with BankSwift."

    if re.search(r'\bhelp\b', text):
        return ("I can help you with: checking your balance, transferring money, viewing transaction "
                "history, account details, interest rates, or reporting a lost card. What would you like to know?")

    return ("I'm still learning! I can currently help with balance enquiries, money transfers, "
            "transaction history, account details, and interest rates. Could you rephrase your question?")
