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



The main documentation for the site is organized into the following sections:


.. toctree::
    :caption: Getting Started
    :maxdepth: 1
   
    getting_started/quickstart.rst
    getting_started/overview/index
    getting_started/step_by_step/index


.. toctree::
    :caption: Tokens
    :maxdepth: 1
    :name: sec-tokens

    tokens/base_token.rst
    tokens/custom_token


.. toctree::
    :caption: Auctions
    :maxdepth: 1
    :name: sec-auctions
    
    auctions/dutch_auction.rst


.. toctree::
    :caption: Community
    :maxdepth: 1
    :name: sec-community

   community/contributing/index
   community/channels


.. toctree::
   :maxdepth: 1
   :caption: Development
   :name: sec-devel

   development/smart_contracts/index

