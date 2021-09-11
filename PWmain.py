import tkinter as tk, os, pystray, time, threading, random
import pystray._win32, queue

from PWcipher import KeyCodeGet, TextEncrypt, TextDecrypt
from PWfiles import *

from tkinter import *
from tkinter.ttk import Combobox
from pystray import MenuItem as item
from PIL import Image



### ЛОГИ ###

def Log(logtext):
    logtime = time.strftime("[%X]")
    print(f'\n{time.strftime("[%X]")} PW: {logtext}')



### ###

os.chdir(os.path.dirname(os.path.abspath(__file__)))

version = '2.3'
Log(f'Пароли (v.{version}): Запуск\n')

window = tk.Tk()
window.title(f'Пароли [v.{version}]')
window.geometry('425x130')
window.iconbitmap('content\image.ico')
window.resizable(False, False)

isTryToHack = False

pathAppdataData = os.getenv("APPDATA") + '\Passwords 2' + '\data'
pathAppdataContent = os.getenv("APPDATA") + '\Passwords 2' + '\content'
pathAppdata = os.getenv("APPDATA") + '\Passwords 2'

settingsDefaults = '{"tray": "False", "loginWindow": "False", "hideData": "False", "colorBack": "WhiteSmoke", "colorFont": "Black", "themeFont": "Consolas"}'

symbols = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_____123456789012345678901234567890'

iconCopy = PhotoImage(file='content\Copy.png')
iconDelete = PhotoImage(file='content\Delete.png')
iconSettings = PhotoImage(file='content\Settings.png')
iconAddAccount = PhotoImage(file='content\Add-account.png')
iconBack = PhotoImage(file='content\Back.png')
iconGeneratePassword = PhotoImage(file='content\Generate-password.png')
iconSave= PhotoImage(file='content\Save.png')
iconSave1= PhotoImage(file='content\Save_1.png')
iconSave2= PhotoImage(file='content\Save_2.png')




### СОЗДАНИЕ ФАЙЛОВ ###

if os.path.exists(pathAppdata) and os.path.exists(pathAppdata + '\settings.txt') and os.path.exists(pathAppdata + '\passwords.txt') and os.path.exists(pathAppdata + '/themes.txt'):
    KeyCodeGet()

    Log('Файлы в AppData уже существуют\n')

elif os.path.exists(pathAppdata):
    KeyCodeGet()
    print()

    if not os.path.exists(pathAppdata + '\settings.txt'): 
        FileWrite('settings', TextEncrypt(settingsDefaults), create=True)
        isTryToHack = True
        Log('Создан файл "settings"')
    if not os.path.exists(pathAppdata + '\passwords.txt'): [FileWrite('passwords', TextEncrypt('{"loginPassword": ""}'), create=True), Log('Создан файл "passwords"')]
    if not os.path.exists(pathAppdata + '/themes.txt'): [FileCreate('themes'), Log('Создан файл "themes"')]

    Log('Созданы файлы в AppData\n')

else:
    os.mkdir(pathAppdata)

    KeyCodeGet()
    print()

    if not os.path.exists(pathAppdata + '\settings.txt'): [FileWrite('settings', TextEncrypt(settingsDefaults), create=True), Log('Создан файл "settings"')]
    if not os.path.exists(pathAppdata + '\passwords.txt'): [FileWrite('passwords', TextEncrypt('{"loginPassword": ""}'), create=True), Log('Создан файл "passwords"')]
    if not os.path.exists(pathAppdata + '/themes.txt'): [FileCreate('themes'), Log('Создан файл "themes"')]

    Log('Созданы файлы в AppData\n')




### ЗАГРУЗКА ДАННЫХ ###

def DataLoad():
    global settingsJSON, passwordsJSON, passwordsJSONKeys
    ReadData()

    from PWfiles import settingsJSON, passwordsJSON

    passwordsJSONKeys = []
    for key in passwordsJSON:
        if key != 'loginPassword': passwordsJSONKeys.append(f'"{key}"')
    passwordsJSONKeys = ' '.join(passwordsJSONKeys)

    if isTryToHack == True and passwordsJSON['loginPassword'] != '':
        settingsJSON['loginWindow'] = 'True'
        FileWrite('settings', TextEncrypt(str(settingsJSON).replace("'", '"')))



### ПРИМЕНЕНИЕ НАСТРОЕК ###

def SettingsApply():

    if settingsJSON['tray'] == 'True': window.protocol('WM_DELETE_WINDOW', withdraw_window)
    else: window.protocol('WM_DELETE_WINDOW', window.destroy)

    ThemeApply()

def ThemeApply():
    global colorBack, colorFont, themeFont
    colorBack = settingsJSON['colorBack']
    window.configure(background=colorBack)
    colorFont = settingsJSON['colorFont']
    themeFont = settingsJSON['themeFont']



### СКРЫТИЕ ПРИЛОЖЕНИЯ В ТРЕЙ ###

def quit_window(icon, item):
    Log('quit_window')
    icon.stop()
    window.destroy()

def show_window(icon, item):
    Log('show_window')
    icon.stop()
    window.after(0,window.deiconify)

def withdraw_window():
    e1.delete(0, 'end')
    Log('withdraw_window')
    if settingsJSON['loginWindow'] == 'True':
        Log('Содержимое приложения скрыто')
        PW_ClearWindow()
        PW_LoginWindow()
    else:
        PW_MainWindow()
    window.withdraw()
    image = Image.open("content\image.ico")
    menu = pystray.Menu(item('Открыть', show_window, default=True), item('Выйти', quit_window))
    icon = pystray.Icon("main", image, "PW2", menu)
    icon.run()



### ФУНКЦИОНАЛ ###

def PW_ClearWindow():

    for widget in window.winfo_children():
        try: widget.grid_forget()
        except: widget.pack_forget()

def CbSelect(selected):
    try: 
        Log(f'>passwordsJSON[{selected}]: {passwordsJSON[selected]}')

        ReadData('passwordsList', selected)
        from PWfiles import passwordsList

        p1.configure(state='normal')
        p1.delete('1.0', END)
        p2.configure(state='normal')
        p2.delete('1.0', END)
        p3.configure(state='normal')
        p3.delete('1.0', END)
        
        print(settingsJSON['hideData'])

        p1.insert(END, selected)
        p1.configure(state='disabled')

        if settingsJSON['hideData'] == 'False': p2.insert(END, passwordsList[0])
        if settingsJSON['hideData'] == 'True': 
            ins = passwordsList[0]
            ins = ins.replace(ins, '*'*len(ins))
            p2.insert(END, ins)
        p2.configure(state='disabled')

        if settingsJSON['hideData'] == 'False': p3.insert(END, passwordsList[1])
        if settingsJSON['hideData'] == 'True':
            ins = passwordsList[1]
            ins = ins.replace(ins, '*'*len(ins))
            p3.insert(END, ins)
        p3.configure(state='disabled')
    except: print('>Button: '+selected)

def ClipboardAppend(text):
    window.clipboard_clear()
    window.clipboard_append(text.replace('\n', ''))

def PasswordGenerator():
    passwordGenerated = ''
    for i in range(random.randint(10, 16)):
        passwordGenerated = passwordGenerated + symbols[random.randint(0, 86)]
        if random.randint(0, 20000) == 0:
            passwordGenerated = passwordGenerated + 'Aboba'
    return passwordGenerated




def PW_LoginWindow():
    t1.config(text='Введите пароль для входа', bg=colorBack, fg=colorFont, font=(themeFont,14))
    t1.grid(row=0, column=0, sticky=W+E, ipadx=100, pady=20)

    e1.focus()
    e1.config(width=26, bg=colorBack, fg=colorFont, font=themeFont, relief=GROOVE, borderwidth=2, show='*')
    e1.grid(row=1, column=0, sticky=W, padx=55)
    
    b1.config(text='Войти', width=65, height=19, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:threading.Thread(target=PW_LWcheck, args=[e1.get()]).start(), relief=GROOVE, borderwidth=2, image=iconSave)
    b1.grid(row=1, column=0, sticky=E, padx=70)

    window.bind('<Return>', lambda b:threading.Thread(target=PW_LWcheck, args=[e1.get()]).start())

def PW_LWcheck(password):
    if password == passwordsJSON['loginPassword']:
        Log('Пароль введён')
        PW_MainWindow()
        window.unbind('<Return>')
        e1.config(show='')
        e1.delete(0, 'end')
    else:
        Log('PW: Неверный пароль')
        e1.config(show='')
        e1.delete(0, 'end')
        e1.insert(0, 'Неверный пароль')
        e1.config(state='readonly')
        time.sleep(1)
        e1.config(state='normal')
        e1.delete(0, 'end')
        e1.config(show='*')




def PW_MainWindow():
    PW_ClearWindow()

    t4.config(text='Выберите аккаунт:', bg=colorBack, fg=colorFont, font=(themeFont,13))
    t4.grid(row=0, rowspan=2, column=0, sticky=NS+W, padx=13)
    

    cb1.config(background=colorBack, foreground='Black', state='readonly', font=(themeFont,10))
    cb1['value'] = (passwordsJSONKeys)
    cb1.grid(row=2, rowspan=2, column=0, sticky=W+E, padx=15, ipady=2)
    cb1.bind("<<ComboboxSelected>>", lambda e: [window.focus(), CbSelect(cb1.get())])
    cb1.set('')

    b1.config(text='', width=13, height=20, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:PW_SettingsWindow(), relief=GROOVE, borderwidth=2, image=iconSettings)
    b1.grid(row=4, rowspan=2, column=0, sticky=W+S, padx=15, ipadx=15)
    b2.config(text='', width=13, height=20, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:AccountDelete(cb1.get()), relief=GROOVE, borderwidth=2, image=iconDelete)
    b2.grid(row=4, rowspan=2, column=0, padx=5, sticky=S, ipadx=15)
    b3.config(text='', width=13, height=20, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:PW_AddAccountWindow(), relief=GROOVE, borderwidth=2, image=iconAddAccount)
    b3.grid(row=4, rowspan=2, column=0, sticky=E+S, padx=15, ipadx=15)

    t1.config(text='Аккаунт', bg=colorBack, fg=colorFont, font=(themeFont,8))
    t1.grid(row=0, column=1, sticky=W+S)
    t2.config(text='Логин', bg=colorBack, fg=colorFont, font=(themeFont,8))
    t2.grid(row=2, column=1, sticky=W+S)
    t3.config(text='Пароль', bg=colorBack, fg=colorFont, font=(themeFont,8))
    t3.grid(row=4, column=1,  sticky=W+S)

    p1.config(bg=colorBack, fg=colorFont, font=(themeFont,10), height=1, width=29, state='normal', relief=GROOVE, borderwidth=1)
    p1.delete('1.0', END)
    p1.config(state='disabled')
    p1.grid(row=1, column=1, sticky=W)
    p2.config(bg=colorBack, fg=colorFont, font=(themeFont,10), height=1, width=29, state='normal', relief=GROOVE, borderwidth=1)
    p2.delete('1.0', END)
    p2.config(state='disabled')
    p2.grid(row=3, column=1, sticky=W)
    p3.config(bg=colorBack, fg=colorFont, font=(themeFont,10), height=1, width=29, state='normal', relief=GROOVE, borderwidth=1)
    p3.delete('1.0', END)
    p3.config(state='disabled')
    p3.grid(row=5, column=1, sticky=W)

    b4.config(text='', width=11, height=0, font=(themeFont,7), bg=colorBack, fg=colorFont, command=lambda:ClipboardAppend(p1.get("1.0",END)), relief=FLAT, borderwidth=0, image=iconCopy)
    b4.grid(row=1, column=2, padx=4, sticky=W+E)
    b5.config(text='', width=11, height=0, font=(themeFont,7), bg=colorBack, fg=colorFont, command=lambda:ClipboardAppend(p2.get("1.0",END)), relief=FLAT, borderwidth=0, image=iconCopy)
    b5.grid(row=3, column=2, padx=4, sticky=W+E)
    b6.config(text='', width=11, height=0, font=(themeFont,7), bg=colorBack, fg=colorFont, command=lambda:ClipboardAppend(p3.get("1.0",END)), relief=FLAT, borderwidth=0, image=iconCopy)
    b6.grid(row=5, column=2, padx=4, sticky=W+E)



def PW_AddAccountWindow():
    PW_ClearWindow()

    t1.config(text='Аккаунт', bg=colorBack, fg=colorFont, font=(themeFont,8))
    t1.grid(row=0, column=0, padx=15, sticky=W+S)
    t2.config(text='Логин', bg=colorBack, fg=colorFont, font=(themeFont,8))
    t2.grid(row=2, column=0, padx=15, sticky=W+S)
    t3.config(text='Пароль', bg=colorBack, fg=colorFont, font=(themeFont,8))
    t3.grid(row=4, column=0,  padx=15, sticky=W+S)

    e1.config(bg=colorBack, fg=colorFont, font=(themeFont,10), width=29, relief=GROOVE, borderwidth=1)
    e1.grid(row=1, column=0, padx=15, sticky=W)
    e2.config(bg=colorBack, fg=colorFont, font=(themeFont,10), width=29, relief=GROOVE, borderwidth=1)
    e2.grid(row=3, column=0, padx=15, sticky=W)
    e3.config(bg=colorBack, fg=colorFont, font=(themeFont,10), width=29, relief=GROOVE, borderwidth=1)
    e3.grid(row=5, column=0, padx=15, sticky=W)

    e1.focus()

    b1.config(text='', width=75, height=25, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:[e1.delete(0, 'end'), e2.delete(0, 'end'), e3.delete(0, 'end'), PW_MainWindow()], relief=GROOVE, borderwidth=2, image=iconBack)
    b1.grid(row=4, rowspan=2, column=2, sticky=W+S)
    b2.config(text='', width=75, height=25, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:[e3.delete(0, 'end'), e3.insert(0, PasswordGenerator())], relief=GROOVE, borderwidth=2, image=iconGeneratePassword)
    b2.grid(row=4, rowspan=2, column=1, padx=5, sticky=W+S)
    b7.config(text='', width=165, height=50, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:threading.Thread(target=AccountSave, args=[e1.get(), e2.get(), e3.get()]).start(), relief=GROOVE, borderwidth=2, image=iconSave1)
    b7.grid(row=0, rowspan=5, column=1, columnspan=2, padx=5, pady=17, sticky=W+S+N)

def AccountSave(accountName, accountLogin, accountPassword):

    if accountName != '' and accountLogin != '' and accountPassword != '' and accountName != 'Не указаны данные' and accountLogin != 'Не указаны данные' and accountPassword != 'Не указаны данные':

        if accountName in passwordsJSON:
            Log('Дублирование имени')
            e1.delete(0, 'end')
            e1.insert(0, 'Такой аккаунт уже сохранён')
            e1.config(state='readonly')
            time.sleep(1)
            e1.config(state='normal')
            e1.delete(0, 'end')

        else:
            accountData = {f'{accountName}': f'{accountLogin}, {accountPassword}'}
            passwordsJSON.update(accountData)
            FileWrite('passwords', TextEncrypt(str(passwordsJSON).replace("'", '"')))
            
            e1.delete(0, 'end')
            e2.delete(0, 'end')
            e3.delete(0, 'end')

            b7.config(image=iconSave2)
            e1.focus()
            DataLoad()
            time.sleep(1)
            b7.config(image=iconSave1)

            Log(f'Аккаунт "{accountName}" сохранён\n')

    else:
        Log('Не указаны данные')
        threading.Thread(target=AS1, args=[accountName]).start()
        threading.Thread(target=AS2, args=[accountLogin]).start()
        threading.Thread(target=AS3, args=[accountPassword]).start()

def AS1(accountName):
    if accountName == '':
        e1.delete(0, 'end')
        e1.insert(0, 'Не указаны данные')
        e1.config(state='readonly')
        time.sleep(1)
        e1.config(state='normal')
        e1.delete(0, 'end')
def AS2(accountLogin):
    if accountLogin == '':
        e2.delete(0, 'end')
        e2.insert(0, 'Не указаны данные')
        e2.config(state='readonly')
        time.sleep(1)
        e2.config(state='normal')
        e2.delete(0, 'end')
def AS3(accountPassword):
    if accountPassword == '': 
        e3.delete(0, 'end')
        e3.insert(0, 'Не указаны данные')
        e3.config(state='readonly')
        time.sleep(1)
        e3.config(state='normal')
        e3.delete(0, 'end')     

def AccountDelete(accountName):
    if accountName != '':
        try:
            passwordsJSON.pop(accountName)
            FileWrite('passwords', TextEncrypt(str(passwordsJSON).replace("'", '"')))
            DataLoad()
            cb1['value'] = (passwordsJSONKeys)
            PW_MainWindow()
        except:
            pass



def PW_SettingsWindow():
    PW_ClearWindow()

    stngTray = StringVar()
    stngTray.set(settingsJSON['tray'])
    stngLW = StringVar()
    stngLW.set(settingsJSON['loginWindow'])
    try:
        stngHD = StringVar()
        stngHD.set(settingsJSON['hideData'])
    except:
        stngHD.set('False')

    chb1.config(text='Сворачивание в трей', bg=colorBack, fg=colorFont, font=(themeFont,9), variable=stngTray, onvalue='True', offvalue='False', command=lambda:SW1('tray', stngTray))
    chb1.grid(row=0, column=0, columnspan=2, sticky=W, padx=13)
    chb2.config(text='Окно входа', bg=colorBack, fg=colorFont, font=(themeFont,9), variable=stngLW, onvalue='True', offvalue='False', command=lambda:[SW2(stngLW), SW1('loginWindow', stngLW)])
    chb2.grid(row=1, column=0, columnspan=2, sticky=W, padx=13)
    chb3.config(text='Скрывать вывод данных', bg=colorBack, fg=colorFont, font=(themeFont,9), variable=stngHD, onvalue='True', offvalue='False', command=lambda:SW1('hideData', stngHD))
    chb3.grid(row=0, column=2, sticky=W, padx=13)

    e1.config(width=19, bg=colorBack, fg=colorFont, font=(themeFont,10), relief=GROOVE, borderwidth=2)
    e1.grid(row=3, column=0, sticky=W, padx=15)
    e1.delete(0, 'end')
    window.focus()

    b1.config(text='', width=43, height=20, font=(themeFont,10), bg=colorBack, fg=colorFont, command=lambda:[FileWrite('settings', TextEncrypt(str(settingsJSON).replace("'", '"'))), FileWrite('passwords', TextEncrypt(str(passwordsJSON).replace("'", '"'))), DataLoad(), SettingsApply(), e1.unbind('<FocusIn>'), window.unbind('<Return>'), e1.delete(0, 'end'), PW_MainWindow()], relief=GROOVE, borderwidth=2, image=iconBack)
    b1.grid(row=4, column=0, sticky=W+S, pady=5, padx=15)
    b2.config(text='', width=20, height=17, font=(themeFont,8), bg=colorBack, fg=colorFont, command=lambda:threading.Thread(target=SW3, args=[e1.get()]).start(), relief=GROOVE, borderwidth=0, image=iconSave)
    b2.grid(row=3, column=0, sticky=E)

    t1.config(text='Изменить пароль для входа:', bg=colorBack, fg=colorFont, font=(themeFont,7))
    t1.grid(row=2, column=0, padx=13, sticky=W+S)

    e1.bind('<FocusIn>', SW4())
    
def SW1(stng, var):
    settingsJSON[stng] = str(var.get())
def SW2(var='False'):
    if passwordsJSON['loginPassword'] == '' and var.get() == 'True': b1.config(state='disabled')
    else: b1.config(state='normal')
def SW3(arg):
    if arg == '':
        e1.delete(0, 'end')
        e1.insert(0, 'Не указаны данные')
        e1.config(state='readonly')
        time.sleep(0.5)
        e1.config(state='normal')
        e1.delete(0, 'end')
    else:
        passwordsJSON['loginPassword'] = arg
        SW2()
        e1.delete(0, 'end')
        e1.insert(0, 'Сохранено!')
        e1.config(state='readonly')
        time.sleep(1)
        e1.config(state='normal')
        e1.delete(0, 'end')
        window.unbind('<Return>')
def SW4():
    window.bind('<Return>', lambda enter:threading.Thread(target=SW3, args=[e1.get()]).start())



### ###



t1 = Label(window)
t2 = Label(window)
t3 = Label(window)
t4 = Label(window)

b1 = Button(window)
b2 = Button(window)
b3 = Button(window)
b4 = Button(window)
b5 = Button(window)
b6 = Button(window)
b7 = Button(window)

e1 = Entry(window)

cb1 = Combobox(window)

p1 = Text(window)
p2 = Text(window)
p3 = Text(window)

e1 = Entry(window)
e2 = Entry(window)
e3 = Entry(window)

chb1 = Checkbutton(window)
chb2 = Checkbutton(window)
chb3 = Checkbutton(window)



DataLoad()
SettingsApply()
if settingsJSON['loginWindow'] == 'True': PW_LoginWindow()
if settingsJSON['loginWindow'] == 'False': PW_MainWindow()
window.mainloop()