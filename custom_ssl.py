# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     01.07.2020
# Copyright:   (c) User 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from .r_manager import RequestManager

import base64
import random
import time
from itertools import chain



class Secure:

    class Stub:
        Encrypt = staticmethod(lambda s,n: s)
        Decrypt = staticmethod(lambda s,n: s)

    class Private(object):

        def __init__ (self, rest = 67): self.rest = rest
        istatement = lambda self, x: 3**x % self.rest
        ipost_statement = lambda self, a, b: a**b % self.rest

        rest = 67
        statement = staticmethod(lambda x, r=None: 3**x % (r or Secure.Private.rest))
        post_statement = staticmethod(lambda a, b, r=None: a**b % (r or Secure.Private.rest))



    class Simplest:

        abc = [chr(c) for c in chain(range(48,58), range(65,91),range(97,123))]

        @staticmethod
        def Encrypt(s, n):
            abc = Secure.Simplest.abc

            res = ''
            for c in s:
                res += abc[(abc.index(c) + n) % len(abc)]
            return res

        @staticmethod
        def Decrypt(s,n):
            abc = Secure.Simplest.abc

            res = ''
            for c in s:
                res += abc[(abc.index(c) - n) % len(abc)]
            return res


    approach = Simplest

    @staticmethod
    def Encrypt(s, n): return Secure.approach.Encrypt(s, n)

    @staticmethod
    def Decrypt(s,n): return Secure.approach.Decrypt(s, n)








def Sniffer(func):
    def wrapper(*args, **kwargs):
        #  + func.__name__ + ' on '
        # tp = 'out' if args[0].__class__.__name__ == 'Server' else 'in'

        print ("steal request to server: " + str(args[1:]))

        return_value = func(*args, **kwargs)
        print ("steal server response: " + str(return_value))
        return return_value
    return wrapper


gs = 0

class Server: # (object)
    username = "asa"
    password = "111111"
    token = None
    Content = 'secure content'

    connections = RequestManager()

    def _encrypt(self, value, key):
        if ' ' in value:
            name, value = value.split(' ')
            rez = name + ' ' + Secure.Encrypt(value, key)
        else: rez = Secure.Encrypt(value, key)

        return rez

    def _decrypt(self, key, value):
        if value is tuple: value = value[1]
        elif value is str: value = value

        # key - open_shift


        rez = Secure.Decrypt(value, key)
        return rez


    def auth_petition(self):



        skey = random.randint(0, 67)
        r_open_shift = Secure.Private.statement(skey)

        self.secure = Secure.Private(97999797)

        # serv
        pkey = random.randint(0, 67)
        r_open_psw = self.secure.istatement(pkey)

        conn_id = self.connections.append((skey, pkey, time.time()))


        # serv:
        # print secure.ipost_statement(r_open_psw_c, skey)

        # print str(r_open_psw).rjust(8,'0'),  str(r_open_psw_c).rjust(8,'0')

        return conn_id, r_open_shift, r_open_psw


    # def Auth(self, name_password, key, open_key):
    def Auth(self, name_password, open_shift, open_psw, conn_id):

        skey, pkey, start_time = self.connections.pop(conn_id)                  # skey, pkey, start_time = self.connections[conn_id]

        shift = Secure.Private.post_statement(open_shift, skey)
        psw = secure.ipost_statement(open_psw, pkey)



##        rkey = random.randint(0, 67)
##        r_open_key = Secure.Private.statement(rkey)
##
##        print (Secure.Private.post_statement(open_key, rkey))
##        print (Secure.Private.post_statement(r_open_key, key))

        name_password = name_password.split(':')
        if len(name_password) != 2: return 'wrong auth data'
        else:
            name, cry_password = name_password



        self.token = "Non authorizated"
        if (self.username == name and self.password == self._decrypt(shift, cry_password)):
            self.token = "token " + base64.b64encode(self.username + self.password)
            print ('token pushed: ' + self.token)
            token = self._encrypt(self.token, rkey)
            return token, rkey
        # encrypt
        return self.token


    def token_auth(self, token, key):

        tkn = token.split(' ')
        if len(tkn) == 2:
            token = ' '.join((tkn[0], self._decrypt(key, tkn[1])))

        if self.token == token: return '> ' + self.Content
        else:
            return "Non authorizated"


class Client(object):

    server = Server()
    token = None


    def input_and_auth(self, name, password):

        conn_id, r_openk_shift, r_openk_psw = self.auth_appeal()


        secure = Secure.Private(97999797)

        rkey = random.randint(0, 67)
        enc_psw = secure.ipost_statement(r_openk_psw, rkey)                     # получили симмет ключ на основе отк ключа, получ с сервера
        print enc_psw

        r_open_psw = secure.istatement(rkey) # =>                               # сгенерировали отк ключ для генерации симм кл на сервере

        skey = random.randint(0, 67)
        shift = Secure.Private.post_statement(r_openk_shift, skey)

        r_open_shift = Secure.Private.statement(skey) # =>                      print str(shift) + '--'


        cry_password = Secure.Encrypt(password, shift)
        token, skey = self.request_for_auth(':'.join((name, cry_password)), r_open_shift, r_open_psw, conn_id)
        if token == "Non authorizated":
            print ("Non authorizated/ no token")
            return None
        else:
            self.token = token.split(' ')[0] + ' ' + Secure.Decrypt(token.split(' ')[1], skey)
            return self.token


    def get_secure_content(self, token):
        realm, token = token.split(' ')
        key = random.randint(0, 67)
        cry_token = Secure.Encrypt(token, key)
        return self.request_for_content(realm + ' ' + cry_token, key)


    @Sniffer
    def auth_appeal(self):
        """
        Peition for auth session (handshake appeal to the server)
        """
        conn_id, r_openk_shift, r_openk_psw = self.server.auth_petition()

        return conn_id, r_openk_shift, r_openk_psw

        # print psw
        # auth_data = psw(data) =>




    @Sniffer
    def request_for_auth(self, name_password, openk_shift, openk_psw, conn_id):

        token, key = self.server.Auth(name_password, openk_shift, openk_psw, conn_id)
        return token, key

    @Sniffer
    def request_for_content(self, token, key):

        return self.server.token_auth(token, key)




def main():
    s = Client()
    token = s.input_and_auth("asa","111111")
    s.get_secure_content(token)
    s.get_secure_content(token)

    # print token
    # print base64.b64decode(token.split(' ')[1])

if __name__ == '__main__':
    main()


