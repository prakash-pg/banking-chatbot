# Banking Chatbot 🏦

A web-based banking assistant powered by Flask that helps users manage their accounts, check balances, transfer money, and get banking information.

![Banking Chatbot Screenshot] .... click here to know how the project looks like after running the code -> https://github.com/prakash-pg/banking-chatbot/issues/1#issue-3038081442

## Features

- 🔐 **Secure Login System**: User authentication with session management
- 💰 **Account Management**: Check balances, view transactions, transfer funds
- 💳 **Card Services**: View card balances, credit limits, make payments
- 📊 **Loan Information**: Check loan balances and payment schedules
- 🏛️ **Branch Locator**: Find nearest branches and ATMs
- 📈 **Interest Rates**: Get current banking rates
- 🤖 **Natural Language Processing**: Understands various user queries
- ⚡ **Real-time Responses**: Instant chatbot replies with typing indicators

## Demo

Try it out with these credentials:
- **Email**: `demo@bank.com`
- **Command**: `login demo@bank.com`

## Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-chatbot.git
cd banking-chatbot
```

2. Install required packages:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
banking-chatbot/
│
├── app.py              # Main Flask application
├── templates/
│   └── banking_index.html  # Frontend interface
├── README.md
└── screenshots/
    └── chatbot-demo.png
```

## Available Commands

### Authentication
- `login demo@bank.com` - Log into demo account
- `logout` - Sign out

### Account Operations
- `balance` - Check account balances
- `recent transactions` - View transaction history
- `transfer $500 to savings` - Transfer money between accounts

### Card Services
- `card balance` - Check credit card balance
- `credit limit` - View available credit
- `make card payment` - Pay credit card

### Information & Support
- `find nearest branch` - Locate branches
- `ATM locations` - Find nearby ATMs
- `interest rates` - Get current banking rates
- `loan information` - Check loan details
- `help` - See all available commands

## Technical Details

### Built With
- **Flask**: Web framework
- **Python**: Backend logic
- **HTML/CSS/JavaScript**: Frontend interface
- **Regular Expressions**: Natural language processing
- **JSON**: Session and data management

### Key Components

1. **BankingChatbot Class**: Handles all chatbot logic and responses
2. **Session Management**: Maintains user sessions securely
3. **Intent Detection**: Recognizes user queries using regex patterns
4. **Mock Database**: Simulates bank data for demo purposes

### API Endpoints

- `GET /`: Serves the main chatbot interface
- `POST /get_response`: Processes user messages and returns chatbot responses

## Security Features

- Session-based authentication
- Timeout handling
- Secure data handling
- No real banking credentials required
- Privacy-conscious responses

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] Integration with real banking APIs
- [ ] Two-factor authentication
- [ ] Transaction history visualization
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Voice recognition
- [ ] Budget planning features
- [ ] Investment advice

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is a demo application for educational purposes only. Do not use with real banking credentials or in production environments without proper security measures.

## Contact

prakashpgmj@outlook.com




