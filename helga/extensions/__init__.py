from helga import settings
from helga.extensions.base import HelgaExtension
from helga.log import setup_logger


logger = setup_logger(__name__)


class ExtensionRegistry(object):

    def __init__(self, bot, load=False):
        self.ext = set()
        self.bot = bot

        if load:
            self.load()

    def load(self):
        for path in getattr(settings, 'EXTENSIONS', []):
            logger.debug('Loading extension extension %s' % path)

            try:
                mod = __import__(path, {}, {}, [path.split('.')[-1]])
            except ImportError:
                logger.warning('Cannot import extension %s' % path)
                continue

            # See if there are any HelgaExtensions
            for member in filter(lambda x: not x.startswith('__'), dir(mod)):
                try:
                    cls = getattr(mod, member)
                    if issubclass(cls, HelgaExtension) and cls != HelgaExtension:
                        self.ext.add(cls(bot=self.bot))
                except TypeError:
                    continue

    def dispatch(self, bot, nick, channel, message, is_public):
        for ext in self.ext:
            try:
                resp = ext.dispatch(bot, nick, channel, message, is_public)
            except:
                logger.exception('Unexpected failure. Skipping extension')
                continue

            if resp:
                return resp

        return None