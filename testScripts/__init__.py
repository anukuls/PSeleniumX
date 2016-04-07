#http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python

# from os.path import dirname, basename, isfile
# import glob
# modules = glob.glob(dirname(__file__)+"/**/*.py")
# print "modules are : ", modules
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

#NOTE: below works with hardcoding
# from SuiteD import google_search
# from SuiteC import google_search

# __all__ = ["google_search", "google_search"]

# import sys

# somehow modnames should be a list of strings that are the names of config files
#
# you can do this more dynamically depending on what you're doing                                                                                                     
# modnames = ['SuiteC.google_search']
# 
# for modname in modnames:
#     exec('import %s' % modname)
# 
#     for modname in modnames:
#         mod = sys.modules[modname]
#         print mod
#         for k in mod.__dict__:
#             if k[:2] != '__':
#                 print modname, k, mod.__dict__[k]

#http://stackoverflow.com/questions/3365740/how-to-import-all-submodules
import pkgutil

__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    module = loader.find_module(module_name).load_module(module_name)
    exec('%s = module' % module_name)