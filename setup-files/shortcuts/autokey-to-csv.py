import os, json

# converts the .txt & .json file representation of text-expansion shortcuts (as used by autokey) into a yaml file (for espanso)

text_expansions = {}  # key: abbreviation, value: expansion

# find all autokey scripts
autokey_script_dir = r"./Notion/"

# go over each text file in the director
for file in os.listdir(autokey_script_dir):
    if not file.endswith(".json"):
        continue

    with open(autokey_script_dir + "/" + file, "r") as f:

        data = json.load(f)
        abbreviation = data["abbreviation"]["abbreviations"][0]
        text_expansions[abbreviation] = None

        # there should be a .txt file with the same name containing the expansion
        expansion_file = file.replace(".json", ".txt")[1:]  # remove leading dot
        try:
            with open(autokey_script_dir + "/" + expansion_file, "r") as f:
                text_expansions[abbreviation] = f.read()
        except:
            print("No expansion found for", abbreviation)


csv_file = r"./notion_shortcuts.csv"

with open(csv_file, "w") as f:
    for abbreviation, expansion in text_expansions.items():
        if expansion is None:
            continue
        if "\n" in expansion:
            # add p tags to denote lines (needed for chrome ext)
            lines = expansion.split("\n")
            lines = ["<p>" + line + "</p>" for line in lines]
            expansion = "".join(lines)
        expansion_text = f'{abbreviation}, {expansion}\n'
        f.write(expansion_text)
        # print(expansion_text)
