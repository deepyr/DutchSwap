import subprocess

# run  `python scripts/flatten.py`

CONTRACT_DIR = "contracts/"

def flatten(mainsol, outputsol):
    pipe = subprocess.call("scripts/solidityFlattener.pl --contractsdir={} --mainsol={} --outputsol={} --verbose"
                           .format(CONTRACT_DIR, mainsol, outputsol), shell=True)
    print(pipe)

def flatten_contracts():
    flatten("DutchSwapFactory.sol", "flattened/DutchSwapFactory_flattened.sol")
    flatten("DutchSwapAuction.sol", "flattened/DutchSwapAuction_flattened.sol")
    flatten("BokkyPooBahsFixedSupplyTokenFactory.sol", "flattened/BokkyPooBahsFixedSupplyTokenFactory.sol")


flatten_contracts()