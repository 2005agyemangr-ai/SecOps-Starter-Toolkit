# Subnet & CIDR Calculator

A lightweight command-line IPv4 subnetting and CIDR calculator written in Python using the standard library `ipaddress` module.

## Features
- Parse CIDR notation (e.g., `192.168.10.0/24`)
- Display network address, broadcast address, subnet mask, wildcard mask, total addresses, and usable host range
- Split a network into equal subnets

## Usage
```bash
python3 cidr_calc.py 192.168.1.0/26
python3 cidr_calc.py 10.0.0.0/22 --subnets 4
```
