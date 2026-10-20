import discord
import AdminSettings

class Counting():
    def __init__(self):
        print("Counting manager is ready, piggy.")
    async def run(self, message, bot, settings_manager):
        if str(message.guild.id) in settings_manager.servers:
            if 'counting_channel' in settings_manager.servers[str(message.guild.id)]:
                if message.channel.id == settings_manager.servers[str(message.guild.id)]['counting_channel']:
                    print("Message is in counting channel")
                    messages = [m async for m in message.channel.history(limit=2)]
                    previous = messages[1]
                    current = messages[0]
                    print("Grabbed required messages to compair.")

                    try:
                        previous = int(previous.content)
                        current = int(current.content)
                        print("Converted messages to int.")
                    
                        if current != previous + 1:
                            await message.delete()
                            print("Message invalid, piggy")
                        else:
                            print("Congrats, piggy! Your not as dumb as you look, oink oink!")

                    except ValueError:
                        print("the message is not a number, piggy!")
                        await message.delete()
