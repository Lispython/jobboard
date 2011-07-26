# -*- coding:  utf-8 -*-

from django.contrib.sessions.backends.base import SessionBase, CreateError

from lib.common import mongo


class SessionStore(SessionBase):
    """
    A mongo-based session store.
    """

    def __init__(self, session_key=None):
        self.mongo = mongo
        super(SessionStore, self).__init__(session_key)

    def load(self):
        session_data = self.mongo.sessions.find_one({
            u'session_key': self.session_key})
        if session_data is not None:
            return dict(session_data)
        self.create()
        return {}

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                # Would be raised if the key wasn't unique
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        data = dict(self._get_session(no_load=must_create))
        data[u'session_key'] = self.session_key
        if must_create:
            if not self.exists(self.session_key):
                self.mongo.sessions.insert(data)
            else:
                raise CreateError
        else:
            self.mongo.sessions.update({u'session_key': self.session_key}, data)

    def exists(self, session_key):
        if self.mongo.sessions.find({u'session_key': session_key}).count() > 0:
            return True
        return False

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        self.mongo.sessions.remove({u'session_key': session_key})
