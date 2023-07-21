#coding: gbk
from main.bingAI import BingDingZhen
from main.gui import GUI
import wx

if __name__ == '__main__':
    #BingDingZhen()
    app = wx.App()
    GUI(parent=None, id=-1).Show()
    app.MainLoop()