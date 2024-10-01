# /// script
# dependencies = [
#   "emlx",
# ]
# ///
import argparse
import email
import logging
import os

import emlx


def extract_addresses(emlx_folder_path):
    """
    Recursively extracts "From" email addresses from all .emlx files in the given folder and nested folders.
    :param emlx_folder_path: Path to the root folder containing .emlx files
    """
    # Will be like:
    # {
    #   "bob@example.org": {"count": 2, "names": ["Bob Ferris", "Robert Ferris"], },
    # }
    addresses = {}
    domains = {}

    for root, dirs, files in os.walk(emlx_folder_path):
        for file in files:
            if file.endswith(".emlx"):
                emlx_file_path = os.path.join(root, file)
                logging.debug(f"Processing {emlx_file_path}")
                msg = emlx.read(emlx_file_path)
                if "From" in msg:
                    flags = msg.plist["flags"]

                    # A message might still be present in this mailbox on disk
                    # but actuall be "deleted". In which case we ignore it.
                    if "deleted" not in flags or flags["deleted"] is False:
                        name, address = email.utils.parseaddr(msg["From"])
                        if address:
                            if address in addresses:
                                addresses[address]["count"] += 1
                            else:
                                addresses[address] = {"count": 1, "names": []}

                            if name not in addresses[address]["names"]:
                                addresses[address]["names"].append(name)

                        domain = address.split("@")[-1]
                        if domain != "" and domain in domains:
                            domains[domain]["count"] += 1
                        else:
                            domains[domain] = {"count": 1}

    return addresses, domains


def print_results(results):
    """
    Outputs a table of data.

    results should be a dict with each key/val like:
      {
       "bob@example.org": {"count": 2, "names": ["Bob Ferris", "Robert Ferris"], },
      }
    The "names" item is optional.

    threshold is an integer. Only items with a "count" of threshold or
    above will be output
    """
    sorted_results = {
        k: v
        for k, v in sorted(
            results.items(), key=lambda item: item[1]["count"], reverse=True
        )
    }

    # Put data into rows, each with several columns
    rows = []
    for address, data in sorted_results.items():
        col3 = data["names"] if "names" in data else []
        rows.append([str(data["count"]), address, ", ".join(sorted(col3))])

    # Calculate how wide each column needs to be:
    widths = [max(map(len, col)) for col in zip(*rows)]

    for row in rows:
        print("  ".join((val.ljust(width) for val, width in zip(row, widths))))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Extract "From" addresses from emails in a folder of .emlx files.'
    )
    parser.add_argument(
        "path", type=str, help="Path to the folder containing .emlx files"
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=2,
        help="Only show addresses that appear at least this many times",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    addresses, domains = extract_addresses(args.path)
    addresses = {k: v for k, v in addresses.items() if v["count"] >= args.threshold}
    domains = {k: v for k, v in domains.items() if v["count"] >= args.threshold}

    print("\nEmail addresses:")
    if len(addresses) == 0:
        print("None")
    else:
        print_results(addresses)

    print("\nDomains:")
    if len(domains) == 0:
        print("None")
    else:
        print_results(domains)
