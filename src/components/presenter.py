from textual.widgets import Static, Header, Button, Input, Rule
from textual.containers import Grid, VerticalScroll
from textual import log

from components.chat import Chat, Message, TextInput

from api import DiscordAPI

discordAPI = DiscordAPI()

currentDiscordID = ""

class Presenter(VerticalScroll):
    def compose(self):
        yield Static("")
        
class UserLabel(Static):
    def __init__(self):
        super().__init__(id="UserLabel")

    def compose(self):
        yield Static("Me", id="UserLabelTitle")

class ChannelLabel(Button):
    def __init__(self, label, discordID, type, selfMain, **kwargs):

        super().__init__(**kwargs)
        self.discordID = discordID
        self.selfMain = selfMain

        if type == -1:
            self.label = label
        elif type == 0:
            self.label = "# "+label
        elif type == 2:
            self.label = "🔊 "+label

    async def on_click(self):
        global currentDiscordID

        if currentDiscordID != self.discordID:
            currentDiscordID = self.discordID
            log.info(f"Presenter {self.discordID}")

            chat = self.selfMain.query_one("Chat", Chat)

            chat.remove_children('Message')
            data = await loadMessages(self.discordID)
            textInput = self.selfMain.query_one("TextInput", TextInput)
            textInput.setDiscordID(currentDiscordID)
            for message in data:
                chat.mount(
                    Message(message)
                )

async def loadMessages(channel_id):
    messages = await discordAPI.loadMessages(channel_id)
    data = []
    if messages != None:
        for message in reversed(messages):  # Inverser l'ordre des messages
            data.append({
                "username": message["author"].get("username"),
                "content": message["content"],
                "timestamp": message["timestamp"],
                "id": "id"+str(message["id"])
            })
        return data
    return []
