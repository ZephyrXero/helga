import random

from giphypop import Giphy, GiphyApiException

from helga.extensions.base import CommandExtension


class GiphyExtension(CommandExtension):
    """
    A plugin for all things gifs
    """
    NAME = 'giphy'

    usage = '[BOTNICK] (gif|gifme) [<search_term> ...]'

    sad_panda = [
        "Well this is embarassing...",
        "Yeah I've got nothing %(nick)s",
        "I couldn't find anything for you %(nick)s",
        "PC LOAD LETTER",
    ]

    def __init__(self, *args, **kwargs):
        self.api = Giphy(strict=True)
        super(GiphyExtension, self).__init__(*args, **kwargs)

    def handle_message(self, opts, message):
        search = ' '.join(opts['<search_term>'])
        message.response = self.gifme(search=search)

    def gifme(self, search=None):
        """
        Hook into giphypop to find a gif. If no search term, just
        return a random gif. If a search term is given, try to translate
        it and default back to a search
        """
        try:
            return self.api.random_gif(search).media_url
        except GiphyApiException:
            try:
                return self.api.translate(search).media_url
            except GiphyApiException:
                try:
                    return self.api.search_list(search, limit=1)[0].media_url
                except GiphyApiException:
                    pass

        return random.choice(self.sad_panda)
