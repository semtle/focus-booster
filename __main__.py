import os
from threading import Thread
from tkinter import *
from tkinter.ttk import *

from pydub import AudioSegment
from pydub.playback import play

path = os.path.dirname(__file__)


def update():
    global time, sec, minu, itv, isSes, breakNum, brkSec, brkMin, bell

    sec -= 1
    if sec < 0:
        sec = 59
        minu -= 1

    stime.set('{:02d}:{:02d}'.format(minu, sec))

    if isSes:
        if sec == 0 and minu == 0:
            minu = brkMin
            sec = brkSec

            if minu == 0 and sec == 0:
                stop()
                return

            breakNum += 1
            if breakNum % 4 == 0:
                t = (minu * 60 + sec) * 3
                minu = t // 60
                sec = t % 60

            itv = pbTime['maximum'] / (minu * 60 + sec)
            ses.set('Break {:02d}'.format(breakNum))
            pbTime['value'] = pbTime['maximum']
            isSes = False
            style.configure('Horizontal.TProgressbar', background='#f0f')
        else:
            pbTime['value'] += itv

            if minu == 0 and sec <= 10:
                thread = Thread(target=play, args=(bell,))
                thread.start()

            if style.theme_use() == 'alt':
                if pbTime['value'] / pbTime['maximum'] < 0.2:
                    pass
                elif pbTime['value'] / pbTime['maximum'] < 0.4:
                    style.configure('Horizontal.TProgressbar', background='#0ff')
                elif pbTime['value'] / pbTime['maximum'] < 0.6:
                    style.configure('Horizontal.TProgressbar', background='#0f0')
                elif pbTime['value'] / pbTime['maximum'] < 0.8:
                    style.configure('Horizontal.TProgressbar', background='#ff0')
                else:
                    style.configure('Horizontal.TProgressbar', background='#f00')
    else:
        if sec == 0 and minu == 0:
            stop()
            isSes = True
            return
        else:
            pbTime['value'] -= itv

    time = root.after(1000, update)


def start():
    global sesNum, time, sec, minu, itv, sesMin, seSec

    minu = sesMin
    sec = seSec
    if minu == 0 and sec == 0:
        return

    itv = pbTime['maximum'] / (minu * 60 + sec)
    style.configure('Horizontal.TProgressbar', background='#00f')
    tbs.set('Stop')
    sesNum += 1
    ses.set('Session {:02d}'.format(sesNum))
    time = root.after(1000, update)


def stop():
    global time

    pbTime['value'] = 0
    root.after_cancel(time)
    tbs.set('Start')


def btn_s():
    if tbs.get() == 'Start':
        start()
    else:
        stop()


def open_pref():
    winOp.state('normal')


def ok_pref():
    global brkSec, brkMin, sesMin, seSec

    sesMin = int(tSesMin.get())
    seSec = int(tSeSec.get())
    brkMin = int(tBrkMin.get())
    brkSec = int(tBrkSec.get())
    winOp.state('withdrawn')

    if tbs.get() == 'Start':
        stime.set('{:02d}:{:02d}'.format(sesMin, seSec))


if __name__ == '__main__':
    sec = 0
    minu = 25
    itv = 0
    sesNum = 0
    breakNum = 0
    psMin = 25
    psSec = 0
    isSes = True
    sesMin = 25
    seSec = 0
    brkMin = 5
    brkSec = 0
    bell = AudioSegment.from_mp3(os.path.join(path, 'bell.mp3'))

    root = Tk()
    root.title("An's focus booster v1.0")
    root.minsize(300, 80)
    root.maxsize(600, 80)
    img = PhotoImage(file=os.path.join(path, 'icon.gif'))
    root.tk.call('wm', 'iconphoto', root._w, img)

    style = Style()
    themes = style.theme_names()

    if 'xpnative' in themes:
        style.theme_use('xpnative')
    elif 'aqua' in themes:
        style.theme_use('aqua')
    elif 'alt' in themes:
        style.theme_use('alt')
    else:
        style.theme_use('default')

    style.configure('Horizontal.TProgressbar', background='#00f')
    time = root.after(0)

    mf = Frame(root, padding=10)
    mf.grid(column=0, row=0, sticky='wnes')

    stime = StringVar()
    stime.set('25:00')
    lbTime = Label(mf, textvariable=stime)
    lbTime.grid(column=0, row=0, sticky='s')

    ses = StringVar()
    ses.set('Session {:02d}'.format(sesNum))
    lbSes = Label(mf, textvariable=ses)
    lbSes.grid(column=0, row=1, sticky='w')

    pbTime = Progressbar(mf, orient=HORIZONTAL, mode='determinate', maximum=2520)
    pbTime.grid(column=1, row=0, rowspan=2, padx=5, sticky='wnes')

    tbs = StringVar()
    tbs.set('Start')
    btnS = Button(mf, textvariable=tbs, command=btn_s)
    btnS.grid(column=2, row=0, pady=2, sticky='ne')

    btnI = Button(mf, text='Option', command=open_pref)
    btnI.grid(column=2, row=1, pady=2, sticky='se')

    root.columnconfigure(0, weight=1)
    mf.columnconfigure(1, weight=1)

    winOp = Toplevel(root)
    winOp.title('Preferences')
    winOp.resizable(False, False)
    winOp.protocol('WM_DELETE_WINDOW', ok_pref)

    lfSes = Labelframe(winOp, text='Session Time:', padding=10)
    lfSes.grid(column=0, row=0, columnspan=2)

    tSesMin = StringVar()
    tSesMin.set(25)
    sbSesMin = Spinbox(lfSes, from_=0, to=999, textvariable=tSesMin, increment=1, state='readonly')
    sbSesMin.grid(column=0, row=0, padx=5, pady=5)

    tSeSec = StringVar()
    sbSeSec = Spinbox(lfSes, from_=0, to=59, textvariable=tSeSec, increment=1, state='readonly')
    sbSeSec.grid(column=0, row=1, padx=5, pady=5)

    lbSesMin = Label(lfSes, text='Minutes')
    lbSesMin.grid(column=1, row=0, sticky='w')

    lbSeSec = Label(lfSes, text='Seconds')
    lbSeSec.grid(column=1, row=1, sticky='w')

    lfBrk = Labelframe(winOp, text='Break Time:', padding=10)
    lfBrk.grid(column=0, row=1, columnspan=2)

    tBrkMin = StringVar()
    tBrkMin.set(5)
    sbBrkMin = Spinbox(lfBrk, from_=0, to=60, textvariable=tBrkMin, increment=1, state='readonly')
    sbBrkMin.grid(column=0, row=0, padx=5, pady=5)

    tBrkSec = StringVar()
    sbBrkSec = Spinbox(lfBrk, from_=0, to=59, textvariable=tBrkSec, increment=1, state='readonly')
    sbBrkSec.grid(column=0, row=1, padx=5, pady=5)

    lbBrkMin = Label(lfBrk, text='Minutes')
    lbBrkMin.grid(column=1, row=0, sticky='w')

    lbBrkSec = Label(lfBrk, text='Seconds')
    lbBrkSec.grid(column=1, row=1, sticky='w')

    winOp.state('withdraw')
    root.mainloop()
