from dot_ui import *

def fetch_data(self: Widget):
    for i in range(10):
        self.add_child(
            Widget(
                text=str(i),
                size=Vector2(100, 100),
                pos=Vector2(i * 100, 0),
                color=WHITE,
            )
        )

List(
    "vertical",

    List(
        "horizontal",
        Button("Button 1"),
        script_fetch_data=fetch_data,
    )
    
).open()