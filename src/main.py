from textual.app import App
from textual.widgets import Static, Header, Button, Input, Rule
from textual.containers import Grid, VerticalScroll
from textual import log

from components.sidebar import Sidebar, ButtonSidebar, loadChannel
from components.presenter import Presenter, ChannelLabel, UserLabel
from components.chat import Chat, Message, TextInput
from websocket import WebSocketClient
import asyncio
import os
from dotenv import load_dotenv

from api import DiscordAPI

discordAPI = DiscordAPI()

class Discord(App):
    CSS_PATH = "../textual/app.tcss"

    def compose(self):
        yield Header()
        yield Grid(
            Sidebar(selfApp=self),
            Presenter(),
            Chat(),
            UserLabel(),
            TextInput(),
        )

    async def on_mount(self):
        await getUserInfo(self)
        await getServersInfo(self)
        await loadChannel("friends", selfApp=self)

        load_dotenv()
        self.websocket_client = WebSocketClient(os.getenv("TOKEN"), self.message_handler)
        asyncio.create_task(self.websocket_client.connect())

    async def message_handler(self, message):
        chat = self.query_one("Chat", Chat)
        currentId = self.query_one("TextInput", TextInput).getDiscordID()
        log("currentId", currentId)
        log("message", message)
        if message["d"]["channel_id"] == currentId and message["t"] == "MESSAGE_CREATE":
            chat.append_message({
                "username": message["d"]["author"]["username"],
                "content": message["d"]["content"],
                "timestamp": message["d"]["timestamp"],
                "id": "id"+str(message["d"]["id"])
            })
        if message["t"] == "MESSAGE_DELETE":
            removeId = "id"+str(message["d"]["id"])
            log("delete", removeId)
            chat.remove_children("#"+removeId)

async def getUserInfo(self):
    """Load my user info from Discord.
    """
    meInfo = await discordAPI.getMeInfo()
    meWidget = self.query_one("#UserLabelTitle",Static)
    meWidget.update(meInfo["global_name"])

async def getServersInfo(self):
    """Load servers from Discord.
    """
    serversInfo = await discordAPI.getServers()
    sidebar = self.query_one("Sidebar", Sidebar)
    for server in serversInfo:
        # log.info(f"Server: {server}")
        sidebar.mount(
            ButtonSidebar({
                "label":server["name"][0], 
                "tooltip": server["name"],
                "id": server["id"],
            },selfApp=self)
        )
    sidebar.mount(
        Static("", classes="paddingStatic")
    )

if __name__ == "__main__":
    app = Discord()
    app.run()
