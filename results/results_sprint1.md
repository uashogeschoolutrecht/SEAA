# Pilot SEAA - Sprint 1 (23 Nov - 6 Dec)

Pilot was started on November 23rd 2023 with the following dev team:

- Anne Leemans (Lead developer)
- Fraukje Coopmans (Project Manager, developer)
- Pim Lamberts (junior developer)

## Results

A first version of the semi-automated anonimisation algorithm (SEAA) was developed. Validation on a 'fake validation dataset' was run to test efficiency and accuracy of the algorithm.
Efficiency = 73.5%, accuracy = 64.5%

## Discussion

1. Choice of dictionary. The dictionary (Opentaal) that we have tried so far has a large number of words (~400k), however, there are names of persons included. This will cause a lower accuracy of the SEAA algorithm, since sentences like 'Teacher Anne is horrible' will be classified as containing no privacy-related content. A libary without any privacy-related words is needed.
2. Quality of valdiation data. The provided validation data does not contain a classification, i.e.: whether the provided string contains privacy-related data yes/no. Also, it is not yet clear when data is considered to containt privacy-related data. Input from the privacy officer is needed to help improve the quality of the validation data and define a strict definition of privacy-containing data.
3. Language. For now we are focusing on Dutch language, but it is unknown yet what proportion of data is written in any other language. An analysis of the proportion Dutch/non-Dutch data is needed to determine whether we can neglect non-Dutch answers.
