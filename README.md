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

win = Window()

widget = Widget(10, 10)

win.add_widget(widget)

win.open()
```