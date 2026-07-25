import discord

class Counting():
    def __init__(self):
        print("Counting manager is ready, piggy.")
    async def run(self, message, bot):
        if message.channel.name == 'counting':
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
