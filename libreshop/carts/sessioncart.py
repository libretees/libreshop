import logging

logger = logging.getLogger(__name__)

UUID = 'b37d96da-006e-4ba1-945c-ca4f3b318eea'

class SessionCart(list):

    def __init__(self, session, *args, **kwargs):
        super(SessionCart, self).__init__(*args, **kwargs)

        logger.info('Getting %s...' % self.__class__.__name__)

        if not session.has_key(UUID):
            logger.info('Could not find a %s!' % self.__class__.__name__)
            session[UUID] = list()
        else:
            logger.info('Found %s!' % self.__class__.__name__)
            self += session.get(UUID)

        self.session = session


    def append(self, item):
        super(SessionCart, self).append(item)
        self.session[UUID] = list(self)


    def add(self, item):
        logger.debug('request.session: %s' % self.session[UUID])
        logger.info('Adding product to %s...' % self.__class__.__name__)

        self.append(item)

        logger.info('Added product to %s.' % self.__class__.__name__)
        logger.debug('request.session: %s' % self.session[UUID])


    @property
    def has_products(self):
        return bool(len(self))
