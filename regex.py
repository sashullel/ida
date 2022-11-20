import random
import re
import string


def generate_password(n: int):
    cyrillic = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    symbols = list(string.ascii_letters + string.digits + string.punctuation + cyrillic)
    # в символах не задан пробел, поэтому по сути пробельные знаки в паттерне необязательно исключать?
    pattern = r"^(?=.*[A-ZА-ЯЁ]{2,})(?=.*[a-zа-яё]{2,})(?=.*[A-ЯЁа-яёA-Za-z])(?=.*[0-9])(?!.*[0-9]{3})(?!.*[\s]).*$"

    valid_password = None
    while not valid_password:
        password = ''.join(random.choices(symbols, k=n))
        valid_password = re.findall(pattern, password)

    print(*valid_password)


generate_password(12)
