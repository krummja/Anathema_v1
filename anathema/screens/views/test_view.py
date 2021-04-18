from screens.views.view import View



class TestView(View):

    def __init__(
            self,
            color_fg=0xFFAAAAAA,
            color_bg=0xFF151515,
            fill=False,
            style='single',
            *args,
            **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.fill = fill
        self.style = style

    def draw(self, console):
        console.print(0, 0, "Hello, world!")

    def handle_input(self, char):
        print(char)
        return True
