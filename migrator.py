import asyncio
import asyncpg


DB_CONFIG = {
    "user": "user",
    "password": "password",
    "database": "ds_bot",
    "host": "postgres",  
    "port": 5432,
}


async def run_migrations():
    conn = await asyncpg.connect(**DB_CONFIG)

    print("🔄 Проверка таблиц...")

    # Таблица users
    result = await conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        discord_id BIGINT UNIQUE,
        username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    print(f"📦 users: {result}")

    # Таблица tasks
    result = await conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    print(f"📦 tasks: {result}")

    await conn.close()
    print("✅ Миграции применены")


if __name__ == "__main__":
    asyncio.run(run_migrations())