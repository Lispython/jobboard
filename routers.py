# -*- coding:  utf-8 -*-



class AuthRouter(object):
    """A router to control all database operations on models in
    the contrib.auth application"""

    def db_for_read(self, model, **hints):
        "Point all operations on auth models to 'credentials'"
        if model._meta.app_label == 'auth':
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on auth models to 'credentials'"
        if model._meta.app_label == 'auth':
            return 'users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in Auth is involved"
        return True
        if obj1._meta.app_label == 'auth' or obj2._meta.app_label == 'auth':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the auth app only appears on the 'credentials' db"
        if db == 'users':
            return model._meta.app_label == 'auth'
        elif model._meta.app_label == 'auth':
            return False
        return None



class AuthOpenIDRouter(object):
    """A router to control all database operations on models in
    the authopenid application"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'authopenid':
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on auth models to 'credentials'"
        if model._meta.app_label == 'authopenid':
            return 'users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in Auth is involved"
        return True
        if obj1._meta.app_label == 'authopenid' or obj2._meta.app_label == 'authopenid':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the auth app only appears on the 'credentials' db"
        if db == 'users':
            return model._meta.app_label == 'authopenid'
        elif model._meta.app_label == 'authopenid':
            return False
        return None


class MasterSlaveRouter(object):
    """A router that sets up a simple master/slave configuration"""

    def db_for_read(self, model, **hints):
        "Point all read operations to a random slave"
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all write operations to the master"
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation between two objects in the db pool"
        db_list = ('master','slave1','slave2')
        if obj1 in db_list and obj2 in db_list:
            return True
        return None

    def allow_syncdb(self, db, model):
        "Explicitly put all models on all databases."
        return True
