import discord
import json

class StalkingManager():
    def __init__(self, stalkers_json):
        self.stalkers_json = stalkers_json
        with open(self.stalkers_json, 'r') as stalkers_file:
            self.stalkers = json.load(stalkers_file)
        self.stalkers = {int(key): value for key, value in self.stalkers.items()}
    async def notify_stalkers(self, message, user_obj, bot):
        for stalker in self.stalkers:
            stalker_obj = bot.get_user(stalker)
            if user_obj.id in self.stalkers[stalker]:
                print("user found in the list of a stalker.")
                await stalker_obj.send(message)
                print("the dm has been sent.")    
    def save(self):
        with open(self.stalkers_json, 'w') as stalkers_file:
            json.dump(self.stalkers, stalkers_file, indent=4)
    async def check_status(self, before, after, bot):
        print("event fired.")
        if before.status != after.status:
            print("statis has actually changed.")
            if after.status == discord.Status.online:
                print("user is online.")
                await self.notify_stalkers(f'{after.display_name} is online, you crazy stalker!', after, bot)
                if after.activity != None:
                    if after.activity.name == 'Minecraft':
                        await self.notify_stalkers(f'{after.display_name} is playing {after.activity.name}, you crazy stalker', after, bot)
                    if after.activity.name == 'VRChat':
                        await self.notify_stalkers(f'{after.display_name} is playing {after.activity.name}, you crazy stalker', after, bot)
                    
    async def check_profile_changes(self, before, after, bot):
        if before.display_name != after.display_name:
            await self.notify_stalkers(f'{before.display_name} has changed their display name to {after.display_name}, you crazy stalker!', after, bot)
        if before.avatar != after.avatar:
            await self.notify_stalkers(f'{after.display_name} has changed their avatar, you crazy stalker!', after, bot)
    async def stalk_command(self, ctx, bot):
        if len(ctx.message.mentions) == 0:
            await ctx.send("You need to mension someone to watch, you crazy stalker!")
            return
        if len(ctx.message.mentions) == 1:
            stalker = ctx.author.id
            target = ctx.message.mentions[0].id
            if stalker not in self.stalkers:
                self.stalkers[stalker] = []
            if target not in self.stalkers[stalker]:
                self.stalkers[stalker].append(target)
                await ctx.send(f"{ctx.author.name} is now stalking {ctx.message.mentions[0].name}")
            else:
                await ctx.send("You are already stalking this user!")

        self.save()
    async def unstalk_command(self, ctx, bot):
        stalker = ctx.author.id
        if stalker in self.stalkers:
            if len(self.stalkers[stalker]) == 0:
                await ctx.send("You are not currently stalking anyone")
                return

            if len(ctx.message.mentions) == 0:
                await ctx.send("you need to mention somebody to stop stalking!")
                return
            if len(ctx.message.mentions) == 1:
                target = ctx.message.mentions[0].id
                if target in self.stalkers[stalker]:
                    self.stalkers[stalker].remove(target)
                    await ctx.send(f"You are no longer stalking {ctx.message.mentions[0].name}!")
                else:
                    await ctx.send(f"You are currently not stalking {ctx.message.mentions[0].name}")
        else:
            await ctx.send("You are not currently stalking anyone")
        self.save()
    async def list_command(self, ctx, bot):
        stalker = ctx.author.id
        list_str = f"{ctx.author.mention} is stalking the following users:\n"
        if stalker in self.stalkers:
            if len(self.stalkers[stalker]) > 0:
                for target in self.stalkers[stalker]:
                    target_obj = bot.get_user(target)
                    list_str += f"{target_obj.display_name}\n"
                list_str += "You really are a crazy stalker after all!"
                await ctx.send(list_str)
            else:
                await ctx.send(f"{ctx.author.mention} is not currently stalking anyone! Good for them!")
        else:
            await ctx.send(f"{ctx.author.mention} is not even a registered stalker!")