import asyncio
from datetime import datetime
from app.portfolio import calculate_invincible_portfolio, calculate_invincible_portfolio2
from app.quote import get_yahoo_quotes


class BackgroundRunner:
    def __init__(self):
        self.min = 0
        self.hour = 0

    async def run_main(self):
        while True:
            now = datetime.now()
            if now.minute != self.min:
                print(now, "checking cron job")

                if now.hour != self.hour and now.hour == 0:
                    print(now, "exec calculate_invincible_portfolio() job")
                    calculate_invincible_portfolio()
                    calculate_invincible_portfolio2()

                    print(now, "get yahoo quote")
                    get_yahoo_quotes()


            self.min = now.minute
            self.hour = now.hour
            
            await asyncio.sleep(5)