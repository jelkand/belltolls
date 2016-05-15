import config.characters as config
import csv
import numpy as np
import pandas as pd
import re

SEARCH_LENGTH = 500    

def build_character_dict(character_name):
    characters = list(config.names)
    characters.remove(character_name)
    character_dict = dict()
    for character in characters:
        character_dict[character] = 0;

    return character_dict


def build_chapter_matrix(chapter_number):
    character_references = dict()

    file = open('./text/chapter%s' % chapter_number, 'r')
    chapter = file.read().lower()

    for character in config.names:
        print('checking for %s' % character)
        character_dict = build_character_dict(character)
        prev = 0
        for m in re.finditer(character, chapter):
            next_ = chapter[m.end():].find(character)
            start_index = max(prev, m.start() - SEARCH_LENGTH)
            end_index = min(next_, m.end() + SEARCH_LENGTH)
            find_nearby_mention(character, character_dict, chapter[start_index:end_index])
            prev = m.end()
        character_dict[character] = 0
        character_references[character] = character_dict

    reference_df = pd.DataFrame.from_dict(character_references)
    reference_df.to_csv('./networks/adj_matrices/chapter%s.csv' % chapter_number)
    return reference_df


def find_nearby_mention(character_name, character_dict, text):
    for key in character_dict:
        count = text.count(key)
        if count > 0:
            print('%s found in conjunction with %s' % (character_name, key))
        character_dict[key] = count
    return character_dict


if __name__ == '__main__':
    master_df = None
    for x in range(1, 44):
        print('Checking chapter %s' % x)
        df = build_chapter_matrix(x)
        if master_df is None:
            master_df = df
        else:
            master_df = master_df.add(df)
    master_df.to_csv('./networks/master_adj_matrix.csv')