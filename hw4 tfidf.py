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
    text = re.split(r'\W+', text.lower())
    clean_text = list(filter(None, text))
    # если сделать каст в set на данном этапе, то не получится подсчитать most_common_term_freq in calc_tf
    return [morph.parse(word)[0].normal_form for word in clean_text]


def calc_tf(term: str, text: str):
    text = preprocess_text(text)
    # если мы не будем tf считать отдельно, то здесь лемматизацию можно не делать, тк она есть в calc_tfidf
    requested_term_freq = text.count(morph.parse(term)[0].normal_form)
    most_common_term_freq = Counter(text).most_common(1)[0][1]  # сначала берем 1-ый эл-т списка, потом 2 эл-т кортежа
    return 0.5 + 0.5 * (requested_term_freq / most_common_term_freq)


def calc_idfs(corpus: Iterable[str]) -> dict:
    processed_corpus = [preprocess_text(text) for text in corpus]
    unique_terms = list(set([term for text in processed_corpus for term in text]))
    idf_dict = defaultdict(int, )

    for unique_term in unique_terms:
        docs_with_term = [unique_term in text for text in processed_corpus].count(True)
        idf = log(len(corpus) / (1 + docs_with_term))
        idf_dict[unique_term] = idf

    return idf_dict


def calc_tfidf(term: str, text: str, precomputed_idfs: dict) -> float:
    processed_term = morph.parse(term)[0].normal_form
    return precomputed_idfs[processed_term] * calc_tf(processed_term, text)


idfs = calc_idfs(text_corpus)
print(idfs)

print(calc_tfidf('не', text_corpus[12], idfs))  # 0.30010459245033816
print(calc_tfidf('верблюд', text_corpus[-1], idfs))  # 1.3013448427221919

given_word = morph.parse(input('give some word: '))[0].normal_form
given_idx = input('give the text idx: ')
print('here\'s its tfidf in the given text: ', calc_tfidf(term=given_word,
                                                          text=given_idx,
                                                          precomputed_idfs=idfs))