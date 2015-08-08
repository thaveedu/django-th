# coding: utf-8
from django.conf import settings
from django.core.cache import caches


class PublishingLimit(object):
    """
        this class permits to reduce the quantity of data to be pulibshed
        get the limit from settings.DJANGO_TH['publishing_limit']
        if the limit does not exist, it return everything
    """
    @staticmethod
    def get_data(service, cache_data, trigger_id):
        """
            get the data from the cache
            :param service: the service name
            :param cache_data: the data from the cache
            :type trigger_id: integer
            :return: Return the data from the cache
            :rtype: object
        """

        # rebuild the string
        # th_<service>.my_<service>.Service<Service>
        if service.startswith('th_'):
            service_name = service.split('_')[1]
            service_long = ''.join((service, ".my_", service_name, ".Service",
                                    service_name.title()))
            # ... and check it
            if service_long in settings.TH_SERVICES:

                cache = caches[service]

                if 'publishing_limit' in settings.DJANGO_TH:
                    limit = settings.DJANGO_TH['publishing_limit']

                    if limit == 0:
                        return cache_data

                    if len(cache_data) > limit:
                        for data in cache_data[limit:]:
                            service_str = ''.join((service, '_',
                                                   str(trigger_id)))
                            cache.set(service_str, data)
                        cache_data = cache_data[:limit]

        return cache_data
