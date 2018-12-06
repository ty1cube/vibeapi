# from .base import *\

try:
    from .local import *
except:
    from .production import *


# import sys
# if 'runserver' in sys.argv:
#     from .local import * 
# else:
#     from .production import *
