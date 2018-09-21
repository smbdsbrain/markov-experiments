import random


def make_answer(phrase: str, model, max_phrase_size=140):
    markovify_words = random.choice(phrase.split(' '))
    answer = model.make_sentence_with_start(markovify_words,
                                            strict=False,
                                            max_words=max_phrase_size)

    if not answer:
        answer = model.make_short_sentence(max_phrase_size)

    return answer
