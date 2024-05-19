import asyncio
import aiohttp
import os
from dotenv import load_dotenv

class DiscordAPI:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("TOKEN")
        if not self.token:
            print("Token non trouvé. Veuillez le définir dans votre fichier .env.")
            return

    async def getFriends(self):
        headers = {"authorization": f"{self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v9/users/@me/channels", headers=headers) as response:
                if response.status == 200:
                    channels_data = await response.json()
                    return channels_data
                else:
                    print("Erreur lors de la récupération des amis.")

    async def getFriendInfo(self, friend_id):
        headers = {"authorization": f"{self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/users/{friend_id}", headers=headers) as response:
                if response.status == 200:
                    friend_data = await response.json()
                    friend_data["avatar_url"] = f"https://cdn.discordapp.com/avatars/{friend_id}/{friend_data['avatar']}.png"
                    return friend_data
                else:
                    print("Erreur lors de la récupération des informations de l'ami.")


    async def sendMessage(self, recipient_id, message):
        headers = {"authorization": f"{self.token}", "content-type": "application/json"}
        payload = {"content": message}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://discord.com/api/v9/channels/{recipient_id}/messages", headers=headers, json=payload) as response:
                if response.status != 200:
                    print("Erreur lors de l'envoi du message.")
                else:
                    print("Message envoyé avec succès.")

    async def loadMessages(self, channel_id):
        headers = {"authorization": f"{self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers) as response:
                if response.status == 200:
                    messages_data = await response.json()
                    return messages_data
                else:
                    print("Erreur lors de la récupération des messages.")

    async def getMeInfo(self):
        headers = {"authorization": f"{self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/users/@me", headers=headers) as response:
                if response.status == 200:
                    messages_data = await response.json()
                    return messages_data
                else:
                    print("Erreur lors de la récupération des messages.")


    async def getServerIcon(self, server_id, server_icon):
        icon_url = f"https://cdn.discordapp.com/icons/{server_id}/{server_icon}.png"
        return icon_url

    async def getServers(self):
        headers = {"authorization": f"{self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v9/users/@me/guilds", headers=headers) as response:
                if response.status == 200:
                    servers_data = await response.json()
                    return servers_data
    
    async def getServerChannels(self, server_id):
        headers = {"authorization": f"{self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://discord.com/api/v9/guilds/{server_id}/channels", headers=headers) as response:
                if response.status == 200:
                    channels_data = await response.json()
                    return channels_data
                else:
                    print("Erreur lors de la récupération des salons.")