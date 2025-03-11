import os, json

# converts the .txt & .json file representation of text-expansion shortcuts (as used by autokey) into a yaml file (for espanso)

text_expansions = {}  # key: abbreviation, value: expansion

# find all autokey scripts
autokey_script_dir = r"/home/saulivor/Desktop/Personalisation/Shortcuts/Notion"

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


espanso_config_file = r"/home/saulivor/.config/espanso/match/notion.yml"

with open(espanso_config_file, "w") as f:
    f.write("matches:\n")
    for abbreviation, expansion in text_expansions.items():
        if expansion is None:
            continue

        expansion_text = f"\n  - trigger: '{abbreviation}'\n"
        if "\n" in expansion:
            initial_whitespace = " " * 13  # 7 indents
            expansion = expansion.replace("\n", "\n" + 14 * " ")  # indent lines
            expansion_text += f"    replace: |\n{initial_whitespace}{expansion}\n"
        else:
            expansion_text += f"    replace: '{expansion}'\n"
        f.write(expansion_text)
        # print(expansion_text)
