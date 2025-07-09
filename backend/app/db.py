import os
import asyncio
import asyncpg
from dotenv import find_dotenv, load_dotenv

# Load .env
load_dotenv(find_dotenv())

MIN_POOL = 5
MAX_POOL = 20
DB_URL = os.getenv("DB_URL")
class Database:
    def __init__(self):
        self.pool = None

    async def init_pool(self): # Create the pool
        self.pool = await asyncpg.create_pool(
            dsn=DB_URL,
            min_size=MIN_POOL,
            max_size=MAX_POOL
        )
        
        await self.pool.execute("SELECT 1") # Test the connection

    async def close(self):  # Close and wait for all connections to finish
        if self.pool:
            await self.pool.close()

async def main():
    db = Database()
    await db.init_pool()
    

    await db.close()
    print("Pool closed.")

if __name__ == "__main__":
    asyncio.run(main())

    