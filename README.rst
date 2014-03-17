===========
BatchUI
===========

GUI framework for creating applications doing batch operations.
Think BatchRename or MP3 taggers.

.. image:: https://github.com/mwicat/batchui/releases/download/v0.0.1/screenshot1.png

Installation
------------

From source
~~~~~~~~~~~~~

To install using `pip`::

	pip install -e git+https://github.com/mwicat/batchui.git#egg=batchui

Ensure you have PyQt4 installed on your system, for Debian::

	sudo apt-get install python-qt4

Getting started
---------------

`BatchUI` is basically a GUI generator for generic applications that do
bulk operations on files.

The simplest example of such application is 
`AutoBackup <https://github.com/mwicat/batchui/blob/master/samples/autobackup.py>`_.
The bulk operation done by this application is just to backup every file, that is
copy the old file to the new file with `.bak` suffix.

You can look at its code and see that it only defines two functions for `BatchUI`:
`parse_file` and `process_item`. `parse_file` tells the framework how the file
should be displayed in the file list and `process_item` tells it what it should
do with parsed file when the `Process` button is hit by the user.

`parse_file` returns a dictionary with items that can be later queried by
`process_item`. If you define an item with the key `has_backup`, you can later reference
it as `item.data['has_backup']`. If you want to show this information in file
list, you can add a pair of `('has_backup', 'Has backup')` to the `columns` list
that you also pass to `BatchUI`.

To see further possibilities that `BatchUI` gives you, check out the
`AutoRootNote <https://github.com/mwicat/autorootnote>`_ application.
