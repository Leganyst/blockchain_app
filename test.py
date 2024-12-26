import json
from eth_keyfile import extract_key_from_keyfile

# Путь к вашему keystore-файлу
keyfile_path = r"E:\geth_network\keystore\UTC--2024-12-25T10-04-29.800657100Z--ec936f8b946a0baf7cfcf11b3b475a930c9ab396"

# Введите пароль, который вы указали при создании аккаунта
password = input("Введите пароль от аккаунта: ").encode()

# Расшифровка файла
with open(keyfile_path) as keyfile:
    private_key = extract_key_from_keyfile(keyfile, password)

# Вывод приватного ключа
print("Приватный ключ:", private_key.hex())
