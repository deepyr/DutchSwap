DutchSwap
=======

DutchSwap is a smart contract factory for Dutch auctions on Ethereum

!! Documentation is currently under construction !!


.. note::

    Parts of this documentation reference smart contracts written in ``Solidity`` and the documentation assumes a basic familiarity with it. You may wish to view the `Solidity docs <https://solidity.readthedocs.io/en/stable/index.html>`_ if you have not used it previously.

Features
========

* Dutch Auction for ERC20 tokens
* Payments in Ethers or an ERC20 of your choosing
* Contract testing via `pytest <https://github.com/pytest-dev/pytest>`_, including trace-based coverage evaluation
* Property-based and stateful testing via `hypothesis <https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python>`_



The main documentation for the site is organized into the following sections:


.. toctree::
    :caption: Getting Started
    :maxdepth: 1
   
    quickstart/index
    getting_started/step_by_step/index


.. toctree::
    :caption: Auctions
    :maxdepth: 1
    :name: sec-auctions
    
    auctions/dutch_auction
    auctions/auction_process


.. toctree::
    :caption: Tokens
    :maxdepth: 1
    :name: sec-tokens

    tokens/token_types
    tokens/creating_tokens


.. toctree::
    :caption: Community
    :maxdepth: 1
    :name: sec-community

    community/contributing
    community/channels


.. toctree::
    :caption: Protocol
    :maxdepth: 1
    :name: sec-devel

    protocol/smart_contracts/index

