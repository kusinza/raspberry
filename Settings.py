import wx
import requests
import threading
APP_EXIT = 1
APP_EXIT = 1
import git
import glob
def dupdatedownload( results, check):
    print("delay")
    import requests
    drivers=glob.glob('drivers/*')
    ploads = {'current': len(drivers), 'total': 25}
    r = requests.get('https://lew6zlwoa6.execute-api.us-east-2.amazonaws.com/raspInnocent', params=ploads)
    import json
    y = json.loads(r.text)
    if len(y["update"])!=0:
        n=0
        strr="Downloading "
        for i in y["update"]:
            results.SetLabel(strr+str(n+1)+"/"+str(len(y["update"])))
            try:
                git.Git("/drivers").clone(i)
            except :
                strr=str(n+1)+" failed\n"+strr
            n=n+1
        if "failed" in strr :
            results.SetLabel("Some drivers failed to download")
        if len(drivers)!=len(glob.glob('drivers/*')):
            check.SetLabel('Install')
            return
    else:
        results.SetLabel("No new drivers available")
    check.SetLabel('Check update')
def updatedownload(results, check):
    print("delay")
    import requests
    ploads = {'current': system_version, 'total': 1}
    r = requests.get('https://lew6zlwoa6.execute-api.us-east-2.amazonaws.com/raspInnocent', params=ploads)
    import json
    y = json.loads(r.text)
    if len(y["update"])!=0:
        n=0
        strr="Downloading "
        for i in y["update"]:
            results.SetLabel(strr+str(n+1)+"/"+str(len(y["update"])))
            try:
                git.Git("~/RaspSetup/system").clone(i)
                config = "system version:"+str(system_version+1)+"\n"

                with open("config", "w") as f:
                    f.write(config)
                    f.close()
                check.SetLabel('Install')
                return

            except :
                strr=str(n+1)+" failed\n"+strr
            n=n+1
            break
        if "failed" in strr :
            results.SetLabel("System update failed to download")
    else:
        results.SetLabel("System up to date")
    check.SetLabel('Check update')
def dupdate( results, check):
    print("delay")
    import requests
    drivers = glob.glob('drivers/*')
    ploads = {'current': len(drivers), 'total': 25}
    r = requests.get('https://lew6zlwoa6.execute-api.us-east-2.amazonaws.com/raspInnocent', params=ploads)
    import json
    y = json.loads(r.text)
    if len(y["update"])!=0:
        results.SetLabel("New Drivers available")
        check.SetLabel("Download")
    else:
        results.SetLabel("No new drivers available")
def sysupdate( results, check):
    print("delay")
    import requests

    ploads = {'current': system_version, 'total': 1}
    r = requests.get('https://lew6zlwoa6.execute-api.us-east-2.amazonaws.com/raspInnocent', params=ploads)
    import json
    y = json.loads(r.text)
    if len(y["update"])!=0:
        results.SetLabel("New System image available")
        check.SetLabel("Download")
    else:
        results.SetLabel("System up to date")
class Settings(wx.Panel):

    def __init__(self, parent,color='#98AFC7',style=wx.SIMPLE_BORDER):
        super(Settings, self).__init__(parent,-1, size=(200,200),style=style)
        self.siser = wx.BoxSizer(wx.VERTICAL)
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        query = wx.StaticText(self, 0, style=wx.ALIGN_CENTER)
        query.SetLabel("System version:  ")
        self.settingSizer = wx.BoxSizer(wx.VERTICAL)
        self.version=query
        self.settingSizer.Add(self.version, 0, wx.ALL | wx.CENTER, 5)
        query = wx.StaticText(self, 0, style=wx.ALIGN_CENTER)
        query.SetLabel("System ")
        self.update=query
        self.checkupdate = wx.Button(self, wx.ID_ANY, 'Check update', (10, 10))
        self.checkupdate.Bind(wx.EVT_BUTTON, self.onCheckU)
        hbx.Add(self.update, 0, wx.ALL | wx.CENTER, 5)
        hbx.Add(self.checkupdate, 0, wx.ALL | wx.CENTER, 5)

        self.settingSizer.Add(hbx, 0, wx.ALL | wx.CENTER, 5)
        hbx = wx.BoxSizer(wx.HORIZONTAL)
        query = wx.StaticText(self, 0, style=wx.ALIGN_CENTER)
        query.SetLabel("Drivers ")
        self.updateD = query
        self.checkupdateD = wx.Button(self, wx.ID_ANY, 'Check update', (10, 10))
        hbx.Add(self.updateD, 0, wx.ALL | wx.CENTER, 5)
        hbx.Add(self.checkupdateD, 0, wx.ALL | wx.CENTER, 5)
        self.settingSizer.Add(hbx, 0, wx.ALL | wx.CENTER, 5)
        query = wx.StaticText(self, 0, style=wx.ALIGN_CENTER)
        query.SetLabel("")
        self.checkupdateD.Bind(wx.EVT_BUTTON, self.onCheckD)

        self.results=query
        self.settingSizer.Add(self.results, 0,wx.LEFT, 10)
        self.siser.Add(self.settingSizer)
        self.SetSizer(self.siser)
        self.SetSize((250,250))
        self.sysupdate=0
        self.Show()


    def onCheckD(self, e):
        if "Down" in self.checkupdateD.GetLabel():
            t = threading.Thread(target=dupdatedownload,
                                 args=(self.results, self.checkupdateD))
            t.setDaemon(True)
            t.start()
            self.results.SetLabel("Downloading please wait")
        else:
            self.results.SetLabel("Checking Driver update")
            t = threading.Thread(target=dupdate,
                                 args=( self.results,self.checkupdateD))
            t.setDaemon(True)
            t.start()
            print("Upload")
    def onCheckU(self, e):
        if "Down" in self.checkupdate.GetLabel():
            self.results.SetLabel("Downloading please wait")
            t = threading.Thread(target=updatedownload,
                                 args=(self.results, self.checkupdateD))
            t.setDaemon(True)
            t.start()
            self.results.SetLabel("Downloading please wait")
        elif "Inst" in self.checkupdate.GetLabel():
            self.checkupdate.Disable()
            self.results.SetLabel("Installing")
            import os
            stream = os.popen('source ~/RaspSetup/system/raspberry/setupu.sh')
            output = stream.read()

            print(output)
        else:
            self.results.SetLabel("Checking System update")
            t = threading.Thread(target=sysupdate,
                                 args=(self.results, self.checkupdate))
            t.setDaemon(True)
            t.start()
    def onUpload(self, e):
        print("Upload")
class Receipt(wx.Panel):

    def __init__(self, parent,color='#98AFC7',style=wx.SIMPLE_BORDER):
        super(Receipt, self).__init__(parent,-1, size=(200,200),style=style)
        self.siser = wx.BoxSizer(wx.VERTICAL)
        self.settingSizer = wx.BoxSizer(wx.VERTICAL)
        query = wx.StaticText(self, 0, style=wx.ALIGN_CENTER)
        query.SetLabel("Total Receipts: ")
        self.total=query
        query = wx.StaticText(self, 0, style=wx.ALIGN_CENTER)
        query.SetLabel("Total Receipts Uploaded: ")
        self.uploaded = query

        button = wx.Button(self, wx.ID_ANY, 'Upload now', (10, 10))
        self.settingSizer.Add(self.total, 0, wx.ALL | wx.LEFT, 10)
        self.settingSizer.Add(self.uploaded, 0, wx.ALL | wx.LEFT, 10)

        self.settingSizer.Add(button, 0, wx.ALL | wx.CENTER, 10)
        button.Bind(wx.EVT_BUTTON, self.onUpload)
        #button = wx.Button(self, wx.ID_ANY, 'Upload now', (10, 10))
        self.siser.Add(self.settingSizer)
        self.SetSizer(self.siser)
        #self.SetSize((200,200))
        self.Show()

    def onUpload(self, e):
        print("Upload")
class MainPanel(wx.Panel):

    def __init__(self, parent,color='#98AFC7',style=wx.SIMPLE_BORDER):
        super(MainPanel, self).__init__(parent,style=style)
        self.siser = wx.BoxSizer(wx.VERTICAL)
        self.settingSizer = wx.BoxSizer(wx.VERTICAL)
        button = wx.Button(self, wx.ID_ANY, 'MainPanel', (10, 10))
        self.settingSizer.Add(button, 0, wx.ALL | wx.CENTER, 10)
        self.siser.Add(self.settingSizer)
        self.SetSizer(self.siser)
        self.SetSize((250,250))
        self.Show()
        self.Layout()

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        settings = wx.MenuItem(fileMenu, 2, '&Settings')
        receipts = wx.MenuItem(fileMenu, 3, '&Receipts')
        #qmi.SetBitmap(wx.Bitmap('exit.png'))
        fileMenu.Append(qmi)
        fileMenu.Append(settings)
        fileMenu.Append(receipts)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.onSetting, id=2)
        self.Bind(wx.EVT_MENU, self.onReceipt, id=3)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.SetSize((350, 250))
        self.SetTitle('POS')
        self.Centre()
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.siser=wx.BoxSizer(wx.VERTICAL)
        self.mainPanel = MainPanel(self.panel)
        #self.settingSizer=wx.BoxSizer(wx.VERTICAL)

        #self.settingSizer.Add(self.settings, 0, wx.ALL | wx.CENTER, 10)
        self.siser.Add(self.panel, 0, wx.ALL | wx.CENTER, 10)
        #self.siser.Add(self.settingSizer)
        #self.panel.SetSizer(self.siser)
        self.SetSizer(self.siser)


        #self.settingSizer.Hide(0)
        self.Layout()
        self.Refresh()
        self.Show()



    def OnQuit(self, e):
        self.Close()
    def onSetting(self, e):
        self.siser.Hide(0)
        self.siser.Remove(0)
        self.settings = Settings(self)
        self.siser.Add(self.settings, 0, wx.CENTER, 10)
        self.siser.Show(0)
        self.Layout()
        self.Refresh()
    def onReceipt(self, e):
        self.siser.Hide(0)
        self.siser.Remove(0)
        self.receipts = Receipt(self)
        self.siser.Add(self.receipts, 0, wx.ALL | wx.CENTER, 10)
        self.siser.Show(0)
        self.Layout()
        self.Refresh()
    def onButton(self, e):
        print("button")
system_version=0

def main():
    config=""

    try:
        with open("config", "r") as f:
            config= f.read()
            f.close()
    except:
        config="system version:1\n"
        i = 1

    with open("config", "w") as f:
        f.write(config)
        f.close()
    system_version=config.split("\n")[0].split(':')[1]
    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
