import os
import shutil
import time


BACKUP_PREFIX = 'backup_'


def walk_dir(dirfn, is_valid_file=None):
    filetree = os.walk(dirfn, topdown=False)

    is_valid_file = is_valid_file or (lambda fn: True)

    def is_backup(fn):
        basefn = os.path.basename(fn)
        return basefn.startswith(BACKUP_PREFIX)
        
    files = [os.path.normpath(os.path.join(root, fn)) for 
             root, dirs, files in filetree for
             fn in files if not is_backup(fn) and is_valid_file(fn)]
    return files

def shorten_fn(fn):
    head, tail = os.path.split(fn)
    fn_parts = []
    while tail:
        fn_parts.append(tail)
        head, tail = os.path.split(head)
        
    fn_parts.reverse()
    fn_parts = fn_parts[-2:]
    fn_parts.insert(0, '(...)')
    short_fn = os.path.sep.join(fn_parts)
    return short_fn


def make_backup(fn):
    dirn = os.path.dirname(fn)
    basefn = os.path.basename(fn)
    timestamp = time.strftime("%d%m%y%H%M%S", time.localtime())
    backup_fn = os.path.join(dirn, '%s%s_%s' % (BACKUP_PREFIX, timestamp, basefn))
    print 'create backup %s: %s' % (fn, backup_fn)
    shutil.copyfile(fn, backup_fn)
    print 'ok'

