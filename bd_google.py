import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


num_st = 0
num_avto = 0

def create_table():
    print('Подгрузка Базы Данных')
    CREDENTIALS_FILE = 'credentials.json'  # Имя файла с закрытым ключом
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

    spreadsheet = service.spreadsheets().create(body = {
        'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист номер один',
                                   'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
    print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

    driveService = build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId = spreadsheetId,
        body = {'type': 'user', 'role': 'writer', 'emailAddress': 'rafil.galimzyanov.00@bk.ru'},  # Открываем доступ на редактирование
        fields = 'id'
    ).execute()
    return service, spreadsheetId

def send_avto(num_car):
    global num_avto
    service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": f"Лист номер один!F{2+num_avto*12}:M{2+num_avto*12}",
                 "majorDimension": "ROWS",
                 "values": [[f"{num_car}", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]]
                }
            ]
        }).execute()

    service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {f"range": f"Лист номер один!F{3+num_avto*12}:F{13+num_avto*12}",
                 "majorDimension": "ROWS",
                 "values": [["8:00 - 9:00"], ["9:00 - 10:00"], ["10:00 - 11:00"], ["11:00 - 12:00"], ["12:00 - 13:00"],
                            ["13:00 - 14:00"], ["14:00 - 15:00"], ["15:00 - 16:00"], ["16:00 - 17:00"], ["17:00 - 18:00"]]
                }
            ]
        }).execute()
    frame(1+num_avto*12, 12+num_avto*12, 5, 13)
    num_avto += 1

'''
Заполнение БД учениками
'''
def send_student(id_std, name, group):
    global num_st
    service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {f"range": f"Лист номер один!B{2+num_st+1}:D{2+num_st+1}",
             "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
             "values": [
                        [f'{id_std}', f"{name}", f"{group}"]  # Заполняем вторую строку
                       ]}
        ]
    }).execute()
    num_st += 1

# Рисуем рамку
def frame(startRowIndex, endRowIndex, startColumnIndex, endColumnIndex):
    '''
    Шапочка шаблона
    '''
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {f"range": "Лист номер один!B2:D2",
             "majorDimension": "ROWS",
             "values": [["ID ученика", "ФИО", "Группа"]]
             }
        ]
    }).execute()

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body={
            "requests": [
                {'updateBorders': {'range': {
                                             'startRowIndex': startRowIndex,
                                             'endRowIndex': endRowIndex,
                                             'startColumnIndex': startColumnIndex,
                                             'endColumnIndex': endColumnIndex},
                                   'bottom': {
                                       # Задаем стиль для верхней границы
                                       'style': 'SOLID',  # Сплошная линия
                                       'width': 1,  # Шириной 1 пиксель
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},  # Черный цвет
                                   'top': {
                                       # Задаем стиль для нижней границы
                                       'style': 'SOLID',
                                       'width': 1,
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                   'left': {  # Задаем стиль для левой границы
                                       'style': 'SOLID',
                                       'width': 1,
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                   'right': {
                                       # Задаем стиль для правой границы
                                       'style': 'SOLID',
                                       'width': 1,
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                   'innerHorizontal': {
                                       # Задаем стиль для внутренних горизонтальных линий
                                       'style': 'SOLID',
                                       'width': 1,
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                                   'innerVertical': {
                                       # Задаем стиль для внутренних вертикальных линий
                                       'style': 'SOLID',
                                       'width': 1,
                                       'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}

                                   }}
            ]
        }).execute()

    '''
    Ширина колонок

    '''
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        "requests": [

            # Задать ширину столбцов B: 30 пикселей
            {
                "updateDimensionProperties": {
                    "range": {
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": 2
                    },
                    "properties": {
                        "pixelSize": 80
                    },
                    "fields": "pixelSize"
                }
            },

            # Задать ширину столбца C: 250 пикселей
            {
                "updateDimensionProperties": {
                    "range": {
                        "dimension": "COLUMNS",
                        "startIndex": 2,
                        "endIndex": 3
                    },
                    "properties": {
                        "pixelSize": 250
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }).execute()

    # Объединяем ячейки A2:D1
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body={
            "requests": [
                {'mergeCells': {'range': {
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 1,
                    'endColumnIndex': 4},
                    'mergeType': 'MERGE_ALL'}}
            ]
        }).execute()
    # Добавляем заголовок таблицы
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Лист номер один!B1",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": [["Ученики Автошколы"]
                        ]}
        ]
    }).execute()

service, spreadsheetId = create_table()

'''
Чтение данных 

'''
def verify_id(id):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range='F2:M12',
        majorDimension='COLUMNS'
    ).execute()
    message_timetable = []
    dict_bd = {
        ('col', 1): 'Номер авто: ', ('col', 2): 'Понедельник', ('col', 3): 'Вторник', ('col', 4): 'Среда',
        ('col', 5): 'Четверг', ('col', 6): 'Пятница', ('col', 7): 'Суббота', ('col', 8): 'Воскресенье',
        ('row', 2): '8:00 - 9:00', ('row', 3): '9:00 - 10:00', ('row', 4): '10:00 - 11:00', ('row', 5): '11:00 - 12:00',
        ('row', 6): '12:00 - 13:00', ('row', 7): '13:00 - 14:00', ('row', 8): '14:00 - 15:00',
        ('row', 9): '15:00 - 16:00',
        ('row', 10): '16:00 - 17:00', ('row', 11): '17:00 - 18:00',
    }

    def dict_get(i, j):
        col = dict_bd.get(('col', i))
        row = dict_bd.get(('row', j))
        return f'{col}: {row}'

    for i in range(len(values['values'])):
        for j in range(len(values['values'][i])):
            if values['values'][i][j] == f'{id}':
                print(dict_get(i + 1, j + 1))
                message_timetable.append(dict_get(i + 1, j + 1))

    return message_timetable

def verify_name(name):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range='A2:A2',
        majorDimension='COLUMNS'
    ).execute()
    try:
        student_name = values['values'][0][0].split()
        return student_name.count(name) == 1
    except:
        print(f'Нет значений в ячейке А2')
        pass


