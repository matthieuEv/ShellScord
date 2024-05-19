from textual.widgets import Static, Header, Button, Input, Rule
from textual.containers import Grid, VerticalScroll
from textual import log

from components.presenter import loadChannel

currentServerId = 0

class Sidebar(VerticalScroll):
    """The sidebar of the application."""

    def __init__(self,selfApp,**kwargs):
        super().__init__(**kwargs)
        self.selfApp = selfApp
        log(">selfApp", selfApp)

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
        log(">> selfApp", self.selfApp)

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