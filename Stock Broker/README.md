## Stock Broker

### Usage
Initialize app: `export FLASK_APP=application.py`

API Key: `export API_KEY=pk_ef0fdffb0c5a467f84ca3d9a85612141`

Run app: `flask run`

When the application launches, use the `Register` button to create an account login. 

### Features
**Home Page**: Display's the user's current portfolio, including the amount of cash remaining. There is also a feature to Add or Withdraw Cash. Within $W, money has magical properties and appears or disappears upon command!

**Quote**: Look up a stock by its ticker symbol and get its current share price

**Buy**: Buy a given number of shares of a ticker symbol. The transaction only occurs if it does not exceed the amount of cash the user has.

**Sell**: Sell a given number of shares of a ticker symbol. The transaction only occurs if the number of shares is positive and does not exceed what the user has. 

**History**: Shows the user's transaction history, including the ticker, number of shares, share price, and timestamp.






