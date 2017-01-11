import os
from threading import Thread
from tkinter import *
from tkinter.ttk import *

from pydub import AudioSegment
from pydub.playback import play


class Core(Tk):
    def get_w(self):
        return self._w


class Application(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.path = os.path.dirname(__file__)
        self.master.title("An's focus booster v2.0")
        self.master.minsize(300, 80)
        self.master.maxsize(600, 80)

        try:
            img = PhotoImage(file=os.path.join(self.path, 'icon.png'))
            self.master.tk.call('wm', 'iconphoto', self.master.get_w(), img)
        except TclError:
            img = PhotoImage(file=os.path.join(self.path, 'icon.gif'))
            self.master.tk.call('wm', 'iconphoto', self.master.get_w(), img)

        self.sec = self.itv = self.ses_num = self.break_num = self.ps_sec = self.se_sec = self.brk_sec = 0
        self.minu = self.ps_min = self.ses_min = 25
        self.is_ses = True
        self.brk_min = 5
        self.bell = AudioSegment.from_mp3(os.path.join(self.path, 'bell.mp3'))
        self.time = self.master.after(0)

        self.style = Style()
        self.tbs = StringVar()
        self.stime = StringVar()
        self.t_ses_min = StringVar()
        self.t_se_sec = StringVar()
        self.t_brk_min = StringVar()
        self.t_brk_sec = StringVar()
        self.ses = StringVar()
        self.win_op = Toplevel(self.master)
        self.pb_time = Progressbar(self, orient=HORIZONTAL, mode='determinate', maximum=2520)

        self.widgets()

    def widgets(self):
        themes = self.style.theme_names()
        if 'xpnative' in themes:
            self.style.theme_use('xpnative')
        elif 'aqua' in themes:
            self.style.theme_use('aqua')
        elif 'alt' in themes:
            self.style.theme_use('alt')
        else:
            self.style.theme_use('default')
        self.style.configure('Horizontal.TProgressbar', background='#00f')

        self.stime.set('25:00')
        lb_time = Label(self, textvariable=self.stime)
        lb_time.grid(column=0, row=0, sticky='s')

        self.ses.set('Session {:02d}'.format(self.ses_num))
        lb_ses = Label(self, textvariable=self.ses)
        lb_ses.grid(column=0, row=1, sticky='w')

        self.pb_time.grid(column=1, row=0, rowspan=2, padx=5, sticky='wnes')

        self.tbs.set('Start')
        btn_s = Button(self, textvariable=self.tbs, command=self.btn_start)
        btn_s.grid(column=2, row=0, pady=2, sticky='ne')

        btn_i = Button(self, text='Option', command=self.open_pref)
        btn_i.grid(column=2, row=1, pady=2, sticky='se')

        self.master.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.win_op.title('Preferences')
        self.win_op.resizable(False, False)
        self.win_op.protocol('WM_DELETE_WINDOW', self.ok_pref)

        lf_ses = Labelframe(self.win_op, text='Session Time:', padding=10)
        lf_ses.grid(column=0, row=0, columnspan=2)

        self.t_ses_min.set(25)
        sb_ses_min = Spinbox(lf_ses, from_=0, to=999, textvariable=self.t_ses_min, increment=1, state='readonly')
        sb_ses_min.grid(column=0, row=0, padx=5, pady=5)

        sb_se_sec = Spinbox(lf_ses, from_=0, to=59, textvariable=self.t_se_sec, increment=1, state='readonly')
        sb_se_sec.grid(column=0, row=1, padx=5, pady=5)

        lb_ses_min = Label(lf_ses, text='Minutes')
        lb_ses_min.grid(column=1, row=0, sticky='w')

        lb_se_sec = Label(lf_ses, text='Seconds')
        lb_se_sec.grid(column=1, row=1, sticky='w')

        lf_brk = Labelframe(self.win_op, text='Break Time:', padding=10)
        lf_brk.grid(column=0, row=1, columnspan=2)

        self.t_brk_min.set(5)
        sb_brk_min = Spinbox(lf_brk, from_=0, to=60, textvariable=self.t_brk_min, increment=1, state='readonly')
        sb_brk_min.grid(column=0, row=0, padx=5, pady=5)

        sb_brk_sec = Spinbox(lf_brk, from_=0, to=59, textvariable=self.t_brk_sec, increment=1, state='readonly')
        sb_brk_sec.grid(column=0, row=1, padx=5, pady=5)

        lb_brk_min = Label(lf_brk, text='Minutes')
        lb_brk_min.grid(column=1, row=0, sticky='w')

        lb_brk_sec = Label(lf_brk, text='Seconds')
        lb_brk_sec.grid(column=1, row=1, sticky='w')

        self.win_op.state('withdraw')

    def btn_start(self):
        if self.tbs.get() == 'Start':
            self.start()
        else:
            self.stop()

    def open_pref(self):
        self.win_op.state('normal')

    def ok_pref(self):
        self.ses_min = int(self.t_ses_min.get())
        self.se_sec = int(self.t_se_sec.get())
        self.brk_min = int(self.t_brk_min.get())
        self.brk_sec = int(self.t_brk_sec.get())
        self.win_op.state('withdrawn')

        if self.tbs.get() == 'Start':
            self.stime.set('{:02d}:{:02d}'.format(self.ses_min, self.se_sec))

    def start(self):
        self.minu = self.ses_min
        self.sec = self.se_sec
        if self.minu == 0 and self.sec == 0:
            return

        self.itv = self.pb_time['maximum'] / (self.minu * 60 + self.sec)
        self.style.configure('Horizontal.TProgressbar', background='#00f')
        self.tbs.set('Stop')
        self.ses_num += 1
        self.ses.set('Session {:02d}'.format(self.ses_num))
        self.time = self.master.after(1000, self.update)

    def stop(self):
        self.pb_time['value'] = 0
        self.master.after_cancel(self.time)
        self.tbs.set('Start')

    def update(self):
        self.sec -= 1
        if self.sec < 0:
            self.sec = 59
            self.minu -= 1

        self.stime.set('{:02d}:{:02d}'.format(self.minu, self.sec))
        if self.is_ses:
            if self.sec == 0 and self.minu == 0:
                self.minu = self.brk_min
                self.sec = self.brk_sec

                if self.minu == 0 and self.sec == 0:
                    self.stop()
                    return

                self.break_num += 1
                if self.break_num % 4 == 0:
                    t = (self.minu * 60 + self.sec) * 3
                    self.minu = t // 60
                    self.sec = t % 60

                self.itv = self.pb_time['maximum'] / (self.minu * 60 + self.sec)
                self.ses.set('Break {:02d}'.format(self.break_num))
                self.pb_time['value'] = self.pb_time['maximum']
                self.is_ses = False
                self.style.configure('Horizontal.TProgressbar', background='#f0f')
            else:
                self.pb_time['value'] += self.itv
                if self.minu == 0 and self.sec <= 10:
                    thread = Thread(target=play, args=(self.bell,))
                    thread.start()

                if self.style.theme_use() == 'alt':
                    if self.pb_time['value'] / self.pb_time['maximum'] < 0.2:
                        pass
                    elif self.pb_time['value'] / self.pb_time['maximum'] < 0.4:
                        self.style.configure('Horizontal.TProgressbar', background='#0ff')
                    elif self.pb_time['value'] / self.pb_time['maximum'] < 0.6:
                        self.style.configure('Horizontal.TProgressbar', background='#0f0')
                    elif self.pb_time['value'] / self.pb_time['maximum'] < 0.8:
                        self.style.configure('Horizontal.TProgressbar', background='#ff0')
                    else:
                        self.style.configure('Horizontal.TProgressbar', background='#f00')
        else:
            if self.sec == 0 and self.minu == 0:
                self.stop()
                self.is_ses = True
                return
            else:
                self.pb_time['value'] -= self.itv
        self.time = self.master.after(1000, self.update)

if __name__ == '__main__':
    root = Core()
    app = Application(root, padding=10)
    app.grid(column=0, row=0, sticky='wnes')
    app.mainloop()
