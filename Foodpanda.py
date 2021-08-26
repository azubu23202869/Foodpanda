#coding:utf-8
import logging
import os
import random
import string
import subprocess
import threading
import time
import tkinter as tk
from time import sleep
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import win32clipboard as w
import win32con
import ScreenShot
import webbrowser
import os
# https://www.foodpanda.com.tw/login/new?step=email
logging.basicConfig(level=logging.INFO, filename='Foodpanda帳號儲存.log', format='%(asctime)s - %(message)s')


class Threader(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()
        self.wnd = tk.Toplevel()
        self.wnd.title('日誌')
        self.wnd.geometry('400x200')
        self.wnd.resizable(0, 0)
        self.Txt1 = ScrolledText(self.wnd, font=("consolas", "14", "normal"))
        self.setT("請等待10秒，窗口會自動消失!!!!\n", self.Txt1)
        self.Txt1.pack(fill=tk.BOTH)

    def run(self):
        proc = subprocess.Popen('run.bat', shell=True, stdout=subprocess.PIPE)
        proc.communicate()
        if proc.poll() == 0:
            # self.setT(subprocess.getoutput('ipconfig | find /i "IPv4"'), self.Txt1)
            sleep(3)
            self.wnd.destroy()

    def setT(self, textvar, inScrolledText):
        inScrolledText.configure(state="normal")
        inScrolledText.insert("end", textvar)
        inScrolledText.see("end")
        inScrolledText.configure(state="disabled")



class Foodpanda(object):
    def __init__(self):
        self.content_state = False
        self.content_savestate = False
        self.w_size = 600
        self.h_size = 400
        self.logger = logging.getLogger(__name__)
        self.root = tk.Tk()
        self.root.title('Foodpanda帳號產生器')
        self.root.geometry('600x400')
        self.root.resizable(0, 0)
        self.backframe = tk.Frame(master=self.root, width=self.w_size, height=self.h_size)
        self.backframe.pack()
        self.backframe.propagate(0)

        # self.handle = {}
        # self.handle["control"] = 1

        # 區域1 帳號顯示
        self.div1 = tk.Frame(master=self.backframe)
        self.lb_view = tk.Label(self.div1, text="", font=('consolas', 18))
        self.lb_view.pack(padx=10, pady=5, fill=tk.BOTH, side=tk.TOP)
        self.bt_copyacc = tk.Button(self.div1, text="複製", command=self.copy_acc, width=5, height=2, state=tk.DISABLED)
        self.bt_copyacc.place(x=450)
        self.div1.pack(fill=tk.X, side=tk.TOP)


        # 區域2 按鈕區
        self.div2 = tk.Frame(master=self.backframe)
        self.bt_open = tk.Button(self.div2, text="開啟網頁", command=self.openweb, width=14, height=2)
        self.bt_open.pack(padx=5, pady=5, side=tk.LEFT)
        self.bt_create = tk.Button(self.div2, text="點擊產生帳號", command=self.new_acc, width=14, height=2)
        self.bt_create.pack(padx=5, pady=5, side=tk.LEFT)
        self.bt_saveacc = tk.Button(self.div2, text="確認下單", command=self.saveacc, width=14, height=2, state=tk.DISABLED)
        self.bt_saveacc.pack(padx=5, pady=5, side=tk.LEFT)
        self.bt_screens = tk.Button(self.div2, text="截圖(Enter複製)", command=self.Screenshot, width=14, height=2)
        self.bt_screens.pack(padx=5, pady=5, side=tk.LEFT)
        self.div2.pack(padx=10, pady=5, side=tk.TOP)

        # 區域3 按鈕區2
        self.div3 = tk.Frame(master=self.backframe)
        self.bt_changeip = tk.Button(self.div3, text="無法創建帳號點我", command=lambda: Threader(name='ChangeIP'), width=14, height=2)
        self.bt_changeip.pack(padx=5, pady=5, side=tk.LEFT)
        # self.bt_openTxt = tk.Button(self.div3, text="開啟紀錄檔", command=self.openLog, width=14, height=2)
        # self.bt_openTxt.pack(padx=5, pady=5, side=tk.LEFT)
        self.div3.pack(padx=10, pady=5,  side=tk.TOP)

        # 區域4 LOG
        self.div4 = tk.Frame(master=self.backframe)
        self.lb_1 = tk.Label(self.div4, text="帳號記錄", font=('consolas', 14)).pack()
        self.log_widget = ScrolledText(self.div4, height=10, font=("consolas", "8", "normal"))
        self.log_widget.pack(side=tk.TOP)
        self.bt_openTxt = tk.Button(self.div4, text="開啟紀錄檔(查找帳號請點這!!!!)", command=self.openLog, width=14, height=2, bg='yellow')
        self.bt_openTxt.pack(side=tk.TOP, fill=tk.X)
        self.div4.pack(padx=10, pady=5,  side=tk.BOTTOM)


        # 區域5 SAVEACC
        # self.div5 = tk.Frame(master=self.backframe)
        # self.lb_2 = tk.Label(self.div5, text="已使用帳號", font=('Arial', 10)).pack()
        # self.log_widget_saveacc = ScrolledText(self.div5, width=42, height=5, font=("consolas", "8", "normal"))
        # self.log_widget_saveacc.pack(side=tk.LEFT)
        # self.div5.pack(padx=10, pady=5, side=tk.LEFT)

        self.root.mainloop()

    def new_acc(self):
        if self.content_state:
            MsgBox = tk.messagebox.askquestion('帳號產生', '是否要產生新帳號?')
            if MsgBox == 'yes':
                self.create_acc()
        else:
            self.create_acc()

    def create_acc(self):
        acc = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        acc += '@gmail.com'
        self.lb_view['text'] = acc
        self.check_lb_view_content()
        self.showinfo(acc, self.log_widget)
        self.logger.info(acc)
        self.content_savestate = False
        return acc

    def copy_acc(self):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, self.lb_view['text'])
        w.CloseClipboard()

    def check_lb_view_content(self):
        if self.lb_view['text'] == '':
            self.content_state = False
            self.bt_copyacc['state'] = tk.DISABLED
            self.bt_saveacc['state'] = tk.DISABLED
        else:
            self.content_state = True
            self.bt_copyacc['state'] = tk.NORMAL
            self.bt_saveacc['state'] = tk.NORMAL

    def showinfo(self, result, inScrolledText):
        realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
        textvar = realtime + result + '\n'
        inScrolledText.configure(state="normal")
        inScrolledText.insert("end", textvar)
        inScrolledText.see("end")
        inScrolledText.configure(state="disabled")

    def saveacc(self):
        if self.content_savestate:
            tk.messagebox.showinfo("帳號儲存", "此帳號已儲存過")
        else:
            acc = self.lb_view['text']
            self.showinfo("此帳號有下單過 : "+acc, self.log_widget)
            self.logger.info("此帳號有下單過 : " + acc)
            self.content_savestate = True

    def openweb(self):
        os.startfile("Foodpanda.lnk")

        # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
        # options = Options()
        # options.add_argument("--disable-notifications")
        # options.add_argument('--user-agent=%s' % user_agent)
        # driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
        # driver.get('https://www.foodpanda.com.tw/login/new?step=email')


    def Screenshot(self):
        self.root.iconify()
        ScreenShot.ScreenShot()

    def openLog(self):
        os.startfile('Foodpanda帳號儲存.log')


if __name__ == '__main__':
    app = Foodpanda()


# import win32process
# import win32event
# handle = win32process.CreateProcess('run.bat', '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())
# win32event.WaitForSingleObject(handle[0], -1)