import random
import re
import string


def generate_password(n: int):
    if n < 4:
        print('password must contain at least 4 characters')
        return None
    cyrillic = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    symbols = list(string.ascii_letters + string.digits + string.punctuation + cyrillic)
    # в символах не задан пробел, поэтому по сути пробельные знаки в паттерне необязательно исключать?
    pattern = r"^(?=.*[A-ZА-ЯЁ]{2,})(?=.*[a-zа-яё]{2,})(?=.*[A-ЯЁа-яёA-Za-z])(?=.*[0-9])(?!.*[0-9]{3})(?!.*[\s]).*$"

    valid_password = None
    print('generating a password..')
    while not valid_password:
        password = ''.join(random.choices(symbols, k=n))
        valid_password = re.findall(pattern, password)

    print(*valid_password)


generate_password(3)  # password must contain at least 4 characters
generate_password(12)  # ЩИы"%9элт4)$
