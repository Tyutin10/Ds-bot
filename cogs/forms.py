import disnake
from disnake.ext import commands
from disnake import TextInputStyle



class MyModal(disnake.ui.Modal):
    
    def __init__(self):
        components = [disnake.ui.TextInput(label="Ваш текст", placeholder="Введите текст здесь...", custom_id="user_text", style=TextInputStyle.short, max_length=100, min_length=3, required=True)]
        super().__init__(title="Введите текст", custom_id="my_modal", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        if "https://shikimori.io/animes/" in inter.values["user_text"]:
             user_text = inter.values["user_text"]
             await inter.response.send_message(f"'Это ссылка шикомори -' {user_text}")
        else: 
            user_text = inter.values["user_text"]
            await inter.response.send_message(f"Кто-то написал: {user_text}")

class MyView(disnake.ui.View):
    
    def __init__(self):
        super().__init__(timeout=180)

    @disnake.ui.button(label="Открыть форму", style=disnake.ButtonStyle.primary)
    async def open_modal(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(MyModal())

class Form(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='forms', description="Создать форму")
    async def start(self, interaction: disnake.CommandInteraction):
        view = MyView()
        embed = disnake.Embed(title="Форма", description="Нажмите на кнопку, чтобы открыть форму!")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)




def setup(bot):
    bot.add_cog(Form(bot))

