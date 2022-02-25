import dot_ui
from dot_ui.widgets.base_widget import Widget

win = dot_ui.Window(title='Test')
win.print_fps = True
win.floating_widgets.append(Widget(160, 100, 100, 100))
win.floating_widgets.append(Widget(50, 100, 100, 100))
win.open()