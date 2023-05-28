import os
import shutil
from threading import Timer
from pathlib import Path

if not os.path.isdir("save_files"):
    os.mkdir("save_files")

class FileService:

    def __init__(self):
        self.data = {}
        self.counter = 0
        self.dictionary = []
        self.backup = {}
        self.sec = 86400

    def save_file(self, filename):
        if os.path.isfile(filename):
            self.data[self.counter] = filename
            print(f"Идентификатор файла: {self.counter}")
            self.counter += 1
        else:
            print("Путь неверный")

        return self.counter

    def get_file(self, id):
        try:
            return self.data[id]
        except:
            return "Такого файла нет"

    def delete_file(self, id):
        try:
            os.remove(self.data[id])
            # self.data.pop(id)
        except:
            return "Нет файла для удаления"

    def show_all_list(self):
        if len(self.data) == 0:
            print("Список пуст, добавьте файлы!")
        else:
            for key in self.data:
                print(str(key) + ":", self.data[key])

    def change_id(self, old_id, new_id):
        try:
            filename = self.data[old_id]
            self.data.pop(old_id)
            self.data |= {new_id: filename}
            

        except:
            return "ID указан неправильно"

    def list_files_from_ids(self, dict):
        try:
            end_dict = []
            for id in dict:
                end_dict.append(self.data[id])
            return end_dict

        except:
            return "ID указан неправильно"

    def create_backup_auto(self):
        for key in self.data:
            shutil.copy(self.data[key], "save_files")
        self.t = Timer(self.sec, self.create_backup_auto)
        self.t.start()

    def save_backup_in_file(self):
        for key in self.data:
            shutil.copy(self.data[key], "save_files")

    def backup_for_tf(self):
        self.save_backup_in_file()
        return "Успешно"

    def recovery_with_backup(self, id):
        shutil.copy(f"save_files\\{os.path.basename(self.data[int(id)])}", self.data[int(id)])
        print('Восстановление прошло успешно')


file_service = FileService()

while True:

    menu_service = '''
[1] Сохранить файл
[2] Получить файл по ID
[3] Удалить файл по ID
[4] Показать все файлы и их ID
[5] Поменять один ID на другой
[6] Получить несколько файлов по нескольким ID
[7] Записать бэкап
[8] Восстановиться с помощью сохранённого бэкапа
[9] Изменить таймер бэкапа
[0] Завершить программу
    '''

    true_print = True

    if true_print:
        print(menu_service)

    choise = input('Укажите номер опции: ')

    if choise == '0':
        break

    elif choise == '1':
        menu_option_save = '''
[1] Ввести путь к файлу
[0] Вернуться обратно
        '''

        print(menu_option_save)
        choise_save_file = input('Выберите: ')

        if choise_save_file == '0':
            continue

        elif choise_save_file == '1':
            file_service.save_file(input("Введите путь: "))
            file_service.create_backup_auto()

    elif choise == '2':
        print(file_service.get_file(int(input("Введите ID файла: "))))

    elif choise == '3':
        file_service.delete_file(int(input("Введите ID файла: ")))

    elif choise == '4':
        file_service.show_all_list()

    elif choise == '5':
        print("Сначала введите настоящий ID файла, а затем новый")
        file_service.change_id(int(input("Первый ID: ")), int(input("Второй ID: ")))

    elif choise == '6':
        len_of_list = int(input("Укажите кол-во файлов по ID: "))
        print("Укажите ID каждого файла: ")

        print(file_service.list_files_from_ids([int(input("→ ")) for i in range(len_of_list)]))

    elif choise == '7':
        print(file_service.backup_for_tf())

    elif choise == '8':
        try:
            directory = 'save_files'
            pathlist = Path(directory).glob('*')
            for key in file_service.data:
                print(str(key) + ": ", file_service.data[key])
            name_b = input(f"Выберите идентификатор файла:")
            file_service.recovery_with_backup(name_b)
        except:
            print("ID указан неправильно")

    elif choise == '9':
        print(f"Сейчас таймер на {file_service.sec} секунд ")
        file_service.sec = int(input("Укажите таймер в секундах: "))
        file_service.t.cancel()
        file_service.create_backup_auto()
        print(f"Таймер установлен на {file_service.sec} секунд ")
