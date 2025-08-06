import gradio as gr
import datetime
from accounts import Account, get_share_price

account = Account()
account_created = False

def format_transactions(transactions):
    if not transactions:
        return "No transactions yet."
    
    formatted = ""
    for tx in transactions:
        timestamp = tx['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        if tx['type'] == 'DEPOSIT':
            formatted += f"{timestamp} - DEPOSIT: ${tx['amount']:.2f}, Balance: ${tx['balance']:.2f}\n"
        elif tx['type'] == 'WITHDRAWAL':
            formatted += f"{timestamp} - WITHDRAWAL: ${tx['amount']:.2f}, Balance: ${tx['balance']:.2f}\n"
        elif tx['type'] == 'BUY':
            formatted += f"{timestamp} - BUY: {tx['quantity']} {tx['symbol']} @ ${tx['price']:.2f}, Total: ${tx['total']:.2f}, Balance: ${tx['balance']:.2f}\n"
        elif tx['type'] == 'SELL':
            formatted += f"{timestamp} - SELL: {tx['quantity']} {tx['symbol']} @ ${tx['price']:.2f}, Total: ${tx['total']:.2f}, Balance: ${tx['balance']:.2f}\n"
    
    return formatted

def format_holdings(holdings):
    if not holdings:
        return "No holdings."
    
    formatted = ""
    total_value = 0.0
    
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        total_value += value
        formatted += f"{symbol}: {quantity} shares @ ${price:.2f} = ${value:.2f}\n"
    
    formatted += f"\nTotal Holdings Value: ${total_value:.2f}"
    return formatted

def create_account(user_id, initial_deposit):
    global account_created
    
    try:
        if not user_id or user_id.strip() == "":
            return "Error: User ID is required"
        
        initial_deposit = float(initial_deposit)
        account.create_account(user_id, initial_deposit)
        account_created = True
        return f"Account created for user {user_id} with initial deposit of ${initial_deposit:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit(amount):
    if not account_created:
        return "Please create an account first."
    
    try:
        amount = float(amount)
        account.deposit_funds(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw(amount):
    if not account_created:
        return "Please create an account first."
    
    try:
        amount = float(amount)
        success = account.withdraw_funds(amount)
        if success:
            return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Insufficient funds. Current balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    if not account_created:
        return "Please create an account first."
    
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        success = account.buy_shares(symbol, quantity)
        if success:
            return f"Successfully bought {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
        else:
            return f"Insufficient funds to buy {quantity} shares of {symbol}. Current balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    if not account_created:
        return "Please create an account first."
    
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        success = account.sell_shares(symbol, quantity)
        if success:
            return f"Successfully sold {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
        else:
            holdings = account.get_holdings()
            current_quantity = holdings.get(symbol, 0)
            return f"Insufficient shares to sell. You have {current_quantity} shares of {symbol}."
    except ValueError as e:
        return f"Error: {str(e)}"

def get_account_summary():
    if not account_created:
        return "Please create an account first."
    
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.calculate_profit_loss()
    profit_loss_str = "profit" if profit_loss >= 0 else "loss"
    
    summary = f"Account Summary:\n"
    summary += f"User ID: {account.user_id}\n"
    summary += f"Cash Balance: ${account.balance:.2f}\n"
    summary += f"Portfolio Value: ${portfolio_value:.2f}\n"
    summary += f"Profit/Loss: ${profit_loss:.2f} ({profit_loss_str})\n\n"
    
    summary += "Current Holdings:\n"
    summary += format_holdings(account.get_holdings())
    
    return summary

def get_transaction_history():
    if not account_created:
        return "Please create an account first."
    
    transactions = account.list_transactions()
    return format_transactions(transactions)

def get_available_stocks():
    return "Available Stocks for Demo:\nAAPL: $150.00\nTSLA: $700.00\nGOOGL: $2800.00"

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Group():
            gr.Markdown("### Create Account")
            with gr.Row():
                user_id_input = gr.Textbox(label="User ID")
                initial_deposit_input = gr.Textbox(label="Initial Deposit ($)")
            create_account_btn = gr.Button("Create Account")
            create_account_output = gr.Textbox(label="Result", interactive=False)
            create_account_btn.click(create_account, inputs=[user_id_input, initial_deposit_input], outputs=[create_account_output])
        
        with gr.Group():
            gr.Markdown("### Deposit & Withdraw")
            with gr.Row():
                with gr.Column():
                    deposit_input = gr.Textbox(label="Amount to Deposit ($)")
                    deposit_btn = gr.Button("Deposit")
                    deposit_output = gr.Textbox(label="Result", interactive=False)
                    deposit_btn.click(deposit, inputs=[deposit_input], outputs=[deposit_output])
                
                with gr.Column():
                    withdraw_input = gr.Textbox(label="Amount to Withdraw ($)")
                    withdraw_btn = gr.Button("Withdraw")
                    withdraw_output = gr.Textbox(label="Result", interactive=False)
                    withdraw_btn.click(withdraw, inputs=[withdraw_input], outputs=[withdraw_output])
    
    with gr.Tab("Trading"):
        gr.Markdown("### Available Stocks")
        gr.Textbox(value=get_available_stocks, interactive=False, every=None)
        
        with gr.Group():
            gr.Markdown("### Buy Shares")
            with gr.Row():
                buy_symbol_input = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
                buy_quantity_input = gr.Textbox(label="Quantity")
            buy_btn = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Result", interactive=False)
            buy_btn.click(buy_shares, inputs=[buy_symbol_input, buy_quantity_input], outputs=[buy_output])
        
        with gr.Group():
            gr.Markdown("### Sell Shares")
            with gr.Row():
                sell_symbol_input = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
                sell_quantity_input = gr.Textbox(label="Quantity")
            sell_btn = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Result", interactive=False)
            sell_btn.click(sell_shares, inputs=[sell_symbol_input, sell_quantity_input], outputs=[sell_output])
    
    with gr.Tab("Portfolio"):
        with gr.Group():
            gr.Markdown("### Account Summary")
            summary_btn = gr.Button("Get Account Summary")
            summary_output = gr.Textbox(label="Account Summary", interactive=False, lines=10)
            summary_btn.click(get_account_summary, inputs=[], outputs=[summary_output])
    
    with gr.Tab("Transactions"):
        with gr.Group():
            gr.Markdown("### Transaction History")
            history_btn = gr.Button("Get Transaction History")
            history_output = gr.Textbox(label="Transactions", interactive=False, lines=15)
            history_btn.click(get_transaction_history, inputs=[], outputs=[history_output])

if __name__ == "__main__":
    demo.launch()