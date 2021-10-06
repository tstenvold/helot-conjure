
import messages

from RestrictedPython import compile_restricted,safe_globals
from RestrictedPython.Eval import default_guarded_getiter,default_guarded_getitem
from RestrictedPython.Guards import guarded_iter_unpack_sequence,safer_getattr,full_write_guard

import string
import math
import random
from PIL import Image
import urllib.request


#Sandbox enviro variables extending safe_globals
safe_globals['__name__'] = 'restricted namespace'
safe_globals['_getiter_'] = default_guarded_getiter
safe_globals['_getitem_'] = default_guarded_getitem
safe_globals['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
safe_globals['getattr'] = safer_getattr
safe_globals['__write__'] = full_write_guard

#Sanbox import modules
safe_globals['Image'] = Image
safe_globals['request'] = urllib.request
safe_globals['string'] = string
safe_globals['math'] = math
safe_globals['random'] = random
safe_globals['whrandom'] = random
safe_globals['set'] = set
safe_globals['frozenset'] = frozenset


def run_code(jCode):
        result = ''
        ex_locals = {}

        try:
            byte_code = compile_restricted(jCode, filename='<inline code>', mode='exec')
            exec(byte_code, safe_globals, ex_locals)
            result = ex_locals['result']
        except: 
            result = messages.INVALIDCODE

        return result