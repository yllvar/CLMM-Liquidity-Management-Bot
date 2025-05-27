from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from anchorpy import Provider, Wallet
import os

class SolanaClient:
    def __init__(self, private_key: str, rpc_url: str):
        self.private_key = private_key
        self.rpc_url = rpc_url
        self.keypair = Keypair.from_base58_string(self.private_key)
        self.wallet = Wallet(self.keypair)
        self.client = AsyncClient(self.rpc_url)
        self.provider = Provider(self.client, self.wallet)

    async def close(self):
        await self.client.close()

    async def create_token_account(self, mint):
        """Create associated token account if needed"""
        from solana.rpc.commitment import Confirmed
        from spl.token.async_client import AsyncToken
        from spl.token.constants import TOKEN_PROGRAM_ID

        token_client = AsyncToken(
            self.client,
            mint,
            TOKEN_PROGRAM_ID,
            self.wallet.payer
        )
        
        return await token_client.create_associated_token_account(
            self.wallet.public_key,
            commitment=Confirmed
        )
