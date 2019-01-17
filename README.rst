howpopular
====================================================

command line popularity checker
-------------------------------------------

This software is inspired by `howdoi <https://github.com/gleitz/howdoi>`.

When you wonder how popular somthing you are interested in is, type as follows

::

    $ howpopular foo

then, howpopular will answer like this.

::

    $ howpopular foo
    foo 133000000 hits

When you want to know which is the most popular among some things, type them as follows:

::

    $ howpopular foo bar baz
    foo 133000000 hits
    bar 6810000000 hits
    baz 51200000 hits

You can also specify histgram mode.

::

    $ howpopular -H foo bar baz
    foo  133000000 hits: *
    bar 6810000000 hits: ****************************************************************************************************
    baz   51200000 hits: 


Installation
------------

::

    python setup.py install

Usage
-----

::

    usage: howpopular [-h] [-C] [-v] [-H] [QUERY [QUERY ...]]

    command line popularity checker

    positional arguments:
      QUERY              things of which you want to know popularity

    optional arguments:
      -h, --help         show this help message and exit
      -C, --clear-cache  clear the cache
      -v, --version      displays the current version of howpopular
      -H, --histgram     display the histgram of popularity

Author
------

- todok-r


Notes
-----

-  Howpopular uses a cache for faster access to previous questions. Caching functionality can be disabled by setting the HOWPOPULAR_DISABLE_CACHE environment variable. The cache is stored in `~/.cache/howpopular`.
-  Special thanks to Benjamin Gleitzman (`@gleitz <https://github.com/gleitz>`_) for the idea.
