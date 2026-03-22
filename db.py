import asyncpg

async def create_user(discord_id, username):
    conn = await asyncpg.connect(
        user='user',
        password='password',
        database='ds_bot',
        host='localhost',
        port=5432
    )
    await conn.execute(
        "INSERT INTO users(discord_id, username) VALUES($1, $2) ON CONFLICT DO NOTHING",
        discord_id, username
    )
    await conn.close()