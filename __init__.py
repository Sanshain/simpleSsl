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


import base64
import random
import time
from itertools import chain

from r_manager import RequestManager
from encryption import Secure







def Sniffer(func):

    def wrapper(*args, **kwargs):
        #  + func.__name__ + ' on '
        # tp = 'out' if args[0].__class__.__name__ == 'Server' else 'in'

        print ("steal request to server: " + str(args[1:]))

        return_value = func(*args, **kwargs)
        print ("steal server response: " + str(return_value))
        return return_value
    return wrapper



RAND = 199 # 99

class Server: # (object)
    username = "asa"
    password = "111111"
    token = None
    Content = '....... content for users ........'

    connections = RequestManager()

    def __init__(self):
        super(type(self), self).__init__()
        self.secure = Secure.Private(979999998077)   # 263

    def _encrypt(self, value, shft, psw=0):
        if ' ' in value:
            name, value = value.split(' ')
            rez = name + ' ' + Secure.Encrypt(value, shft, psw)
        else: rez = Secure.Encrypt(value, shft, psw)

        return rez

    def _decrypt(self, key_info, value):
        if value is tuple: value = value[1]
        elif value is str: value = value

        if type(key_info) == tuple:
             shft, psw = key_info
        else: shft, psw = key_info, 0
        # shft - open_shift


        rez = Secure.Decrypt(value, shft, psw)
        return rez


    def auth_petition(self):

        skey = random.randint(0, RAND)
        r_open_shift = Secure.Private.statement(skey)


        # serv
        pkey = random.randint(0, RAND * 48)
        r_open_psw = self.secure.istatement(pkey)

        conn_id = self.connections.append((skey, pkey, time.time()))


        # serv:
        # print secure.ipost_statement(r_open_psw_c, skey)

        # print str(r_open_psw).rjust(8,'0'),  str(r_open_psw_c).rjust(8,'0')

        return conn_id, r_open_shift, r_open_psw


    # def Auth(self, name_password, key, open_key):
    def Auth(self, name_password, open_shift, open_psw, conn_id):

        # skey, pkey, start_time = self.connections.pop(conn_id)                  # skey, pkey, start_time = self.connections[conn_id]
        skey, pkey, start_time = self.connections[conn_id]

        shift = Secure.Private.post_statement(open_shift, skey)
        psw = self.secure.ipost_statement(open_psw, pkey)




##
##        print (Secure.Private.post_statement(open_key, rkey))
##        print (Secure.Private.post_statement(r_open_key, key))

        name_password = name_password.split(':')
        if len(name_password) != 2: return 'wrong auth data'
        else:
            name, cry_password = name_password



        self.token = "Non authorizated", None, None
        if (self.username == name and self.password == self._decrypt((shift, psw), cry_password)):
            self.token = "token " + base64.b64encode(self.username + self.password)
            print ('token pushed: ' + self.token)

            skey = random.randint(0, RAND)
            r_open_shift = Secure.Private.statement(skey)
            r_shift = Secure.Private.post_statement(open_shift, skey)


            pkey = random.randint(0, RAND*48)
            r_open_psw = self.secure.istatement(pkey)
            r_psw = self.secure.ipost_statement(open_psw, pkey)


            token = self._encrypt(self.token, r_shift, r_psw)
            print ('token shift == ' + str(r_shift))

            # self.connections.append((skey, pkey, time.time()))
            self.connections[conn_id] = (skey, pkey, time.time())
            return token, r_open_shift, r_open_psw
        # encrypt
        return self.token


    def token_auth(self, conn_id, token, open_shift, open_psw):

        skey, pkey, resp_time = self.connections[conn_id]
        shft = Secure.Private.post_statement(open_shift, skey)
        psw = self.secure.ipost_statement(open_psw, pkey)

        tkn = token.split(' ')
        if len(tkn) == 2:
            token = ' '.join((tkn[0], self._decrypt((shft, psw), tkn[1])))




        skey = random.randint(0, RAND)
        r_shift = Secure.Private.post_statement(open_shift, skey)

        pkey = random.randint(0, RAND*48)
        r_psw = self.secure.ipost_statement(open_psw, pkey)

        cry_token = self._encrypt(self.token, r_shift, r_psw)


        self.connections[conn_id] = (skey, pkey, time.time())

        r_open_shift = Secure.Private.statement(skey)
        r_open_psw = self.secure.istatement(pkey)


        if self.token == token: return (conn_id, cry_token, r_open_shift, r_open_psw), self.Content
        else:
            return None, "Non authorizated"




class Client(object):

    server = Server()
    token = None
    # secure = Secure.Private()


    def input_and_auth(self, name, password):

        conn_id, r_openk_shift, r_openk_psw = self.auth_appeal()


        self.secure = Secure.Private(979999998077)                                    #263 # 97999797

        self.pkey = random.randint(0, RAND)
        enc_psw = self.secure.ipost_statement(r_openk_psw, self.pkey)                  # получили симмет ключ на основе отк ключа, получ с сервера

        self.skey = random.randint(0, RAND)
        shift = Secure.Private.post_statement(r_openk_shift, self.skey)

        r_open_psw = self.secure.istatement(self.pkey) # =>                            # сгенерировали отк ключ для генерации симм кл на сервере
        r_open_shift = Secure.Private.statement(self.skey) # =>                        print str(shift) + '--'


        cry_password = Secure.Encrypt(password, shift, enc_psw)

        cry_token, r_open_shift, r_open_psw = (
                self.request_for_auth(':'.join((name, cry_password)), r_open_shift, r_open_psw, conn_id)
        )

        if cry_token == "Non authorizated":
            print ("Non authorizated/ no token")
            return None
        else:
            return conn_id, cry_token, r_open_shift, r_open_psw


    def get_secure_content(self, token_info):

##        skey = random.randint(0, RAND)
##        r_open_shift = Secure.Private.statement(skey)
##        shift = Secure.Private.post_statement(r_open_shift, skey)
##        token = cry_token.split(' ')[0] + ' ' + Secure.Encrypt(cry_token.split(' ')[1], shift)

        if not token_info: return (None,)

        conn_id, cry_token, r_open_shift, r_open_psw = token_info

        r_shift = Secure.Private.post_statement(r_open_shift, self.skey)
        r_psw = self.secure.ipost_statement(r_open_psw, self.pkey)

        token = cry_token.split(' ')[0] + ' ' + Secure.Decrypt(cry_token.split(' ')[1], r_shift, r_psw)

        realm, token = token.split(' ')

        self.skey = random.randint(0, RAND)
        shift = Secure.Private.post_statement(r_open_shift, self.skey)

        self.pkey = random.randint(0, RAND*48)
        psw = self.secure.ipost_statement(r_open_psw, self.pkey)

        cry_token = realm + ' ' + Secure.Encrypt(token, shift, psw)

        open_shift = Secure.Private.statement(self.skey)
        open_psw = self.secure.istatement(self.pkey)

        return self.request_for_content(conn_id, cry_token, open_shift, open_psw)


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

        cry_token, r_open_shift, r_open_psw = self.server.Auth(name_password, openk_shift, openk_psw, conn_id)
        return cry_token, r_open_shift, r_open_psw

    @Sniffer
    def request_for_content(self, conn_id, token, open_shift, open_psw=0):

        return self.server.token_auth(conn_id, token, open_shift, open_psw)




def main():
    s = Client()
    token_info = s.input_and_auth("asa","111111")
    info = s.get_secure_content(token_info)
    s.get_secure_content(info[0])

    # print token
    # print base64.b64decode(token.split(' ')[1])

if __name__ == '__main__':
    main()


