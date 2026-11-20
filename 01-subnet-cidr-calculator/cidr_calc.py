#!/usr/bin/env python3
"""CLI IPv4 Subnet & CIDR Calculator."""

import argparse
import ipaddress
import sys


def inspect_network(cidr: str, num_subnets: int | None = None) -> None:
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    total_addrs = net.num_addresses
    hosts = list(net.hosts())
    usable_count = len(hosts)
    first_host = str(hosts[0]) if usable_count > 0 else "N/A"
    last_host = str(hosts[-1]) if usable_count > 0 else "N/A"

    print(f"Network:          {net.with_prefixlen}")
    print(f"Network Address:  {net.network_address}")
    print(f"Broadcast Addr:   {net.broadcast_address}")
    print(f"Subnet Mask:      {net.netmask}")
    print(f"Wildcard Mask:    {net.hostmask}")
    print(f"Total Addresses:  {total_addrs}")
    print(f"Usable Hosts:     {usable_count}")
    print(f"Usable Range:     {first_host} - {last_host}")

    if num_subnets is not None:
        if num_subnets < 2 or (num_subnets & (num_subnets - 1)) != 0:
            print("Note: --subnets works best with powers of 2 (2, 4, 8, 16...).", file=sys.stderr)
        new_prefix_bits = (num_subnets - 1).bit_length()
        target_prefix = net.prefixlen + new_prefix_bits
        if target_prefix > net.max_prefixlen:
            print(f"Error: Cannot split /{net.prefixlen} into {num_subnets} subnets.", file=sys.stderr)
            sys.exit(1)
        print(f"\nSubnets (/{target_prefix}):")
        for idx, sub in enumerate(net.subnets(new_prefix=target_prefix), start=1):
            print(f"  {idx}. {sub.with_prefixlen} (hosts: {sub.num_addresses - 2 if sub.num_addresses > 2 else 0})")


def main() -> None:
    parser = argparse.ArgumentParser(description="IPv4 Subnet and CIDR Calculator")
    parser.add_argument("cidr", help="Target CIDR block, e.g. 192.168.1.0/24")
    parser.add_argument("--subnets", type=int, default=None, help="Split into N subnets")
    args = parser.parse_args()
    inspect_network(args.cidr, args.subnets)


if __name__ == "__main__":
    main()
