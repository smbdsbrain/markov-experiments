
async def phrase(request, phrase):
    answer = request.app.model.make_sentence()
    return {'answer': answer}
