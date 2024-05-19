from textual.widgets import Static, Header, Button, Input, Rule
from textual.containers import Grid, VerticalScroll
from textual import log
from api import DiscordAPI

discordAPI = DiscordAPI()

class Chat(VerticalScroll):
    def compose(self):
        yield Static("")

class TextInput(Input):
    def __init__(self, **kwargs):
        super().__init__(placeholder="Envoyer votre message",type="text", **kwargs)
        self.currentDiscordID = ""

    async def action_submit(self):
        log.info(f"Message sent: {self.value}")
        await discordAPI.sendMessage(self.currentDiscordID, self.value)
        self.value = ""

    def setDiscordID(self, discordID):
        self.currentDiscordID = discordID

class Message(Static):
    def __init__(self, data: str, **kwargs):
        super().__init__(**kwargs,classes="Message")
        self.data = data

    def compose(self):
        import datetime

        name = self.data["username"]
        message = self.data["content"]
        time = datetime.datetime.strptime(self.data["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
        time = time.strftime("%d/%m/%Y %H:%M")
        
        yield Static(f"{name}: {time}\n{message}")