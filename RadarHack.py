import pymem
import pymem.process
import re
import webbrowser
import time
import keyboard

def main():
    try:
        # Подключение к процессу игры
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll")
        client_module = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)

        # Поиск адреса
        address = client.lpBaseOfDll + re.search(rb'\x74\x15\x8B\x47\x08\x8D\x4F\x08', client_module).start() - 1
    except (pymem.process.exception.ProcessNotFound, AttributeError, TypeError):
        # Если игра не найдена или произошла ошибка, открываем игру и ждем 60 секунд
        webbrowser.open('steam://rungameid/730') #Запуск игры если она выключена
        time.sleep(60)
        try:
            # Повторная попытка подключения к процессу игры
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll")
            client_module = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)

            # Повторный поиск адреса
            address = client.lpBaseOfDll + re.search(rb'\x74\x15\x8B\x47\x08\x8D\x4F\x08', client_module).start() - 1
        except (pymem.process.exception.ProcessNotFound, AttributeError, TypeError):
            exit()

    # Функция изменения значения по найденному адресу
    def radar_hack():
        pm.write_uchar(address, 0 if pm.read_uchar(address) != 0 else 2)

        # Улучшенное обнаружение противников
        # Добавьте здесь свой код для улучшенного обнаружения противников на радаре.
        # Можете использовать дополнительные маркеры, цветовую индикацию или звуковые сигналы.

    # Пользовательская функция для привязки клавиши
    def set_key_binding():
        print("Введите клавишу для привязки (например, F1):")
        while True:
            try:
                key = keyboard.read_key()
                print(f"Клавиша привязки установлена на {key}")
                return key
            except keyboard.KeyboardInterrupt:
                print("Прервано пользователем. Попробуйте снова.")

    # Установка клавиши привязки
    key_bind = set_key_binding()

    # Бесконечный цикл для прослушивания нажатий клавиши привязки и включения/выключения функций
    is_enabled = False
    print("Скрипт запущен. Нажмите клавишу привязки для включения/выключения функций.")
    while True:
        try:
            if keyboard.is_pressed(key_bind):
                is_enabled = not is_enabled
                if is_enabled:
                    print("Функции включены.")
                else:
                    print("Функции выключены.")
                time.sleep(0.2)  # Задержка для предотвращения множественного включения/выключения
        except keyboard.KeyboardInterrupt:
            print("Прервано пользователем.")
            break

        # Выполнение функции при включенном состоянии
        if is_enabled:
            radar_hack()

        time.sleep(0.01)  # Минимальная задержка для снижения нагрузки на процессор

    pm.close_process()

if __name__ == '__main__':
    main()
