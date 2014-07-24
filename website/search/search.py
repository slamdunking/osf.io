from website import settings
import logging


# Abstracts search away from solr
logger = logging.getLogger('website.search.search')

if settings.SEARCH_ENGINE == 'solr':
    import solr_search as search_engine
elif settings.SEARCH_ENGINE == 'elastic':
    import elastic_search as search_engine
else:
    search_engine = None
    logger.warn('Neither elastic or solr are set to load')


def requires_search(func):
    def wrapped(*args, **kwargs):
        if search_engine is not None:
            return func(*args, **kwargs)
    return wrapped


@requires_search
def search(query, start=0):
    result, tags, counts = search_engine.search(query, start)
    return result, tags, counts


@requires_search
def update_node(node):
    search_engine.update_node(node)


@requires_search
def update_user(user):
    search_engine.update_user(user)


@requires_search
def delete_all():
    search_engine.delete_all()


@requires_search
def search_contributor(query, exclude=None):
    result = search_engine.search_contributor(query, exclude)
    return result
