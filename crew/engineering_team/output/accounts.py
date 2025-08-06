import datetime

def get_share_price(symbol: str) -> float:
    """Returns the current price of a share. Test implementation with fixed prices.
    
    Args:
        symbol: The stock symbol to get the price for.
        
    Returns:
        float: The current price of the share.
    """
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol, 0.0)


class Account:
    """A class representing a user's account in a trading simulation platform."""

    def __init__(self) -> None:
        """Initialize a new account with zero balance, no holdings, and no transactions."""
        self.balance = 0.0
        self.transactions = []
        self.holdings = {}
        self.initial_deposit = 0.0
        self.user_id = None

    def create_account(self, user_id: str, initial_deposit: float) -> None:
        """Create a new account with an initial deposit.
        
        Args:
            user_id: The unique identifier for the user.
            initial_deposit: The amount of money to initially deposit into the account.
            
        Raises:
            ValueError: If the initial deposit is not positive or user_id is empty.
        """
        if not user_id or user_id.strip() == "":
            raise ValueError("User ID is required")
        
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be positive")
        
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.transactions.append({
            'type': 'ACCOUNT_CREATION',
            'user_id': user_id,
            'amount': initial_deposit,
            'balance': self.balance,
            'timestamp': datetime.datetime.now()
        })

    def deposit_funds(self, amount: float) -> None:
        """Deposit funds into the account.
        
        Args:
            amount: Amount to deposit into the account.
            
        Raises:
            ValueError: If the deposit amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.transactions.append({
            'type': 'DEPOSIT',
            'amount': amount,
            'balance': self.balance,
            'timestamp': datetime.datetime.now()
        })

    def withdraw_funds(self, amount: float) -> bool:
        """Withdraw funds from the account if sufficient funds exist.
        
        Args:
            amount: Amount to withdraw from the account.
            
        Returns:
            bool: Indicates success or failure of the withdrawal.
            
        Raises:
            ValueError: If the withdrawal amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            return False
        
        self.balance -= amount
        self.transactions.append({
            'type': 'WITHDRAWAL',
            'amount': amount,
            'balance': self.balance,
            'timestamp': datetime.datetime.now()
        })
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """Buy shares if the account balance suffices.
        
        Args:
            symbol: Stock symbol of the shares to buy.
            quantity: Number of shares to buy.
            
        Returns:
            bool: Indicates success or failure of the purchase.
            
        Raises:
            ValueError: If the quantity is not positive or if the stock symbol is invalid.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        price = get_share_price(symbol)
        if price == 0.0:
            raise ValueError(f"Invalid stock symbol: {symbol}")
        
        total_cost = price * quantity
        
        if total_cost > self.balance:
            return False
        
        self.balance -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self.transactions.append({
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'balance': self.balance,
            'timestamp': datetime.datetime.now()
        })
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """Sell shares if enough shares are held.
        
        Args:
            symbol: Stock symbol of the shares to sell.
            quantity: Number of shares to sell.
            
        Returns:
            bool: Indicates success or failure of the sale.
            
        Raises:
            ValueError: If the quantity is not positive or if the stock symbol is invalid.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        
        price = get_share_price(symbol)
        if price == 0.0:
            raise ValueError(f"Invalid stock symbol: {symbol}")
        
        total_value = price * quantity
        
        self.balance += total_value
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transactions.append({
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_value,
            'balance': self.balance,
            'timestamp': datetime.datetime.now()
        })
        return True

    def calculate_portfolio_value(self) -> float:
        """Calculate the total value of the portfolio including shares and available balance.
        
        Returns:
            float: Total current value of the portfolio.
        """
        holdings_value = sum(get_share_price(symbol) * quantity 
                           for symbol, quantity in self.holdings.items())
        return self.balance + holdings_value

    def calculate_profit_loss(self) -> float:
        """Calculate the profit or loss relative to initial deposit.
        
        Returns:
            float: The profit or loss relative to initial deposit.
        """
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """Get the current holdings of the account.
        
        Returns:
            dict: The current holdings of the account (stock symbols with quantities).
        """
        return self.holdings.copy()

    def list_transactions(self) -> list:
        """List all executed transactions.
        
        Returns:
            list: A list of all executed transactions.
        """
        return self.transactions.copy()