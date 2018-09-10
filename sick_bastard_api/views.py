
async def phrase(request, phrase):
    answer = request.app.model.make_short_sentence(request.app.config.max_phrase_size)
    return {'answer': answer}
