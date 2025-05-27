# CLMM Liquidity Management Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

A Solana bot for managing concentrated liquidity positions on Raydium's SOL-USDC pool with automatic rebalancing when positions go out of range.

## Features

- 🎯 Opens concentrated liquidity positions with customizable price range
- 🔄 Automatically monitors existing positions
- 💸 Withdraws out-of-range positions
- � Redeploys liquidity to new in-range positions
- 🔔 Discord notifications for important events
- ⚙️ Easy configuration via `.env` file
- 🛡️ Robust error handling and automatic recovery

## Prerequisites

- Python 3.9 or higher
- Solana wallet with funds for transactions
- RPC endpoint (can use public or private RPC)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yllvar/CLMM-Liquidity-Management-Bot.git
cd CLMM-Liquidity-Management-Bot
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on the template:
```bash
cp .env.example .env
```

## Configuration

Edit the `.env` file with your configuration:

```ini
PRIVATE_KEY=your_solana_wallet_private_key
RPC_URL=https://api.mainnet-beta.solana.com  # Or your custom RPC
POOL_ID=58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2  # SOL-USDC pool
DISCORD_WEBHOOK=your_discord_webhook_url
PRICE_RANGE_PERCENT=5  # The percentage range for liquidity
```

### Configuration Options

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `PRIVATE_KEY` | Your Solana wallet private key | `your_base58_private_key` |
| `RPC_URL` | Solana RPC endpoint | `https://api.mainnet-beta.solana.com` |
| `POOL_ID` | Raydium pool ID for SOL-USDC | `58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2` |
| `DISCORD_WEBHOOK` | Discord webhook URL for notifications | `https://discord.com/api/webhooks/...` |
| `PRICE_RANGE_PERCENT` | Price range percentage for liquidity position | `5` (for ±5%) |

## Usage

Run the bot:
```bash
python main.py
```

The bot will:
1. Initialize and check for existing positions
2. Monitor the current price and position range
3. Automatically rebalance when the price moves out of range
4. Send notifications for important events

### Running in Production

For production use, consider running the bot in a process manager like `pm2` or `systemd`. Example with `pm2`:

```bash
pm2 start "python main.py" --name clmm-bot
pm2 save
pm2 startup
```

## How It Works

1. **Initialization**:
   - Connects to Solana using the provided RPC
   - Loads existing positions (if any)
   - Verifies token accounts

2. **Monitoring Loop**:
   - Checks current pool price every minute
   - Verifies if current position is still in range
   - Calculates new range based on configured percentage

3. **Rebalancing**:
   - If price moves out of range:
     - Withdraws current position
     - Collects fees
     - Opens new position centered around current price
   - Notifies about rebalancing events

4. **Error Handling**:
   - Automatic retry on RPC errors
   - Rate limiting to avoid spamming transactions
   - Discord notifications for critical errors

## Customization

You can customize the bot behavior by modifying:

1. **Price Range**: Adjust `PRICE_RANGE_PERCENT` in `.env` to change how wide your liquidity position is
2. **Rebalancing Strategy**: Modify the `rebalance_position` method in `main.py` to implement different allocation strategies
3. **Monitoring Frequency**: Change the sleep duration in the main loop (currently 60 seconds)

## Security Considerations

1. **Private Key Security**:
   - Never commit your `.env` file to version control
   - Consider using a hardware wallet for larger positions
   - Use a dedicated wallet with limited funds

2. **RPC Endpoint**:
   - Using a private RPC is recommended for better reliability
   - Public RPCs may have rate limits

3. **Transaction Safety**:
   - The bot includes slippage protection by default
   - All transactions are verified before submission

## Troubleshooting

### Common Issues

1. **RPC Connection Errors**:
   - Verify your RPC URL is correct
   - Check your internet connection
   - Try a different RPC provider

2. **Insufficient Funds**:
   - Ensure your wallet has enough SOL for transactions
   - The bot needs SOL for transaction fees

3. **Position Not Opening**:
   - Check you have sufficient token balances
   - Verify the pool ID is correct

### Error Messages

| Error | Solution |
|-------|----------|
| `Invalid private key` | Verify your private key in `.env` is correct |
| `RPC connection failed` | Check your RPC URL and internet connection |
| `Insufficient balance` | Fund your wallet with SOL and the tokens you want to provide as liquidity |

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided "as is" without warranty of any kind. Use at your own risk. The authors are not responsible for any losses incurred while using this bot. Always test with small amounts first.
