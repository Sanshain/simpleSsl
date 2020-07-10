# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        r_manager
# Purpose:
#
# Author:      User
#
# Created:     03.07.2020
# Copyright:   (c) User 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class RequestManager:

    """
    Dict with unique key autogeneration
    """

    __getitem__ = lambda self, cn_id: self._dict[cn_id]
    def __setitem__(self, cn_id, value):
        self._dict[cn_id] = value


    def __init__(self, _dct=None):
        self._dict = _dct or {}
        self.removed = []
        self._next = (max(self._dict.keys()) + 1) if self._dict else 0

    def pop(self, cn_id):
        val = self._dict.pop(cn_id, None)
        if val: self.removed.append(cn_id)
        return val

    def append(self, values):
        key = self._get_next()
        self._dict[key] = values
        return key

    def _get_next(self):
        if len(self.removed) > 0:
            key = self.removed.pop()
            return key
        else:
            _next = self._next
            self._next += 1
            return _next





    # has_key
    # del


