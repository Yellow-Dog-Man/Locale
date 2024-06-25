#!/usr/bin/env python3

import json


class LocaleCleaner:
    def __init__(self, en: str, lang: str, out: str, add_missing_keys: bool = False):
        with open(en, "r", encoding="utf8") as en_file:
            self.en: list = en_file.readlines()
        with open(lang, "r", encoding="utf8") as lang_file:
            self.lang: dict = json.load(lang_file)
        self.out: str = out
        self.output: list = []
        self.add_missing_keys: bool = add_missing_keys

    def run(self):
        self.make_header()
        self.parse()
        self.make_footer()
        self.save()

    def make_header(self):
        self.output.append("{")
        self.output.append('    "localeCode": "{}",'.format(self.lang["localeCode"]))
        self.output.append(
            '    "authors": ["{}"],'.format('", "'.join(self.lang["authors"]))
        )
        self.output.append('    "messages": {')

    def make_footer(self):
        self.output.append('        "Dummy": "Dummy"')
        self.output.append("    }")
        self.output.append("}")
        self.output.append("")

    def find_start(self):
        counter = 0
        for line in self.en:
            counter += 1
            if "message" in line:
                break
        return counter

    def parse(self):
        start_pos = self.find_start()
        blank = False
        for line in self.en[start_pos:]:
            if '"Dummy": "Dummy"' in line:
                break
            kv = line.strip().split(":", 1)
            key = kv[0].strip().replace('"', "")
            if key in self.lang["messages"]:
                blank = False
                translation = (
                    self.lang["messages"][key].replace("\n", "\\n").replace('"', '\\"')
                )
                self.output.append('        "{}": "{}",'.format(key, translation))
            elif self.add_missing_keys and key != "":
                blank = False
                value = kv[1].strip().rstrip(",")[1:-1]
                self.output.append('        "#{}": "{}",'.format(key, value))
            elif blank == False:
                self.output.append("")
                blank = True

    def save(self):
        with open(self.out, "w", encoding="utf8") as out:
            out.write("\n".join(self.output))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="This script will reformat a Babel style JSON for locales to match the en.json baseline formatting for git changes purposes."
    )
    parser.add_argument(
        "--en", metavar="en_path", type=str, help="The path to the en.json locale."
    )
    parser.add_argument(
        "--lang",
        metavar="lang_path",
        type=str,
        help="The path to the LANG.json locale to clean.",
    )
    parser.add_argument(
        "--out",
        metavar="out_path",
        type=str,
        help="The path to save the formatted file.",
    )
    parser.add_argument(
        "-a",
        "--add-missing-keys",
        action="store_true",
        help="If a key is missing in the translation, copy original text from en.json to the output file.  The key will be prefixed with #.",
    )

    args = parser.parse_args()
    if args.lang is None or args.en is None or args.out is None:
        parser.print_help()
        exit(1)
    N = LocaleCleaner(args.en, args.lang, args.out, args.add_missing_keys)
    N.run()
    print("Cleaned!")
