from textual.widgets import Static, Header, Button, Input, Rule
from textual.containers import Grid, VerticalScroll
from textual import log

from components.presenter import Presenter, ChannelLabel

from api import DiscordAPI

currentServerId = 0

class Sidebar(VerticalScroll):
    """The sidebar of the application."""

    def __init__(self,selfApp,**kwargs):
        super().__init__(**kwargs)
        self.selfApp = selfApp
    def compose(self):

        yield ButtonSidebar({
            "label": "Friends", 
            "tooltip": "Friends",
            "id": 0
        },selfApp=self.selfApp, id="blue")
        yield Rule(id="SidebarRule",line_style="heavy")

class ButtonSidebar(Button):
    def __init__(self, data, selfApp, **kwargs):
        super().__init__(classes="serverIcon", **kwargs)
        self.label = data["label"]
        self.tooltip = data["tooltip"]
        self.idServ = data["id"]
        self.selfApp = selfApp

    def on_mount(self):
        self.tooltip = self.tooltip

    async def on_click(self):
        global currentServerId
        if currentServerId != self.idServ:
            currentServerId = self.idServ
            if currentServerId == 0:
                await loadChannel("friends", self.selfApp ,self.idServ)
            else:
                await loadChannel("server", self.selfApp ,self.idServ)

async def loadChannel(type, selfApp, id=0):
    presenter = selfApp.query_one("Presenter", Presenter)
    presenter.remove_children('*')
    discordAPI = DiscordAPI()

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