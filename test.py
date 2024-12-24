import json
from eth_keyfile import extract_key_from_keyfile

# Путь к вашему keystore-файлу
keyfile_path = r"E:\geth_network\keystore\UTC--2024-12-22T20-01-46.565106400Z--add70f3aa1a6bff0f574c205083df15f189dc3e4"

# Введите пароль, который вы указали при создании аккаунта
password = input("Введите пароль от аккаунта: ").encode()

# Расшифровка файла
with open(keyfile_path) as keyfile:
    private_key = extract_key_from_keyfile(keyfile, password)

# Вывод приватного ключа
print("Приватный ключ:", private_key.hex())
