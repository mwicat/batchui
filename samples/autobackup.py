import sys
import os

import batchui.batchui as batchui
import shutil


COLUMNS = [('fn', 'Filename'),
           ('has_backup', 'Has backup'),
           ('status_text', 'Status')]


def parse_file(fn, preferences, parameters):
    fn_backup = '%s.bak' % fn
    has_backup = 'Yes' if os.path.exists(fn_backup) else 'No'
    item = {'fn': fn,
            'has_backup': has_backup}
    return item


def process_item(item, should_backup, preferences, parameters):
    fn = item.data['fn']
    fn_backup = '%s.bak' % fn
    shutil.copyfile(fn, fn_backup)


if __name__ == '__main__':
    batchui.run(sys.argv,
                'AutoBackup',
                parse_file=parse_file,
                process_item=process_item,
                columns=COLUMNS)
