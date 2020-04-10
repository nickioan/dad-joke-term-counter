
import pandas as pd
import re
from djranker.contractions import CONTRACTION_MAP

class WordCount:
    def __init__(self):
        self.jokes_number = 10
        self.word_tracker = {}
        column_names = ["Rank", "Term", "Count"]
        self.df = pd.DataFrame(columns=column_names)

    #Splits joke string into list of words and stores occurrence in a Hash Map
    def add_joke(self,joke):
        upper_words = ["I"]
        filtered_joke = self.__filter_joke(joke)

        #This function returns a list of terms in lower case but "I" from a string
        get_words = lambda x: list(a if a in upper_words else a.lower() 
                    for a in x.split())

        words= get_words(filtered_joke)
        for word in words:
            if word in self.word_tracker:
                self.word_tracker[word] += 1
            else:
                self.word_tracker[word] = 1
    
    #Updates Dataframe rows based on newly parsed jokes
    def update_ranks(self):
        rank = list(range(1,11))
        words = sorted(self.word_tracker,key=self.word_tracker.__getitem__, reverse=True)
        frequency = [self.word_tracker[x] for x in words[:10]]
        self.df["Rank"] = rank
        self.df["Term"] = words[:10]
        self.df["Count"] = frequency


    
    #Removes all special characters and digits
    def __filter_joke(self,joke):

        filtered_joke = joke.replace("’","'")
        filtered_joke = self.__expand_contractions(filtered_joke)

        #Regular expression is used to remove special characters and digits
        pattern = r'[^a-zA-z\s]'
        filtered_joke = re.sub(pattern, '', filtered_joke)

        return filtered_joke

    #Returns input sentence without contracted words
    def __expand_contractions(self, joke, contraction_mapping=CONTRACTION_MAP):
        contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                        flags=re.IGNORECASE|re.DOTALL)
        def expand_match(contraction):
            match = contraction.group(0)
            first_char = match[0]
            expanded_contraction = contraction_mapping.get(match)\
                                    if contraction_mapping.get(match)\
                                    else contraction_mapping.get(match.lower())                       
            expanded_contraction = first_char+expanded_contraction[1:]
            return expanded_contraction
            
        expanded_joke = contractions_pattern.sub(expand_match, joke)
        expanded_joke = re.sub("'", "", expanded_joke)
        return expanded_joke
