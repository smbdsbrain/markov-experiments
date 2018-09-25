from sick_bastard_api.utils import make_answer


async def phrase(request, phrase):
    return {
        'answer': make_answer(
            phrase.get('phrase', 'Hello!'),
            request.app.model,
            request.app.config.max_phrase_size
        )
    }


async def alice(request, phrase):
    response = {
        "version": phrase['version'],
        "session": phrase['session'],
        "response": {
            "end_session": False
        }
    }

    if phrase['session']['new']:
        response['response']['text'] = \
            'Привет! Этот навык наизусть знает учебники по C++,C и Python, ' \
            'а также произведения Довлатова!' \
            'Просто скажи любую фразу и он продолжит ее опираясь на свои знания'
    else:
        response['response']['text'] = make_answer(
            phrase.get('request', {}).get('command', 'Hello!'),
            request.app.model,
            request.app.config.max_phrase_size,
        )

    return response
