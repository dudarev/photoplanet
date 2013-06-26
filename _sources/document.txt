How to document
===================

If you have set up a directory with generated HTML based on the gist below,
you may do the following from the ``/docs`` directory to publish to Gihub pages::

    make html
    cd build/html  # or your build directory depending on config
    git commit -a -m 'made some changes, yo'
    git push origin gh-pages

The full gist to setup the publishing of HTML pages generated with Sphinx to Github pages 
(originally by `@brantfaircloth <https://github.com/brantfaircloth>`__):

.. gist:: https://gist.github.com/dudarev/5871867
