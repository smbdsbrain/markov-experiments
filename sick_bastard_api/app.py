import aioworkers_aiohttp.app
import markovify


class Application(aioworkers_aiohttp.app.Application):
    def __init__(self, config, *, context, **kwargs):
        super(Application, self).__init__(config, debug=config.debug, context=context, **kwargs)
        with open('model.json', 'r') as f:
            model_json = f.read()

        self.model = markovify.Text.from_json(model_json)

        del model_json
