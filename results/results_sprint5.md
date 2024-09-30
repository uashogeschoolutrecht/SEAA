# Pilot SEAA - Sprint 5 (29 Aug - 11 Sep 2024)

## Work done

**Annotation**. All manual annotations are done: 2239 in total. Annotations include a random draw from all questions, and all answers from the question regarding study limitations and illness. 
**Add output**. Each respondent was given a technical id (e.g. a number), and this technical id was provided in SEAA's output file among all other derived columns. 

## Results

SEAA was run on the 2239 annotated cases:  efficiency = 79.4%, accuracy = 94%.

## Discussion

Out of 2239 cases there were 11 cases where SEAA did not flag the answer even though it was annotated as containing privacy-related data. Examining these false negative cases in more depth showed that 10 out of 11 answers where falsely annotated as containing privacy-related data. One false negative case contained a reference to a car-accident ('auto-ongeluk'). 

Efficiency can be easily further increased by excluding non-Dutch answers (which will always be flagged by SEAA) and adding more Dutch words to the whitelist dictionary. 

In conclusion, SEAA reached a very high accuracy of 99% while flagging answers from the National Student Questionaire (NSE) 2023, with a decent effeciency rate of 79%. 
