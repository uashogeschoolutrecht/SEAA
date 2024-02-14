# Pilot SEAA - Sprint 4 (1 Feb - 14 Feb)

## Work done

**Annotation**. All manual annotations are done: 300 in total.

**Illness dictionary**. A list of illness words (such as 'ADHD', 'ALS', etc) was gathered from Wikipedia and implemented in SEAA as a blacklist: if an answer contains a word on this list it will always be flagged by SEAA.

**Analysis on common unknown words**. Some words are not part of our standard OpenTaal dictionary, but do appear quite often in the answers. We made an overview of all words that are not matched within the Dutch language dictionary (the 'unknown words') and listed them in order of how often they occur.

**Whitelist**. Based on above analysis, a small number of common unknown words were added to the whitelist. These words are:
nederlands
powerpoint
ipv
leerteam
powerpoints
nvt
slides
nederlandse
bijv

## Results

SEAA was run on the 300 annotated cases:  accuracy = 100%.
SEAA was run on the full batch of answers: efficiency = 76.0%.

## Discussion

Accuracy of SEAA is very good: with the implementation of the illness dictionary we are now confident SEAA can succesfully distinguish between answers that contain no privacy-related data and answers that might contain some form of privacy-related data.

Efficiency is lower than expected (80% or higher). A proportion of answers seems to be written in English (~5 - 20%) which currently all will be flagged as 'might contain privacy-related data' and contribute strongly to a lower efficiency as false positives. By excluding English answers the true efficiency can be calculated.

The illness dictionary contained one word that is also a common Dutch word: 'als'. To evade a high number of false positives we opted to exclude the illness smallcaps writing 'als' and only inlude the truecaps writing 'ALS'.

There is one type of privacy-related content SEAA currently cannot detect. For instance the sentence 'docent groen is stom' will be not be flagged by SEAA since all words are part of the Dutch language dictionary. To correct for this, we want to implement smart rules to identify these types of privacy-related language.
