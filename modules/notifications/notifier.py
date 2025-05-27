import asyncio
import requests
from typing import Optional

class Notifier:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url

    async def send(self, message: str):
        """Send notification via configured channels"""
        print(f"System: {message}")
        
        if self.webhook_url:
            try:
                payload = {"content": f"CLMM Bot: {message}"}
                await asyncio.to_thread(
                    requests.post,
                    self.webhook_url,
                    json=payload,
                    timeout=10
                )
            except Exception as e:
                print(f"Failed to send Discord notification: {str(e)}")

    async def critical_alert(self, message: str):
        """Send high priority alert"""
        await self.send(f"CRITICAL: {message}")
