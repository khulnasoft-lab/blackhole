#!/usr/bin/env python3

# Enhanced Script by KhulnaSoft
# https://github.com/KhulnaSoft
#
# This Python script updates the readme files in this repo with improved
# readability, modularization, logging, and error handling.

import json
import os
import time
import logging
from string import Template

# ===== Project Settings =====
BASEDIR_PATH = os.path.dirname(os.path.realpath(__file__))
README_TEMPLATE = os.path.join(BASEDIR_PATH, "readme_template.md")
README_FILENAME = "readme.md"
README_DATA_FILENAME = "readmeData.json"

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8", newline="\n") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file '{path}': {e}")
        raise


def sort_keys(data):
    keys = list(data.keys())
    keys.sort(
        key=lambda item: (
            item.replace("-only", "").count("-"),
            item.replace("-only", ""),
        )
    )
    logging.debug(f"Sorted keys: {keys}")
    return keys


def format_toc_rows(data, keys):
    toc_template = Template(
        "${description} | [Readme](https://github.com/KhulnaSoft/"
        "blackhole/blob/master/${location}readme.md) | "
        "[link](https://raw.githubusercontent.com/KhulnaSoft/"
        "blackhole/master/${location}blackhole) | "
        "${fmtentries} | "
        "[link](http://sbc.io/blackhole/${location}blackhole)"
    )
    toc_rows = []
    for key in keys:
        entry = data[key]
        entry["fmtentries"] = "{:,}".format(entry["entries"])
        if key == "base":
            entry["description"] = "Unified blackhole = **(adware + malware)**"
        elif entry.get("no_unified_blackhole", False):
            entry["description"] = (
                "**" + key.replace("-only", "").replace("-", " + ") + "**"
            )
        else:
            entry["description"] = (
                "Unified blackhole **+ " + key.replace("-", " + ") + "**"
            )
        entry["location"] = entry["location"].replace("\\", "/")
        toc_rows.append(toc_template.substitute(entry))
    return "\n".join(toc_rows) + "\n"


def format_source_rows(source_list):
    row_defaults = {
        "name": "",
        "homeurl": "",
        "url": "",
        "license": "",
        "issues": "",
        "description": "",
    }
    source_template = Template(
        "${name} |[link](${homeurl})"
        " | [raw](${url}) | ${license} | [issues](${issues})| ${description}"
    )
    rows = []
    for source in source_list:
        this_row = row_defaults.copy()
        this_row |= source
        rows.append(source_template.substitute(this_row))
    return "\n".join(rows) + "\n"


def update_readme(key, entry, toc_rows):
    extensions = key.replace("-only", "").replace("-", ", ")
    extensions_str = f"* Extensions: **{extensions}**."
    if entry.get("no_unified_blackhole", False):
        extensions_header = f"Limited to the extensions: {extensions}"
    else:
        extensions_header = f"Unified blackhole file with {extensions} extensions"

    size_history_graph = (
        "![Size history](https://raw.githubusercontent.com/KhulnaSoft/blackhole/master/blackhole_file_size_history.png)"
        if key == "base"
        else "![Size history](stats.png)"
    )

    source_rows = format_source_rows(entry["sourcesdata"])

    target_readme = os.path.join(entry["location"], README_FILENAME)
    os.makedirs(entry["location"], exist_ok=True)

    try:
        with open(README_TEMPLATE, encoding="utf-8", newline="\n") as template_file, \
             open(target_readme, "wt", encoding="utf-8", newline="\n") as out_file:
            for line in template_file:
                line = line.replace("@GEN_DATE@", time.strftime("%B %d %Y", time.gmtime()))
                line = line.replace("@EXTENSIONS@", extensions_str)
                line = line.replace("@EXTENSIONS_HEADER@", extensions_header)
                line = line.replace("@NUM_ENTRIES@", "{:,}".format(entry["entries"]))
                line = line.replace("@SUBFOLDER@", os.path.join(entry["location"], ""))
                line = line.replace("@TOCROWS@", toc_rows)
                line = line.replace("@SOURCEROWS@", source_rows)
                line = line.replace("@SIZEHISTORY@", size_history_graph)
                out_file.write(line)
        logging.info(f"Updated {target_readme}")
    except Exception as e:
        logging.error(f"Failed to update {target_readme}: {e}")


def main():
    logging.info("Starting readme update process...")
    data = load_json(README_DATA_FILENAME)
    keys = sort_keys(data)
    toc_rows = format_toc_rows(data, keys)

    for key in keys:
        update_readme(key, data[key], toc_rows)

    logging.info("All readmes updated successfully.")


if __name__ == "__main__":
    main()
