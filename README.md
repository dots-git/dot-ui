# dot-ui
An easy to use yet good-looking UI creation framework for Python

## Contents
* [Basics](#basics)
    * [Creating a window](#creating-a-window)
    * [Adding widgets](#adding-widgets)

# Basics
## Creating a window
Creating a Window is as easy as creating a window object and calling open():
```python
from dot_ui import Window

win = Window()

win.open()
```
![Opened Window](https://github.com/dots-git/dot-ui/blob/main/docs/assets/new_window.png?raw=true)

In the constructor you can specify the width, height, title, icon and whether the window should be opened in full screen mode.

## Adding widgets
Adding a widget is no more compicated. You create the widget and add it to the window:
```python
from dot_ui import Window, Widget

win = Window("Demo")

widget = Widget(10, 10)

win.add_widget(widget)

win.open()
```
![Window with widget](https://github.com/dots-git/dot-ui/blob/main/docs/assets/window_with_widget.png?raw=true)

## Changing renderer settings
Some window and widget properties are universal and are controlled by the renderer. You can customize these settings by calling the corresponding setter on the renderer (DotRenderer by default):
```python
from dot_ui import *

DotRenderer.set_corner_radius(0)
DotRenderer.set_shadow_offset(Vector2(-2, -2))
DotRenderer.set_shadow_radius(10)
DotRenderer.set_default_color(Color.GREEN)


win = Window(title="Demo")

widget = Widget(10, 10)

win.add_widget(widget)

win.open()
```
![Changed renderer settings](https://github.com/dots-git/dot-ui/blob/main/docs/assets/changed_renderer_settings.png?raw=true)