# DutchSwap

Digital Dutch Auctions 

## Dutch Auctions Are Fair.


Ever wanted to raise some money for your project? Or.. have you ever tried to sell a 100 limited edition collectables, but didn't know what to charge? Did you pay top Dai for your UNISOCKS?

Dutch auctions are awesome. Gnosis used them to raise money, so did Google, the Fed Treasury, and the Dutch for hundreds of years to sell billions of dollars of flowers. Why not more of us in the Ethereum Community?

A dutch auction starts with a batch of tokens (say 100 FLOWERS) and I have to sell all of the flowers at the end of the week. I start with a high price, 10 dai per tulip, and drop the price bit by bit. I sell a few flowers at 7 dai, 5, 4, most at 3 and sell out at 2.5 dai. Now the cool part is.. Everyone pays 2.5 DAI!!

It is a fair way to make sure everyone who really wanted them, got them, and everyone else is happy with the price. 




## Setup

Install needed Python modules: `python -m pip install -r requirements.txt`

## Compiling the contracts

Compile updated contracts: `brownie compile`

Compile all contracts (even not changed ones): `brownie compile --all`

## Running tests

Run tests: `brownie test`

Run tests in verbose mode: `brownie test -v`

Check code coverage: `brownie test --coverage`

Check available fixtures: `brownie --fixtures .`


## Brownie commands

Run script: `brownie run <script_path>`

Run console (very useful for debugging): `brownie console`

## Deploying DutchSwap Contracts 

Run script: `brownie run scripts/deploy_DutchSwapAuction.py`


## Testing with Docker

A Dockerfile is available if you are experiencing issues testing locally.

run with:
`docker build -f Dockerfile -t brownie .`
`docker run -v $PWD:/usr/src brownie pytest tests`