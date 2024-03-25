def jaNeeBlacklistInput(question):
    '''Function that returns a value based on the user input 
    that follows a question prompt.'''

    ## Let user choose input only 'j', 'n' or 'blacklist'
    while "the answer is invalid":
        reply = str(input(question+' (j/n/blacklist): ')).lower().strip()
        if reply[0] == 'j':
            return 'j'
        elif reply == 'blacklist':
            return 'b'
        elif reply[0] == 'n':
            return 'n'
        else:
            print('Onjuiste input antwoord moet j/n/blacklist zijn!')

def expand_dicts(avg_words_df, whitelist_df, blacklist_df):
    '''Function that lets the user annotate words to a whitelist, skip
     or to a blacklist; based on user input. '''
    import pandas as pd
    # Let user check words and add to whitelist or blacklist based on user input 
    for i in avg_words_df.head(15).index:
        avg_woord = avg_words_df['AVG_woord'][i]
        #Get user input and transform to dataframe
        user_input = jaNeeBlacklistInput(f"{avg_woord} kwam {avg_words_df['Count'][i]} keer voor in de open antwoorden.\nWil je dit woord toevoegenaan de whitelist? ")
        antwoord_df = pd.DataFrame({'words': [avg_woord]})
        
        if user_input == 'j':
            #If answer is yes add to whitelist
            whitelist_df = pd.concat([whitelist_df, antwoord_df], axis=0)
            print(f'Woord "{avg_woord}" is toegevoegd aan de whitelist')
        elif user_input == 'blacklist':
            #If answer is blacklist: add to blacklist
            blacklist_df = pd.concat([blacklist_df, antwoord_df], axis=0)
            print(f'Woord "{avg_woord}" is toegevoegd aan de blacklist')
        else:
            print(f'Woord "{avg_woord}" is overgeslagen')
        
    return whitelist_df, blacklist_df