import asyncio
from datetime import datetime
from app.portfolio import calculate_invincible_portfolio, calculate_invincible_portfolio2



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
                # if now.minute % 5 == 0:
                    print(now, "exec calculate_invincible_portfolio() job")
                    calculate_invincible_portfolio()
                    print(now, "exec calculate_invincible_portfolio2() job")
                    calculate_invincible_portfolio2()

            self.min = now.minute
            self.hour = now.hour
            
            await asyncio.sleep(60)