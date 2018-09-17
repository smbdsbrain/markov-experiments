import random


async def phrase(request, phrase):
    markovify_words = random.choice(phrase.get('phrase', 'Hello!').split(' '))
    answer = request.app.model.make_sentence_with_start(markovify_words,
                                                        strict=False,
                                                        max_words=request.app.config.max_phrase_size)

    if not answer:
        answer = request.app.model.make_short_sentence(request.app.config.max_phrase_size)

    return {'answer': answer}
