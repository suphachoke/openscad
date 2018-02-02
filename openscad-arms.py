# coding: utf-8
import wx

class MyPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.frame = parent

        self.cbox = wx.BoxSizer(wx.VERTICAL)
        self.combo = wx.ComboBox(self,choices=['a','b','c'])
        self.cbox.Add(wx.StaticText(self,label="เลือกชิ้นส่วนแขนเทียม:"),0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,10)
        self.cbox.Add(self.combo,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)

        self.combo.Bind(wx.EVT_COMBOBOX,self.onPartSelected)

        self.abox = wx.BoxSizer(wx.VERTICAL)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.cbox,0,wx.CENTER|wx.ALL,10)
        self.box.Add(self.abox,0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        self.SetSizer(self.box)

    def onPartSelected(self,event):
        while self.abox.GetChildren():
            self.abox.Hide(0)
            self.abox.Remove(0)
            self.frame.mainbox.Layout()
        if self.combo.GetValue()=="a":
            self.abox.Add(wx.StaticText(self,label="การตั้งค่า"),0,0,0)
            self.addAboxComponent()
            self.frame.mainbox.Layout()

    def addAboxComponent(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        saveBtn = wx.Button(self,label="บันทึก")
        saveBtn.Bind(wx.EVT_BUTTON,self.onSave)
        hbox.Add(saveBtn,0,0,0)
        self.abox.Add(hbox,0,wx.CENTER,10)

    def onSave(self,event):
        with wx.FileDialog(self,"บันทีกไฟล์​ SCAD (*.scad)",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal()==wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname+".scad",'w') as file:
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'"%pathname)

    def doSaveData(self,file):
        defaultFile = open("models/UnLimbited_Arm_v2.1.scad",'r')
        file.write(defaultFile.read())
        file.close()

class MyFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,600))

        self.mainbox = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        self.mainbox.Add(panel,1,wx.EXPAND)
        self.SetSizer(self.mainbox)

        self.Show()

app = wx.App(False)
frame = MyFrame(None,'Test')
app.MainLoop()
