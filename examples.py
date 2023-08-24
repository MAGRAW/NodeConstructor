import wx

APP_EXIT = 1
VIEW_STATUS = 2
VIEW_RGB = 3
VIEW_SRGB = 4

class AppMDIChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, title, size):
        super().__init__(parent, -1, title=title, size=size)

        self.panel = wx.Panel(self)
        parent.ctx = AppContextMenu(self)
        self.panel.Bind(wx.EVT_RIGHT_DOWN, parent.OnRightDown)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.panel.Unbind(wx.EVT_BUTTON)
        self.Show()

    def onLeftDown(self, event):
        print("Нажатие на левую кнопку мыши")

    def onButton1(self, event):
        print("Нажатие на первую кнопку")

    def onButton2(self, event):
        print("Нажатие на вторую кнопку")

    def onButton(self, event):
        print('Уровень кнопки')
        event.Skip()

    def onButtonPanel(self, event):
        print('Уровень панели')
        event.Skip()

    def onButtonFrame(self, event):
        print('Уровень окна')
        event.Skip()

    def OnCloseWindow(self, event):
        dial = wx.MessageDialog(None, "Вы действительно хотите выйти?", "Вопрос", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            self.Destroy()
        else:
            event.Veto()

    def OnMove(self, event):
        x, y = event.GetPosition()
        self.panel.x.SetLabel('x:' + str(x))
        self.panel.y.SetLabel('y:' + str(y))

    def OnPaint(self, event):
        print("Событие EVT_PAINT")
        dc = wx.PaintDC(self.panel)
        dc.DrawLine(0, 0, 100, 100)

    def OnSetFocus(self, event):
        event.GetEventObject().SetBackgroundColour("#FFFFE5")
        event.Skip()

    def OnKillFocus(self, event):
        event.GetEventObject().SetBackgroundColour("#fff")
        event.Skip()

    def OnKeyDown(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            ret = wx.MessageBox("Вы действительно хотите выйти из программы?", "Вопрос",
                                wx.YES_NO | wx.NO_DEFAULT, self)
            if ret == wx.YES:
                self.Close()

    def OnKeyUp(self, e):
        print('Отпустили кнопку')

class AppContextMenu(wx.Menu):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

        it_min = self.Append(wx.ID_ANY, "Минимизировать")
        it_max = self.Append(wx.ID_ANY, "Распахнуть")
        self.Bind(wx.EVT_MENU, self.onMinimize, it_min)
        self.Bind(wx.EVT_MENU, self.onMaximize, it_max)

    def onMinimize(self, event):
        self.parent.Iconize()

    def onMaximize(self, event):
        self.parent.Maximize()


class MyFrame(wx.MDIParentFrame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        wx_case_Menu(self)

        wx_case_BoxSizer(self)

        wx_case_toolbar(self)

        wx_case_GridSizer(self)

        wx_case_FlexGridSizer(self)

        wx_case_GridBagSizer(self)

        wx_case_propagation(self)

        wx_case_EVT_MOTION(self)






    def OnRightDown(self, event):
        self.PopupMenu(self.ctx, event.GetPosition())

    def onStatus(self, event):
        if self.vStatus.IsChecked():
            print('Показать статусную строку')
        else:
            print('Скрыть статусную строку')

    def onImageType(self, event):
        if self.vRgb.IsChecked():
            print('Режим RGB')
        elif self.vSrgb.IsChecked():
            print('Режим sRGB')

    def onQuit(self, event):
        self.Close()

    def OnMove(self, owner, event):
        x, y = event.GetPosition()
        owner.x.SetLabel('x:' + str(x))
        owner.y.SetLabel('y:' + str(y))

def wx_case_Menu(self):
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()

    expMenu = wx.Menu()
    expMenu.Append(wx.ID_ANY, "Экспорт изображения")
    expMenu.Append(wx.ID_ANY, "Экспорт видео")
    expMenu.Append(wx.ID_ANY, "Экспорт данных")

    fileMenu.Append(wx.ID_NEW, '&Новый\tCtrl+N')
    fileMenu.Append(wx.ID_OPEN, '&Открыть\tCtrl+O')
    fileMenu.Append(wx.ID_SAVE, '&Сохранить\tCtrl+S')
    fileMenu.AppendSubMenu(expMenu, '&Экспорт')
    fileMenu.AppendSeparator()

    # item = wx.MenuItem(fileMenu, wx.ID_EXIT, "Выход\tCtrl+Q", "Выход из приложения")
    item = wx.MenuItem(fileMenu, APP_EXIT, "Выход\tCtrl+Q", "Выход из приложения")
    item.SetBitmap(wx.Bitmap('icons/free-icon-exit-3483569_16.png'))
    fileMenu.Append(item)

    viewMenu = wx.Menu()
    # viewMenu.Append(wx.ID_ANY, 'Статусная строка', kind=wx.ITEM_CHECK)
    self.vStatus = viewMenu.Append(VIEW_STATUS, 'Статусная строка', kind=wx.ITEM_CHECK)
    # viewMenu.Append(wx.ID_ANY, 'Тип RGB', 'Тип RGB', kind=wx.ITEM_RADIO)
    self.vRgb = viewMenu.Append(VIEW_RGB, 'Тип RGB', 'Тип RGB', kind=wx.ITEM_RADIO)
    # viewMenu.Append(wx.ID_ANY, 'Тип sRGB', 'Тип sRGB', kind=wx.ITEM_RADIO)
    self.vSrgb = viewMenu.Append(VIEW_SRGB, 'Тип sRGB', 'Тип sRGB', kind=wx.ITEM_RADIO)

    menubar.Append(fileMenu, "&File")
    menubar.Append(viewMenu, "&Вид")

    self.SetMenuBar(menubar)

    # self.Bind(wx.EVT_MENU, self.onQuit, item)
    self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)
    self.Bind(wx.EVT_MENU, self.onStatus, id=VIEW_STATUS)
    self.Bind(wx.EVT_MENU, self.onImageType, id=VIEW_RGB)
    self.Bind(wx.EVT_MENU, self.onImageType, id=VIEW_SRGB)

def wx_case_BoxSizer(self):
    self.win = AppMDIChildFrame(self, "SetPointSize", (200, 150))
    panel = self.win.panel
    font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
    font.SetPointSize(12)
    panel.SetFont(font)
    vbox = wx.BoxSizer(wx.VERTICAL)
    '''
    img1 = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap("icons/free-icon-python-1826733.png"))
    img2 = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap("icons/free-icon-js-5968292.png"))
    #vbox.Add(img1, wx.ID_ANY, wx.EXPAND)
    #vbox.Add(img2, wx.ID_ANY, wx.EXPAND)
    mp = wx.Panel(panel)
    mp.SetBackgroundColour('#FFFFE5')
    vbox.Add(mp, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
    # img1.SetPosition((10, 10))
    # img2.SetPosition((300, 40))
    '''
    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    st1 = wx.StaticText(panel, label='Путь к файлу:')
    tc = wx.TextCtrl(panel)

    hbox1.Add(st1, flag=wx.RIGHT, border=8)
    hbox1.Add(tc, proportion=1)

    vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    st2 = wx.StaticText(panel, label='Содержимое файла')
    vbox.Add(st2, flag=wx.EXPAND | wx.ALL, border=10)

    tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
    vbox.Add(tc2, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, border=10)

    btnOK = wx.Button(panel, label='Да', size=(70, 30))
    btnCn = wx.Button(panel, label='Отмена', size=(70, 30))

    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    hbox2.Add(btnOK, flag=wx.LEFT, border=10)
    hbox2.Add(btnCn, flag=wx.LEFT, border=10)

    vbox.Add(hbox2, flag=wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, border=10)

    panel.SetSizer(vbox)

def wx_case_toolbar(self):
    # toolbar = self.CreateToolBar()
    # toolbar = self.CreateToolBar(wx.TB_RIGHT)
    # toolbar = self.CreateToolBar(wx.TB_LEFT)
    toolbar = self.CreateToolBar(wx.TB_BOTTOM)
    br_quit = toolbar.AddTool(wx.ID_ANY, "Выход", wx.Bitmap("icons/free-icon-exit-853348_64.png"))
    toolbar.AddSeparator()
    br_undo = toolbar.AddTool(wx.ID_UNDO, "", wx.Bitmap("icons/free-icon-undo-889590.png"))
    br_undo = toolbar.AddTool(wx.ID_REDO, "", wx.Bitmap("icons/free-icon-right-arrow-4028603.png"))
    toolbar.AddSeparator()
    toolbar.AddCheckTool(wx.ID_ANY, "", wx.Bitmap("icons/free-icon-volume-1057102.png"))
    toolbar.AddRadioTool(wx.ID_ANY, "", wx.Bitmap("icons/free-icon-volume-611636.png"))
    toolbar.AddRadioTool(wx.ID_ANY, "", wx.Bitmap("icons/free-icon-volume-1142318.png"))
    toolbar.EnableTool(wx.ID_REDO, False)
    toolbar.Realize()

    self.Bind(wx.EVT_TOOL, self.onQuit, br_quit)

def wx_case_GridSizer(self):
    self.win2 = AppMDIChildFrame(self, "BoxSizer", (600, 350))
    panel = self.win2.panel
    vbox2 = wx.BoxSizer(wx.VERTICAL)

    tc = wx.TextCtrl(panel)
    vbox2.Add(tc, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

    gbox = wx.GridSizer(5, 4, 5, 5)
    gbox.AddMany([(wx.Button(panel, label='Cls'), wx.ID_ANY, wx.EXPAND),
                  (wx.Button(panel, label='Bck'), wx.ID_ANY, wx.EXPAND),
                  (wx.StaticText(panel), wx.EXPAND),
                  (wx.Button(panel, label='Cloce'), 0, wx.EXPAND),
                  (wx.Button(panel, label='7'), 0, wx.EXPAND),
                  (wx.Button(panel, label='8'), 0, wx.EXPAND),
                  (wx.Button(panel, label='9'), 0, wx.EXPAND),
                  (wx.Button(panel, label='/'), 0, wx.EXPAND),
                  (wx.Button(panel, label='4'), 0, wx.EXPAND),
                  (wx.Button(panel, label='5'), 0, wx.EXPAND),
                  (wx.Button(panel, label='6'), 0, wx.EXPAND),
                  (wx.Button(panel, label='*'), 0, wx.EXPAND),
                  (wx.Button(panel, label='1'), 0, wx.EXPAND),
                  (wx.Button(panel, label='2'), 0, wx.EXPAND),
                  (wx.Button(panel, label='3'), 0, wx.EXPAND),
                  (wx.Button(panel, label='-'), 0, wx.EXPAND),
                  (wx.Button(panel, label='0'), 0, wx.EXPAND),
                  (wx.Button(panel, label='.'), 0, wx.EXPAND),
                  (wx.Button(panel, label='='), 0, wx.EXPAND),
                  (wx.Button(panel, label='+'), 0, wx.EXPAND)])
    vbox2.Add(gbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

    panel.SetSizer(vbox2)

def wx_case_FlexGridSizer(self):
    self.win3 = AppMDIChildFrame(self, "FlexGridSizer", (600, 350))
    panel = self.win3.panel
    vbox3 = wx.BoxSizer()

    fb = wx.FlexGridSizer(4, 2, 10, 10)
    fb.AddMany([(wx.StaticText(panel, label='Ф.И.О.')),
                (wx.TextCtrl(panel), wx.ID_ANY, wx.EXPAND),
                (wx.StaticText(panel, label='email:')),
                (wx.TextCtrl(panel), wx.ID_ANY, wx.EXPAND),
                (wx.StaticText(panel, label='Адрес:')),
                (wx.TextCtrl(panel), wx.ID_ANY, wx.EXPAND),
                (wx.StaticText(panel, label='О себе')),
                (wx.TextCtrl(panel, style=wx.NB_MULTILINE), wx.ID_ANY, wx.EXPAND)
                ])
    fb.AddGrowableCol(1, 1)
    # fb.AddGrowableRow(0,1)
    fb.AddGrowableRow(3, 1)
    vbox3.Add(fb, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    panel.SetSizer(vbox3)

def wx_case_GridBagSizer(self):
    self.win4 = AppMDIChildFrame(self, "GridBagSizer", (600, 300))
    gr = wx.GridBagSizer(5, 5)
    panel = self.win4.panel
    text = wx.StaticText(panel, label="Email:")
    gr.Add(text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

    tc = wx.TextCtrl(panel)
    gr.Add(tc, pos=(1, 0), span=(1, 5), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

    button1 = wx.Button(panel, label="Восстановить", size=(120, 28))
    button2 = wx.Button(panel, label="Отмена", size=(90, 28))
    gr.Add(button1, pos=(3, 3))
    gr.Add(button2, pos=(3, 4), flag=wx.RIGHT | wx.BOTTOM, border=10)
    gr.AddGrowableCol(1)
    gr.AddGrowableRow(1)
    # gr.AddGrowableRow(2)
    panel.SetSizer(gr)

def wx_case_propagation(self):
    self.win5 = AppMDIChildFrame(self, "Bind", (600, 300))
    '''
    btn1 = wx.Button(self.win5.panel, wx.ID_ANY, "Кнопка 1")
    btn2 = wx.Button(self.win5.panel, wx.ID_ANY, "Кнопка 2")
    btn1.SetPosition(wx.Point(10, 10))
    btn2.SetPosition(wx.Point(200, 10))
    # PROPAGATION
    ##self.win5.panel.Bind(wx.EVT_BUTTON, self.win5.onButton1, btn1)
    #btn1.Bind(wx.EVT_BUTTON, self.win5.onButton1, btn1)
    self.Bind(wx.EVT_BUTTON, self.win5.onButton1, btn1)
    ##self.win5.panel.Bind(wx.EVT_BUTTON, self.win5.onButton2, btn2)
    #btn2.Bind(wx.EVT_BUTTON, self.win5.onButton2, btn2)
    self.Bind(wx.EVT_BUTTON, self.win5.onButton2, btn2)'''

    btn = wx.Button(self.win5.panel, wx.ID_ANY, "Нажать")
    btn.Bind(wx.EVT_BUTTON, self.win5.onButton)
    self.win5.panel.Bind(wx.EVT_BUTTON, self.win5.onButtonPanel)
    self.win5.Bind(wx.EVT_BUTTON, self.win5.onButtonFrame)

def wx_case_EVT_MOTION(self):
    self.win6 = AppMDIChildFrame(self, "EVT_MOTION", (600, 300))
    panel = self.win6.panel
    # panel.x = wx.StaticText(panel, label='x:', pos=(10, 10))
    # panel.y = wx.StaticText(panel, label='y:', pos=(10, 30))
    # panel.Bind(wx.EVT_MOTION, self.win6.OnMove)

    # panel.Bind(wx.EVT_PAINT, self.win6.OnPaint)

    t1 = wx.TextCtrl(panel)
    t2 = wx.TextCtrl(panel)
    vbox6 = wx.BoxSizer(wx.VERTICAL)
    vbox6.Add(t1, flag=wx.EXPAND | wx.ALL, border=10)
    vbox6.Add(t2, flag=wx.EXPAND | wx.ALL, border=10)
    panel.SetSizer(vbox6)

    t1.Bind(wx.EVT_SET_FOCUS, self.win6.OnSetFocus)
    t1.Bind(wx.EVT_KILL_FOCUS, self.win6.OnKillFocus)
    t2.Bind(wx.EVT_SET_FOCUS, self.win6.OnSetFocus)
    t2.Bind(wx.EVT_KILL_FOCUS, self.win6.OnKillFocus)

    panel.Bind(wx.EVT_KEY_DOWN, self.win6.OnKeyDown)
    panel.Bind(wx.EVT_KEY_UP, self.win6.OnKeyUp)
