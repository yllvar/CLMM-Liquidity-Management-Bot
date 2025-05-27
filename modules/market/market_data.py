import requests
from solana.pubkey import Pubkey
from typing import Optional, Tuple
import asyncio

class MarketData:
    def __init__(self, pool_id: Pubkey):
        self.pool_id = pool_id
        self.raydium_url = "https://api.raydium.io/v2/sdk/liquidity/mainnet.json"

    async def get_current_price(self) -> float:
        """Get current pool price from Raydium API with error handling"""
        try:
            response = await asyncio.to_thread(
                requests.get,
                self.raydium_url,
                timeout=10
            )
            response.raise_for_status()
            
            pools = response.json().get('official', [])
            pool = next((p for p in pools if str(p.get('id')) == str(self.pool_id)), None)
            
            if not pool:
                raise ValueError(f"Pool {self.pool_id} not found in Raydium API")
                
            return float(pool['price'])
        except Exception as e:
            raise RuntimeError(f"Market data fetch failed: {str(e)}")

    async def calculate_price_range(self, current_price: float, percent_range: float) -> Tuple[float, float]:
        """Calculate price range based on percentage"""
        range_factor = percent_range / 100
        lower = current_price * (1 - range_factor)
        upper = current_price * (1 + range_factor)
        return lower, upper
