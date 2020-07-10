#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     09.07.2020
# Copyright:   (c) User 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from itertools import chain, cycle
import base64
import random

sh_multiplier = 17      # 10

class Secure:

    Abc = [chr(c) for c in chain(range(48,58), range(65,91),range(97,123))]

    class Stub:
        Encrypt = staticmethod(lambda s,n: s)
        Decrypt = staticmethod(lambda s,n: s)

    class Caesar:

        @staticmethod
        def Encrypt(text, n, *args):
            abc = Secure.Abc

            res = ''
            for c in text:
                res += abc[(abc.index(c) + n) % len(abc)]
            return res

        @staticmethod
        def Decrypt(text,n, *args):
            abc = Secure.Abc

            res = ''
            for c in text:
                res += abc[(abc.index(c) - n) % len(abc)]
            return res

    class Vijner:

        @staticmethod
        def Encrypt(text, keytext, *args):
            alphabet = Secure.Abc
            rest - len(alphabet)
            if type(keytext) != str:
                keytext *= 2
                keytext = keytext.__str__()
            f = lambda arg: alphabet[((alphabet.index(arg[0])+alphabet.index (arg[1]))%rest)]
            return ''.join(map(f, zip(text, cycle(keytext))))

        @staticmethod
        def Decrypt(coded_text, keytext, *args):
            alphabet = Secure.Abc
            rest - len(alphabet)
            if type(keytext) != str:
                keytext *= 2
                keytext = keytext.__str__()
            f = lambda arg: alphabet[alphabet.index(arg[0])-alphabet.index(arg[1])]
            return ''.join(map(f, zip(coded_text, cycle(keytext))))


    class Combo:

        @staticmethod
        def Encrypt(text, shift, keytext):
            weak_encr_text = Secure.Caesar.Encrypt(text, shift)
            full_cry_text = Secure.Vijner.Encrypt(weak_encr_text, keytext)
            return full_cry_text

        @staticmethod
        def Decrypt(coded_text, shift, keytext):
            weak_encr_text = Secure.Vijner.Decrypt(coded_text, keytext)
            text = Secure.Caesar.Decrypt(weak_encr_text, shift)
            return text


    class Private(object):

        # instance methods for password generation:

        def __init__ (self, rest = 979999998077): self.rest = rest              # 67
        istatement = lambda self, x: (sh_multiplier**x) % self.rest
        ipost_statement = lambda self, a, b: (a**b) % self.rest

        @staticmethod
        def i3_statement(lvls = None):

            lvls = [random.randint(0, 199) for i in range(3)]
            istatement = lambda x: (65**x) % 839
            o_keys = tuple(istatement(lvl) for lvl in lvls)
            rez = ''.join([str(lv).rjust(3,'0') for lv in o_keys])
            return rez, lvls

        @staticmethod
        def i3post_statement(o_kyes, skeys):

            ipost_statement = lambda ml, lv: (ml**lv) % 839
            o_kyes = [int(o_kyes[i:i + 3]) for i in range(0, len(o_kyes), 3)]
            keys = [ipost_statement(o_kyes[i],skey) for i, skey in enumerate(skeys)]
            rez = ''.join([str(k).rjust(3,'0') for k in keys])
            return rez

        # for make calculats the faster do separated operation for three-digit keys.
        # Need repartition for some code in Ssl realization


##        istatement = lambda self, lvl: Secure.Private.i3_statement()
##        ipost_statement = lambda self, ml, lvl: Secure.Private.i3post_statement(ml, lvl)





        # static methods for the shift generation

        rest = 263                                                              # 979999998077
        gt_multiplier = 10                                                      # 17

        statement = staticmethod(lambda lvl: Secure.Private.gt_multiplier**lvl % Secure.Private.rest)
        post_statement = staticmethod(lambda mpl, lvl, r=None: mpl**lvl % (r or Secure.Private.rest))


    approach = Combo # Vijner # Caesar

    @staticmethod
    def Encrypt(s, shft, key = 0):
        return Secure.approach.Encrypt(s, shft, key)

    @staticmethod
    def Decrypt(s, shft, key = 0):
        return Secure.approach.Decrypt(s, shft, key)















alphabet = [chr(c) for c in chain(range(65,91),range(97,123),range(48,58))]
rest = len(alphabet)

def encode_vijn(text, keytext):
    if type(keytext) != str:
        keytext *= 2
        keytext = keytext.__str__()
    f = lambda arg: alphabet[((alphabet.index(arg[0])+alphabet.index (arg[1]))%rest)]
    return ''.join(map(f, zip(text, cycle(keytext))))


def decode_vijn(coded_text, keytext):
    if type(keytext) != str:
        keytext *= 2
        keytext = keytext.__str__()
    f = lambda arg: alphabet[alphabet.index(arg[0])-alphabet.index(arg[1])]
    return ''.join(map(f, zip(coded_text, cycle(keytext))))






if __name__ == '__main__':
    # txt = encode_vijn ('111111', 0)
    txt = Secure.Combo.Encrypt('111111', 2, 123456)
    print (txt)
    # txt = decode_vijn(txt, 0)
    txt = Secure.Combo.Decrypt(txt, 2, 123456)
    print (txt)

    print dict(enumerate(alphabet))

