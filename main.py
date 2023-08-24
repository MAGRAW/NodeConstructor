import wx
from examples import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = wx.App()

    frame = MyFrame(None, title="Hello")
    frame.Centre()
    frame.Show()

    app.MainLoop()
