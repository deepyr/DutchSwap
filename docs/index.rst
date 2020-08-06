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
    :maxdepth: 1

    Overview <index.rst>
    .. quickstart.rst
    .. demo.rst

.. toctree::
    :caption: Getting Started
    :maxdepth: 1
   
    getting_started/step_by_step/index
    getting_started/dutch_swap/index
    getting_started/tokens/index

   ..  dutch_swap.rst
   ..  tokens.rst


.. toctree::
    :caption: Tokens
    :maxdepth: 1

    tokens/base_token/index
    tokens/custom_token/index


.. toctree::
    :caption: Auctions
    :maxdepth: 1

    auctions/dutch_auction/index


.. toctree::
   :maxdepth: 1
   :caption: Development
   :name: sec-devel

   development/smart_contracts/index


.. toctree::
    :caption: Community
    :maxdepth: 1

   community/contributing/index
   community/channels


