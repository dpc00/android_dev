from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, OptionList

sli = None


class OptionListApp(App[None]):
    CSS_PATH = "selection_list.tcss"

    def __init__(self, lst):
        self.lst = lst
        super().__init__()

    def compose(self) -> ComposeResult:
        global sli
        yield Header()
        sli = OptionList(*self.lst)
        yield sli
        yield Button("Accept", id="accept")
        yield Button("Abort", id="abort")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(OptionList).border_title = "Select best guess for entity name:"

    @on(Button.Pressed, "#accept")
    def button_pressed1(self, evt):
        global sli
        self.exit(sli.highlighted_option.prompt)

    @on(Button.Pressed, "#abort")
    def button_pressed2(self, evt):
        global sli
        self.exit(None)


cnl = ["a", "b", "c"]


def main(lst):
    return OptionListApp(lst).run()


if __name__ == "__main__":
    print(main(cnl))
