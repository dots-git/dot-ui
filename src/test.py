from dot_ui import *

Input.add_action("Print Delta", Key.D, 0)
Input.add_action(
    "Close", KeyCombination(Key.L_CTRL, Key.Q), KeyCombination(Key.R_CTRL, Key.Q)
)

win = Window(title="Demo")


def input_demo(self: Widget, delta):
    if Input.action_pressed("Print Delta"):
        print(delta)
    
    if Input.action_just_pressed("Close"):
        self.close()


widget = Widget(10, 10)

widget.add_behaviour("Input Demo", input_demo)

win.add_widget(widget)

win.open()
