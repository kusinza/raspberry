import os
import socket

import cups
import wx
from image_to_text import main_changer
from nfc_erver import connected, startup
import wiringpi
from remote import remote_command
from push_button import push_button_command
from printer import print_function
import nfc
import nfc.snep
import threading
import nfc.tag
import ndef
import nfc
import nfc.snep
import threading
import time
import mimetypes
from pathlib import Path


def nfc_Start_server(clf):
    print("NFC READY")
    try:
        clf.connect(llcp={'on-startup': startup, 'on-connect': connected})
    finally:
        clf.close()


def changeBitmapWorker(parent,i,stop_tread):
    print("delay")
    initial_=stop_tread()
    my_snep_server = None
    global clf
    try:
        print("NFC STAT")
        clf.close()
        clf = nfc.ContactlessFrontend('tty:ttyUSB0:pn532')
        threading.Thread(target=nfc_Start_server, args=(clf,)).start()
        time.sleep(0)
    except:
        print("FAiled")
    if parent.ci==i:
        img1 = wx.Image("transparent.png", wx.BITMAP_TYPE_ANY)
        img1 = img1.Scale(20, 20)
        parent.panel.bitmap = wx.Bitmap(img1)
        #parent.title.SetBitmap(parent.texttitle[1])
        #parent.panel.Image1.SetBitmap(img1.ConvertToBitmap())

        #parent.panel.Refresh()
        #parent.print.Enable(False)
        stop_tread = False
    #clf.close()


def userUART(parent, i, stop_tread):
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen('/dev/ttyUSB1', 9600)
    # wiringpi.serialPuts(serial,'hello world!')
    i = 0
    while 1:
        a = wiringpi.serialDataAvail(serial)
        c = 1
        if a != 0:
            print("New receipts")
            try:
                with open("receipts", "r") as f:
                    i = int(f.read()) + 1
                    f.close()
            except:
                i = 1
            with open("receipts", "w") as f:
                f.write(str(i))
                f.close()
            with open("test" + str(i) + ".txt", "w") as f:
                while c != -1 and a != 0:

                    c = wiringpi.serialGetchar(serial)
                    a = wiringpi.serialDataAvail(serial)
                    if a == 0:
                        time.sleep(0.2)
                        a = wiringpi.serialDataAvail(serial)
                        if a==0:
                            f.close()
                            print("\n Done")
                            break
                    f.write(chr(c))
                    a = 1
            main_changer("test" + str(i) + ".txt", "image" + str(i) + ".png")
            # os.system("mudraw -o image"+str(i)+"%d.png -r 300 test"+str(i)+".xps")
            img1 = wx.Image("image" + str(i) + ".png", wx.BITMAP_TYPE_ANY)  # image"+str(i)+"1
            parent.file_print = "image" + str(i) + ".png"
            img1 = img1.Rotate90(False)
            W, H = parent.panel.GetSize()
            IW = img1.GetWidth()
            IH = img1.GetHeight()
            NewW = W
            if IH > IW:
                Aspect = float(IW) / float(IH)
            else:
                Aspect = float(IH) / float(IW)
            NewH = W * Aspect
            img1 = img1.Scale(W - 10, H - 10)

            parent.panel.bitmap = wx.Bitmap(img1)
            parent.panel.Image1.SetBitmap(img1.ConvertToBitmap())
            parent.panel.Refresh()
            parent.title.SetBitmap(parent.texttitle[0])
            print("here")
            parent.print.Enable(True)
            parent.ci = i
            t = threading.Thread(target=changeBitmapWorker,
                                 args=(parent, i, lambda: stop_tread()))
            t.setDaemon(True)
            t.start()


def serverWorker(parent,i,stop_tread):
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    # create the server socket
    # TCP socket
    s = socket.socket()
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    processes = []
    i=0
    while 1:
        # accept connection if there is any
        print("Waiting connection")
        client_socket, address = s.accept()
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")
        try:
            with open("receipts", "r") as f:
                i = int(f.read()) + 1
                f.close()
        except:
            i=1
        with open("receipts", "w") as f:
            f.write(str(i))
            f.close()
        # receive the file infos
        # receive using client socket, not server socket
        with open("test"+str(i)+".txt", "w") as f:
            a=0
            while 1:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                #print("read: ",bytes_read)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read.decode())
                print('=', end='')
                a = a + len(bytes_read)
            print("  : ",a," bytes")
            #os.system("dir")
            f.close()
            client_socket.close()
            main_changer("test"+str(i)+".txt","image"+str(i)+".png")
            #os.system("mudraw -o image"+str(i)+"%d.png -r 300 test"+str(i)+".xps")
            img1 = wx.Image("image"+str(i)+".png", wx.BITMAP_TYPE_ANY)#image"+str(i)+"1
            parent.file_print="image"+str(i)+".png"
            img1=img1.Rotate90(False)
            W,H = parent.panel.GetSize()
            IW = img1.GetWidth()
            IH = img1.GetHeight()
            NewW = W
            if IH>IW:
                Aspect = float(IW) /float(IH)
            else:
                Aspect = float(IH) / float(IW)
            NewH = W * Aspect
            img1 = img1.Scale(W-10, H-10)
            
            
            parent.panel.bitmap = wx.Bitmap(img1)
            parent.panel.Image1.SetBitmap(img1.ConvertToBitmap())
            parent.panel.Refresh()
            parent.title.SetBitmap(parent.texttitle[0])
            print("here")
            parent.print.Enable(True)
            parent.ci=i
            t = threading.Thread(target=changeBitmapWorker,
                                 args=(parent, i, lambda: stop_tread()))
            t.setDaemon(True)
            t.start()
            
        continue
        received = client_socket.recv(BUFFER_SIZE).decode()
        print(received)
        print(len(received))
        received = client_socket.recv(BUFFER_SIZE).decode()
        print(received)
        print(len(received))
        print("ffff")
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        with open(filename, "w") as f:
            i = 0
            print("Receiving: ", filesize)
            a = 0
            while (i < filesize / 1024):

                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read.decode())
                # update the progress bar
                print('=', end='')
                a = a + len(bytes_read)
                i = i + 1

            print(" ", a, " / ", filesize)

        # close the client socket
        client_socket.close()
        # close the server socket
        # s.close()
        print("done. ")
        img1 = wx.Image("save.png", wx.BITMAP_TYPE_ANY)
        img1 = img1.Scale(350, 550)
        parent.panel.bitmap = wx.Bitmap(img1)

        parent.title.SetBitmap(parent.texttitle[0])
        parent.panel.Refresh()
        parent.print.Enable(True)
        t = threading.Thread(target=changeBitmapWorker,
                                  args=(parent,i, lambda: stop_tread()))
        t.setDaemon(True)
        t.start()
        #pro = subprocess.Popen("mupdf " + filename, stdout=subprocess.PIPE,
        #                       shell=True, preexec_fn=os.setsid)
        #processes.append(pro)


class MyPanel(wx.Panel):

    def __init__(self,parent=None):
        wx.Panel.__init__(self,parent,id=-1,size=(-1,-1),style=wx.BORDER_RAISED)
        self.parent = parent
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.bitmap = None
        self.current_item=0
        self.stop_threads = False
        self.current_item = 0
        box = wx.BoxSizer(wx.HORIZONTAL)
        img1 = wx.Image("transparent.png", wx.BITMAP_TYPE_ANY)
        img1 = img1.Scale(20, 20)
        self.Image1 = wx.StaticBitmap(self, bitmap=img1.ConvertToBitmap())
        box.Add(self.Image1, 1,flag = wx.EXPAND|wx.ALL,border = 3)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)
        self.SetSizer(box)
    def onKey(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.parent.Close()
            print("ESCAPE")
        else:
            event.Skip()

    def OnPaint(self, evt):
        if self.bitmap != None:
            print("image ready")
            #self.Image1.SetBitmap(self.bitmap)
            #dc = wx.BufferedPaintDC(self)
            #dc.Clear()
            #dc.DrawBitmap(self.bitmap, 0,20)
            #dc.DrawRotatedText("Rotated text...", 300, 300, 90)

        else:
            pass
class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(400, 600))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)

        txt = "Waiting"

        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)

        #box.Add(lbl, 0, wx.ALIGN_CENTER)
        self.panel = MyPanel(panel)
        self.ci=0
        simg = wx.Image(150,25,True)
        #Change from black to grey
        simg.Replace(0,0,0,200,200,200)
        self.file_print=""
        bitmap = simg.ConvertToBitmap()
        waitingbitmap = simg.ConvertToBitmap()
        readybitmap = simg.ConvertToBitmap()
        #Write required text
        dc = wx.MemoryDC(bitmap)
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText("PRINT", 5, 0)
        del dc
        dc = wx.MemoryDC(waitingbitmap)
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText("Waiting", 5, 0)
        del dc
        dc = wx.MemoryDC(readybitmap)
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText("Ready", 5, 0)
        del dc
        img = bitmap.ConvertToImage()
        img1 = img.Rotate90(False)
        img = waitingbitmap.ConvertToImage()
        waitingbitmap = img.Rotate90(False)
        img = readybitmap.ConvertToImage()
        readybitmap = img.Rotate90(False)
        readybitmap=readybitmap.ConvertToBitmap()
        waitingbitmap=waitingbitmap.ConvertToBitmap()
        self.texttitle=[readybitmap,waitingbitmap]
        self.title=wx.StaticBitmap(panel, -1, waitingbitmap, (10, 5),
                                   (waitingbitmap.GetWidth(), waitingbitmap.GetHeight()))
        bmp = img1.ConvertToBitmap()
        self.print = wx.BitmapButton(panel, -1, bmp)
        self.print.Enable(False)
        self.print.Bind(wx.EVT_BUTTON, self.printFunc)
        box.Add(self.title, 0, wx.ALIGN_CENTER)
        #box.Add((0, 0), 1, wx.EXPAND)
        
        box_flags = wx.SizerFlags().Expand().Border(wx.ALL, 1).Proportion(1)
        box.Add(self.panel,box_flags)
        box.Add(self.print, 0, wx.ALIGN_CENTER)
        #box.Add((0, 0), 1, wx.EXPAND)
        
        self.t = threading.Thread(target=serverWorker,
                                  args=(self, self.panel.current_item, lambda: self.panel.stop_threads))
        self.t.setDaemon(True)
        self.t.start()
        self.t = threading.Thread(target=userUART,
                                  args=(self, self.panel.current_item, lambda: self.panel.stop_threads))
        self.t.setDaemon(True)
        self.t.start()
        threading.Thread(target=push_button_command).start()
        threading.Thread(target=remote_command).start()
        panel.SetSizer(box)
        self.Centre()
        self.ShowFullScreen(True)
        self.Layout()
        self.Show()
    def onKey(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.Close()
            print("ESCAPE")
        else:
            event.Skip()        

    def printFunc(self, e):
        
        self.panel.stop_threads = True
        self.ci=-1
        self.title.SetBitmap(self.texttitle[1])
        self.print.Enable(False)
        img1 = wx.Image("transparent.png", wx.BITMAP_TYPE_ANY)
        img1 = img1.Scale(20, 20)
        self.panel.bitmap = wx.Bitmap(img1)
        self.panel.Image1.SetBitmap(img1.ConvertToBitmap())
        self.panel.Refresh()
        print_function()


class MainFrame(wx.Frame):
    def __init__(self,id=-1):

        #super().__init__(parent=None, title='Natural Language Template',size=simple_size)
        print(wx.Locale.GetSystemLanguage())
        wx.Locale(60)
        print(wx.Locale.GetSystemLanguage())
        print(wx.GetApp().GetLayoutDirection())
        self.SetLayoutDirection(1)
        #ico = wx.Icon(main_icon, wx.BITMAP_TYPE_ANY)
        #self.SetIcon(ico)
        self.my_sizer=wx.BoxSizer(wx.VERTICAL)
        self.Show()
clf = nfc.ContactlessFrontend()
if __name__ == '__main__':
    app = wx.App()
    Mywin(None, 'Device')
    app.MainLoop()
