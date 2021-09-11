import os, traceback, json, time

pathAppdataData = os.getenv("APPDATA") + '\Passwords 2' + '\data'
pathAppdata = os.getenv("APPDATA") + '\Passwords 2'

def Log(logtext):
    logtime = time.strftime("[%X]")
    print(f'{time.strftime("[%X]")} PW: {logtext}')

def Start():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try: #Чтение файлов
        file = open('test.txt', 'r+', encoding='utf-8')

        Log('Чтение файлов')

    except: #Создание файлов при первом запуске
        file = open('test.txt', 'w', encoding='utf-8')

        Log('Создание файлов')

    try:
        print(file.readlines())
    except:
        pass
#Start()

def FileRead(fileName, path = pathAppdata, create = False):
    try:
        Log(f'Чтение файла "{fileName}"')
        file = open(f'{path}\\{fileName}.txt', 'r', encoding='utf-8')
        Log(f'Файл "{fileName}" прочитан\n')
        return file
    except:
        if create == True:
            FileCreate(fileName, path)
            file = open(f'{path}\\{fileName}.txt', 'r', encoding='utf-8')
            Log(f'Файл "{fileName}" прочитан\n')
            return file
        else:
            Log(f'Файла "{fileName}" не существует\n')        
            return False

def FileWrite(fileName, toWrite, path = pathAppdata, create = False):
    try:
        Log(f'Попытка записи в файл "{fileName}"')
        file = open(f'{path}\\{fileName}.txt', 'r+', encoding='utf-8')
        file.seek(0)
        file.truncate(0)
        file.write(f'{toWrite}\n')
        Log(f'Запись в файл "{fileName}" выполнена\n')
    except:
        if create == True:
            FileCreate(fileName, path)
            file = open(f'{path}\\{fileName}.txt', 'r+', encoding='utf-8')
            file.seek(0)
            file.truncate(0)
            file.write(f'{toWrite}\n')
            Log(f'Запись в файл "{fileName}" выполнена\n')
        else:
            Log(f'Файла "{fileName}" не существует\n')        
            return False

def FileCreate(fileName, path = pathAppdata):
    if os.path.exists(f'{pathAppdata}/{fileName}.txt'):
        Log(f'Файл "{fileName}" уже существует\n')
        return False
    else:
        Log(f'Создание файла "{fileName}"')
        file = open(f'{path}\\{fileName}.txt', 'w', encoding='utf-8')
        Log(f'Файл "{fileName}" создан')
        return True

def ReadData(arg='all', a = None):
    global settingsData, settingsJSON, passwordsData, passwordsJSON, passwordsList, themesData
    if arg == 'all':
        from PWcipher import TextDecrypt

        settingsData = FileRead('settings').read()
        settingsJSON = TextDecrypt(settingsData).rstrip('\n').replace("'", '"')
        settingsJSON = json.loads(settingsJSON)

        passwordsData = FileRead('passwords').read()
        passwordsJSON = TextDecrypt(passwordsData).rstrip('\n').replace("'", '"')
        passwordsJSON = json.loads(passwordsJSON)

        themesData = FileRead('themes').read()
    else:
        if arg == 'passwordsList':
            passwordsList = passwordsJSON[a].split(', ')
            return passwordsList