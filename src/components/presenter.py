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

async def loadChannel(type, selfApp, id=0):
    presenter = selfApp.query_one("Presenter", Presenter)
    presenter.remove_children('*')

    if type == "friends":
        log("Loading friends")
        friends = await discordAPI.getFriends()
        
        for friend in reversed(friends):
            label = friend["recipients"][0].get("username")
            discordID = friend["id"]
            presenter.mount(
                ChannelLabel(label, discordID, -1, selfApp)
            )
        presenter.mount(Static("", classes="paddingStatic"))
    elif type == "server":
        log("Loading server")
        channels = await discordAPI.getServerChannels(id)
        for channel in reversed(channels):
            label = channel.get("name")
            discordID = channel.get("id")
            type = channel.get("type")
            if type != 4: # 4 = catégorie
                presenter.mount(
                    ChannelLabel(label, discordID, type, selfApp)
                )
        presenter.mount(Static("", classes="paddingStatic"))

async def loadMessages(channel_id):
    messages = await discordAPI.loadMessages(channel_id)
    data = []
    for message in reversed(messages):  # Inverser l'ordre des messages
        data.append({
            "username": message["author"].get("username"),
            "content": message["content"],
            "timestamp": message["timestamp"]
        })
    return data
