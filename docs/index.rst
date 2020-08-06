DutchSwap
=======

DutchSwap is a token framework for revenue generating ventures

!! Documentation is currently under construction !!


.. note::

    This project relies upon some knowledge about ``Solidity`` and the documentation assumes a basic familiarity with it. You may wish to view the `Solidity docs <https://solidity.readthedocs.io/en/stable/index.html>`_ if you have not used it previously.

Features
========

* Hybrid token structure - distinct asset classes combined with fungible tokens
* Token converters for converting between different classes
* Customisable rule engine for token transfers 
* Different token types - Dividend tokens, vested tokens, options etc
* Contract testing via `pytest <https://github.com/pytest-dev/pytest>`_, including trace-based coverage evaluation
* Property-based and stateful testing via `hypothesis <https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python>`_



.. toctree::
    :maxdepth: 2

    Overview <index.rst>
    .. quickstart.rst
    .. demo.rst

.. toctree::
    :caption: Getting Started
    :maxdepth: 2

    dutch_swap.rst

.. toctree::
    :caption: Core Functionality
    :maxdepth: 2

    tokens.rst


.. toctree::
    :caption: Tokens
    :maxdepth: 2

    base_token.rst
    custom_token.rst


.. toctree::
    :caption: Auctions
    :maxdepth: 2

    dutch_auction.rst


.. .. toctree::
..     :caption: Testing
..     :maxdepth: 2

..     run_tests.rst
..     new_test.rst

.. toctree::
    :caption: Reference
    :maxdepth: 2

    links.rst


