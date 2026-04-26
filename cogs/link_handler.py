import disnake
from disnake.ext import commands
from config import Config
import requests
from bs4 import BeautifulSoup
from datetime import datetime



class LinkHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.config.get_config('config.json')

    async def handle_link(self, inter: disnake.ModalInteraction, url: str):

        # 👉 Шикимори
        if "shikimori.io/animes/" in url:
            await self.handle_shikimori(inter, url)
            return

        # 👉 Если ссылка, но неизвестная
        await inter.response.send_message("❓ Неизвестный тип ссылки")

        # 🔥 отдельный метод под шикимори
    async def handle_shikimori(self, inter, url):

        target_channel_id = int(self.config.Channels_id["anime"])

        try:
            target_channel = await self.bot.fetch_channel(target_channel_id)
        except disnake.NotFound:
            await inter.response.send_message("❌ Канал не найден")
            return
        except disnake.Forbidden:
            await inter.response.send_message("❌ Нет доступа")
            return

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            await inter.response.send_message(f"❌ Ошибка запроса: {e}")
            return

        soup = BeautifulSoup(response.text, "lxml")

        # 🔹 Название
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Без названия"

        # 🔹 Постер (ВАЖНО: правильный селектор)
        poster_tag = soup.select_one(".c-poster img")
        poster = poster_tag.get("src") if poster_tag else None

        # 🔹 Информация
        result = {}

        info_block = soup.select_one("div.c-info-left div.b-entry-info")
        if info_block:
            lines = info_block.select("div.line-container > div.line")

            for line in lines:
                key_tag = line.select_one(".key")
                value_tag = line.select_one(".value")

                if not key_tag or not value_tag:
                    continue

                key = key_tag.get_text(strip=True).replace(":", "")

                time_tag = value_tag.select_one(".local-time")
                status_tag = value_tag.select_one(".b-anime_status_tag")

                if status_tag and status_tag.has_attr("data-text"):
                    status_text = status_tag["data-text"]
                    rest_text = value_tag.get_text(" ", strip=True)
                    value = f"{status_text} {rest_text}".strip()

                elif time_tag:
                    dt = time_tag.get("data-datetime")

                    if dt:
                        parsed = datetime.fromisoformat(dt)

                        months = [
                            "янв.", "фев.", "мар.", "апр.", "мая", "июн.",
                            "июл.", "авг.", "сен.", "окт.", "ноя.", "дек."
                        ]

                        value = f"{parsed.day} {months[parsed.month-1]} {parsed.strftime('%H:%M')}"
                    else:
                        value = "Неизвестно"

                else:
                    value = value_tag.get_text(" ", strip=True)

                result[key] = value

        # 🔹 Формируем текст инфы
        info_text = ""
        for k, v in result.items():
            info_text += f"**{k}:** {v}\n"

        # 🔥 Embed
        embed = disnake.Embed(
            title=title,
            description=info_text[:4000],  # защита от лимита Discord
            color=disnake.Color.blue(),
            url=url
        )

        if poster:
            embed.set_image(url=poster)

        embed.set_footer(text=f"Отправил: {inter.author}")

        # 🔹 Отправка
        await target_channel.send(embed=embed)
        await inter.response.send_message("✅ Готово!")


def setup(bot):
    bot.add_cog(LinkHandler(bot))