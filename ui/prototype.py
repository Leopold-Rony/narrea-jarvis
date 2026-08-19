from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container


class NarreaPrototype(App):
    """Premier prototype TUI pour Naræa."""


    CSS = """
    #main {
        align: center middle;
        }
    #titre {
        text-align: center;
        text-style: bold;
        color: green;
        }
        """
    BINDING = [("q", "quit" ,"Quitter")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main"):
            yield Static("N A R Æ A", id="titre")
            yield Static("Systeme en ligne. En attente d'ordres...")
        yield Footer()


if __name__ == "__main__":
    app=NarreaPrototype()
    app.run()















































