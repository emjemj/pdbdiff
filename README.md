# pdbdiff
A simple tool for comparing two networks' PeeringDB entries

## Usage
Pdbdiff can display unique or common exchange and facility presences for two networks. By default, the unique data is displayed, use `-c` or `--common` to display common data. You can switch to only displaying exchange or facility data with `-i` and `-f`  respectively. Use `-1` or `-2` to only display data for the first or second asn.

```
usage: Compare two peeringdb entries [-h] [--common] [--ix] [--facility]
                                     [--first] [--second]
                                     ASN ASN
```
