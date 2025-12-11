

from textual.app import App
from textual.reactive import Reactive
from textual.widgets import Label


class Num(Label):
    num = Reactive(0, layout=True)

    def __init__(self, val, **kwargs):
        super().__init__(f"{val}", **kwargs)
        self.num = val

    def render(self):
        return f"{self.num:>8.2f}"


class Test(App):
    def compose(self):
        self.val = Num(4, id="num_label")
        yield self.val

    def on_click(self):
        self.val.num += 1


if __name__ == "__main__":
    app = Test()
    app.run()
