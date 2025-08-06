import unittest
import datetime

def get_share_price(symbol: str) -> float:
    """Test implementation with fixed prices."""
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

    def create_account(self, initial_deposit: float) -> None:
        """Create a new account with an initial deposit."""
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be positive")
        
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.transactions.append({
            'type': 'DEPOSIT',
            'amount': initial_deposit,
            'balance': self.balance,
            'timestamp': datetime.datetime.now()
        })

    def deposit_funds(self, amount: float) -> None:
        """Deposit funds into the account."""
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
        """Withdraw funds from the account if sufficient funds exist."""
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
        """Buy shares if the account balance suffices."""
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
        """Sell shares if enough shares are held."""
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
        """Calculate the total value of the portfolio including shares and available balance."""
        holdings_value = sum(get_share_price(symbol) * quantity 
                       for symbol, quantity in self.holdings.items())
        return self.balance + holdings_value

    def calculate_profit_loss(self) -> float:
        """Calculate the profit or loss relative to initial deposit."""
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """Get the current holdings of the account."""
        return self.holdings.copy()

    def list_transactions(self) -> list:
        """List all executed transactions."""
        return self.transactions.copy()


class TestAccount(unittest.TestCase):
    """Test cases for the Account class."""

    def setUp(self):
        """Set up a fresh account for each test."""
        self.account = Account()

    def test_create_account_valid_deposit(self):
        """Test creating an account with valid initial deposit."""
        self.account.create_account(1000.0)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'DEPOSIT')

    def test_create_account_invalid_deposit(self):
        """Test creating an account with invalid initial deposit."""
        with self.assertRaises(ValueError):
            self.account.create_account(0.0)
        with self.assertRaises(ValueError):
            self.account.create_account(-100.0)

    def test_deposit_funds(self):
        """Test depositing funds into the account."""
        self.account.create_account(1000.0)
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'DEPOSIT')

    def test_deposit_funds_invalid(self):
        """Test depositing invalid amounts."""
        with self.assertRaises(ValueError):
            self.account.deposit_funds(0.0)
        with self.assertRaises(ValueError):
            self.account.deposit_funds(-100.0)

    def test_withdraw_funds_success(self):
        """Test successful withdrawal."""
        self.account.create_account(1000.0)
        result = self.account.withdraw_funds(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'WITHDRAWAL')

    def test_withdraw_funds_failure(self):
        """Test failed withdrawal due to insufficient funds."""
        self.account.create_account(1000.0)
        result = self.account.withdraw_funds(1500.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.transactions), 1)

    def test_withdraw_funds_invalid(self):
        """Test withdrawing invalid amounts."""
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(0.0)
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(-100.0)

    def test_buy_shares_success(self):
        """Test successful share purchase."""
        self.account.create_account(10000.0)
        result = self.account.buy_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 10000.0 - (150.00 * 10))
        self.assertEqual(self.account.holdings['AAPL'], 10)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'BUY')

    def test_buy_shares_insufficient_funds(self):
        """Test failed share purchase due to insufficient funds."""
        self.account.create_account(1000.0)
        result = self.account.buy_shares('GOOGL', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(len(self.account.holdings), 0)
        self.assertEqual(len(self.account.transactions), 1)

    def test_buy_shares_invalid_quantity(self):
        """Test buying shares with invalid quantity."""
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', -5)

    def test_buy_shares_invalid_symbol(self):
        """Test buying shares with invalid symbol."""
        with self.assertRaises(ValueError):
            self.account.buy_shares('INVALID', 10)

    def test_sell_shares_success(self):
        """Test successful share sale."""
        self.account.create_account(10000.0)
        self.account.buy_shares('AAPL', 10)
        initial_balance = self.account.balance
        result = self.account.sell_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance + (150.00 * 5))
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[2]['type'], 'SELL')

    def test_sell_shares_insufficient_shares(self):
        """Test failed share sale due to insufficient shares."""
        self.account.create_account(10000.0)
        self.account.buy_shares('AAPL', 5)
        result = self.account.sell_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(len(self.account.transactions), 2)

    def test_sell_shares_invalid_quantity(self):
        """Test selling shares with invalid quantity."""
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 0)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', -5)

    def test_sell_shares_invalid_symbol(self):
        """Test selling shares with invalid symbol."""
        with self.assertRaises(ValueError):
            self.account.sell_shares('INVALID', 10)

    def test_calculate_portfolio_value(self):
        """Test calculating portfolio value."""
        self.account.create_account(10000.0)
        self.account.buy_shares('AAPL', 10)
        self.account.buy_shares('TSLA', 5)
        expected_value = self.account.balance + (150.00 * 10) + (700.00 * 5)
        self.assertEqual(self.account.calculate_portfolio_value(), expected_value)

    def test_calculate_profit_loss(self):
        """Test calculating profit/loss."""
        self.account.create_account(10000.0)
        self.account.buy_shares('AAPL', 10)
        profit_loss = self.account.calculate_profit_loss()
        expected = (self.account.balance + (150.00 * 10)) - 10000.0
        self.assertEqual(profit_loss, expected)

    def test_get_holdings(self):
        """Test getting holdings."""
        self.account.create_account(10000.0)
        self.account.buy_shares('AAPL', 10)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 10})

    def test_list_transactions(self):
        """Test listing transactions."""
        self.account.create_account(10000.0)
        self.account.buy_shares('AAPL', 10)
        transactions = self.account.list_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['type'], 'DEPOSIT')
        self.assertEqual(transactions[1]['type'], 'BUY')


class TestGetSharePrice(unittest.TestCase):
    """Test cases for the get_share_price function."""

    def test_get_share_price_valid(self):
        """Test getting valid share prices."""
        self.assertEqual(get_share_price('AAPL'), 150.00)
        self.assertEqual(get_share_price('TSLA'), 700.00)
        self.assertEqual(get_share_price('GOOGL'), 2800.00)

    def test_get_share_price_invalid(self):
        """Test getting invalid share prices."""
        self.assertEqual(get_share_price('INVALID'), 0.0)


if __name__ == '__main__':
    unittest.main()