#!/usr/bin/env python3

import json

class LocaleCleaner:
    def __init__(self, en, lang, out):
        en_file = open(en, 'r', encoding="utf8")
        lang_file = open(lang, 'r', encoding="utf8")
        self.out = out
        self.en = en_file.readlines()
        self.lang = json.load(lang_file)
        self.output = []
        
    def run(self):
        self.make_header()
        self.parse()
        self.make_footer()
        self.save()
    
    def make_header(self):
        self.output.append('{')
        self.output.append('    "localeCode": "{}",'.format(self.lang["localeCode"]))
        self.output.append('    "authors": ["{}"],'.format('", "'.join(self.lang["authors"])))
        self.output.append('    "messages": {')
        
    def make_footer(self):
        self.output.append('        "Dummy": "Dummy"')
        self.output.append('    }')
        self.output.append('}')
        self.output.append('')

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
            key = line.strip().split(':')[0].strip().replace('"','')
            if key in self.lang["messages"]:
                blank = False
                translation = self.lang["messages"][key].replace('\n','\\n').replace('"','\\"')
                self.output.append('        "{}": "{}",'.format(key, translation))
            elif blank == False:
                self.output.append('')
                blank = True
    
    def save(self):
        out = open(self.out, 'w', encoding="utf8")
        out.write('\n'.join(self.output))
        out.close()
        
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='This script will reformat a Babel style JSON for locales to match the en.json baseline formatting for git changes purposes.')
    parser.add_argument('--en', metavar='en_path', type=str, 
                        help='The path to the en.json locale.')
    parser.add_argument('--lang', metavar='lang_path', type=str, 
                        help='The path to the LANG.json locale to clean.')
    parser.add_argument('--out', metavar='out_path', type=str, 
                        help='The path to save the formatted file.')

    args = parser.parse_args()
    N = LocaleCleaner(args.en, args.lang, args.out)
    N.run()
    print("Cleaned!")

