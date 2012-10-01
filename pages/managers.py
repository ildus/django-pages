'''Managers for pages classes, can be used to easies access for models
'''
from django.db import models


class ActiveQuerySet(models.query.QuerySet):
    '''QuerySet has additional methods to siplify access to active items
    '''

    def active(self):
        '''Get only active items
        '''
        return self.filter(is_active=True)

    def inactive(self):
        '''Get only inactive items
        '''
        return self.filter(is_active=False)

    def make_active(self):
        '''Mark items as active
        '''
        return self.update(is_active=True)

    def mark_inactive(self):
        '''Mark items as inactive
        '''
        return self.update(is_active=False)


class ActiveManager(models.Manager):
    '''Manager that creates ActiveQuerySet
    '''

    def get_query_set(self):
        '''Create an ActiveQuerySet
        '''
        return ActiveQuerySet(self.model, using=self._db)

    def active(self):
        '''Get only active items
        '''
        return self.get_query_set().active()

    def inactive(self):
        '''Get only inactive items
        '''
        return self.get_query_set().inactive()


class LayoutManager(ActiveManager):
    '''Manager for Layout model. Contains method to sipmlify access to default
    record
    '''

    def get_default(self):
        '''Get default
        '''
        return self.get(is_default=True)
