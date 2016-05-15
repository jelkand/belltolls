import config.characters as config
import numpy as np
import pandas as pd

SEARCH_WORDS = 200   


def build_chapter_matrix(chapter_number):
    print('Searching chapter %s' % str(chapter_number))
    characters = list(config.names)
    chapter_df = pd.DataFrame(0, index=characters, columns=characters, dtype=int)

    file = open('./text/chapter%s' % chapter_number, 'r')
    chapter = file.read().lower()

    chapter_words = chapter.split()

    for chunk in range(0, (len(chapter_words) // SEARCH_WORDS)+1):
        find_characters_in_chunk(chapter_words[chunk*SEARCH_WORDS:(chunk+1)*SEARCH_WORDS], chapter_df)
        print('Searched section number %s, %s thru %s out of %s total words' % (str(chunk), chunk*SEARCH_WORDS,
              (chunk+1)*SEARCH_WORDS, len(chapter_words) ))

    chapter_df.to_csv('./networks/adj_matrices/chapter%s.csv' % chapter_number)
    return chapter_df

def find_characters_in_chunk(chunk, adj_matrix):
    characters = list(config.names)
    found_characters = list()
    for character in characters:
        if character in chunk:
            found_characters.append(character)
    
    for first_character in found_characters:
        for second_character in found_characters:
            if first_character != second_character:
                adj_matrix.ix[first_character, second_character] += 1



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