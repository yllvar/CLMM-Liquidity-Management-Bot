from modules.core.config import Config
from modules.solana.solana_client import SolanaClient
from modules.core.position_manager import PositionManager
from modules.notifications.notifier import Notifier
from modules.market.market_data import MarketData
import asyncio

class CLMMBot:
    def __init__(self):
        # Initialize modules
        self.config = Config()
        self.solana = SolanaClient(self.config.private_key, self.config.rpc_url)
        self.notifier = Notifier(self.config.discord_webhook)
        self.market_data = MarketData(self.config.pool_id)
        self.position_manager = PositionManager(
            self.solana,
            self.config.pool_id
        )
        
        # Track current position
        self.current_position = None

    async def initialize(self):
        """Initialize the bot components"""
        await self.position_manager.initialize(self.solana.client)
        await self.notifier.send("CLMM Bot initialized")

    async def get_current_price(self):
        """Get current price from market data module"""
        return await self.market_data.get_current_price()

    async def calculate_range(self, current_price):
        """Calculate price range using market data module"""
        return await self.market_data.calculate_price_range(
            current_price,
            self.config.price_range_percent
        )

    async def open_new_position(self, amount_sol, amount_usdc):
        """Open a new concentrated liquidity position"""
        current_price = await self.get_current_price()
        lower, upper = await self.calculate_range(current_price)
        
        # Create token accounts if needed
        token_a_account = await self.solana.create_token_account(
            self.position_manager.pool_info.token_a_mint
        )
        token_b_account = await self.solana.create_token_account(
            self.position_manager.pool_info.token_b_mint
        )
        
        # Open position through position manager
        position = await self.position_manager.open_position(
            tick_lower=lower,
            tick_upper=upper,
            token_a_amount=amount_sol,
            token_b_amount=amount_usdc
        )
        
        await self.notifier.send(f"Opened new position: {position}")

    async def check_position_range(self):
        """Check if position is in range using position manager"""
        return await self.position_manager.check_in_range(
            await self.get_current_price()
        )

    async def withdraw_position(self):
        """Withdraw the current position through position manager"""
        if await self.position_manager.withdraw_position():
            await self.notifier.send("Successfully withdrew position")
            self.current_position = None

    async def rebalance_position(self):
        """Rebalance the position if needed"""
        needs_rebalance = await self.check_position_range()
        
        if needs_rebalance:
            await self.notify("Position out of range, rebalancing...")
            
            # Withdraw existing position
            if self.current_position:
                await self.withdraw_position()
            
            # Get current balances
            sol_balance = await self.get_token_balance(self.pool_info.token_a_mint)
            usdc_balance = await self.get_token_balance(self.pool_info.token_b_mint)
            
            # Open new position with 50/50 split (adjust as needed)
            amount_sol = sol_balance * 0.5
            amount_usdc = usdc_balance * 0.5
            
            if amount_sol > 0 and amount_usdc > 0:
                await self.open_new_position(amount_sol, amount_usdc)

    async def get_token_balance(self, mint):
        """Get token balance through position manager"""
        return await self.position_manager.get_token_balance(mint)

    async def notify(self, message):
        """Send notification using Notifier module"""
        await self.notifier.send(message)

    async def run(self):
        """Main bot loop"""
        await self.initialize()
        
        while True:
            try:
                await self.rebalance_position()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                await self.notify(f"Error: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

if __name__ == "__main__":
    bot = CLMMBot()
    asyncio.run(bot.run())
