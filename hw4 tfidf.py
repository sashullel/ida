from math import log
from collections import Counter, defaultdict
from typing import Iterable

import pymorphy2
import re

morph = pymorphy2.MorphAnalyzer()

text_corpus = [
    "Как выжить в современной России.",
    "Никогда не берите в руки нож.",
    "Не покупайте водку.",
    "Просыпайся в 7 утра.",
    "Никогда не ешьте котов",
    "Не ешьте то, что не можете позволить себе купить.",
    "Уберитесь в квартире.",
    "В любой непонятной ситуации - ешь мясо!",
    "Не ешьте мясо, если хотите жить долго и счастливо.",
    "Не попадаться на глаза сотрудникам полиции. Выйти из дома с сумкой, на которой написано “Я не верблюд",
    "Не ешьте камни. Не ешьте ничего, кроме собаки.",
    "Не ешьте собаку.",
    "Не ешьте мышей. Не ешьте кошек.",
    "Не ешьте котиков. Не ешьте мышь. Не ешьте сыр.",
    "Не ешьте никого. Не ешьте кота.",
    "Покупать себе только то, что выгодно, например, покупать дешевый алкоголь в магазине, который находится в подвале.",
    "Не иметь друзей.",
    "Не говорить с незнакомцами. Не разговаривать с незнакомыми людьми.",
    "Перестать бояться незнакомых людей, перестать бояться незнакомцев.",
    "Не общаться с незнакомыми девушками. Не общаться со знакомыми девушками.",
    "Не говорить девушкам, что они нравятся тебе. Не говорить, что нравишься им."
    "Не говорить им, что любишь их. Не встречаться с ними. Не влюбляться в них. Не рассказывать им о своих чувствах.",
    'В современных российских условиях вопрос выживания становится все более актуальным. И не столько для тех, кто живет "на земле", сколько для интеллигенции, представителей творческих профессий и, конечно, для студентов. В этой связи особенно важно, чтобы каждый из нас смог определить для себя жизненные ценности, которые помогут ему сохранить себя, свою человеческую сущность и остаться человеком в экстремальных условиях.',
    'Как выжить в современной России. У нас есть три способа: 1) стать жертвой маньяка; 2) стать жертвой другого маньяка, которого мы убьем; 3) стать жертвой не маньяка.',
    'Покупать все продукты в магазине "Магнит" и ходить в церковь.',
    'Никогда не ложитесь спать, будучи голодными;',
    'Кушать бублики с маком. Бубликов с маком много.',
    'Не ходить в церковь; Не верить в бога; Не пить водку; Не работать.',
]


def preprocess_text(text: str) -> list[str]:
    text = re.split(r'[ .,!:;?\[\]\-\'"“)(<>*@`_]+', text.lower())
    clean_text = list(filter(None, text))
    return [morph.parse(word)[0].normal_form for word in clean_text]


def calc_tf(term: str, text: str):
    text = preprocess_text(text)
    requested = text.count(morph.parse(term)[0].normal_form)
    most_common = Counter(text).most_common(1)[0][1]
    return 0.5 + 0.5 * (requested / most_common)


def calc_idfs(corpus: Iterable[str]) -> dict:
    all_words = [token for text in corpus for token in preprocess_text(text)]
    return defaultdict(int, {term: log(len(corpus) / (1 + all_words.count(term)))
                             for text in corpus for term in preprocess_text(text)})


def calc_tfidf(term: str, text: str, precomputed_idfs: dict) -> float:
    return precomputed_idfs[term] * calc_tf(term, text)


idfs = calc_idfs(text_corpus)

print(calc_tfidf('не', text_corpus[12], idfs))

print('here\'s its tfidf in one of the texts: ',
      calc_tfidf(term=input('enter a word: '), text=text_corpus[5], precomputed_idfs=idfs))