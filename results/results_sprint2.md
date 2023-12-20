# Pilot SEAA - Sprint 2 (7 Dec - 21 Dec)

**Dictionary**. In the second week we changed the data cleaning step such that the dictionary words are no longer changed to all smallcase. This means that all person names in answers will be classified as containing privacy information that could be traced back to the individual.

**Validation data definition**. In a meeting with different stakeholders (product owner, privacy officer, development team) we determined a first version of 'privacy definitions'. These are a set of rules that determine when the SEAA algorithm should or should not classify an answer as possibly containing privacy data.

**Accuracy definition change**. For SEAA it is of vital importance that all cases containing any type of privacy related information are classified as such. We have changed the calculation of accuracy to reflect this. Accuracy is now defined as the proporition of correctly classified cases (true positives) with respect to the total number of cases that contain privacy-related data.

**Code optimization**. The code was optimized by introducing functionization (separating the code into separate functions that can be called from main). This makes the code more easy to read and also to (re)use.

**External discussion**. We discussed SEAA with the analytics team of Inholland and gained some valuable insights for improvements. Also, they will be sharing their dictionary with us.

## Results

A second version of SEAA was developed with above dictionary improvements. Also, the validation dataset was updated to the agreed-upon privacy definitions.

Running SEAA on the validation dataset resulted in the following:
Efficiency = 73.1% (down 0.4% from last sprint), accuracy = 76.1% (up 11.6% from last sprint).

## Discussion

Listed below are improvements listed by priority:

1. Overview of privacy definitions. With the help of the privacy officer of OO&S we have defined when an answer should be classified as 'possibly containing privacy-related information'. These definitions need to be combined and described in an overview document.
2. Create validation dataset. Currently we use fake data to validate SEAA. It would be better to use actual data. For this, it is needed that we take a random sample of about 10% of the actual data and annotate manually using the privacy definitions. With the current dataset a sample of about 300 cases is required, meaning each team member will annotated 100 cases: Pim > sample between cases 0-800, Anne: 800-1600, Fraukje: 1600+.
3. Easy efficiency improvements. Improve current Dutch dictionary with quick-fixes:
   - make an overview of all words that are not matched and count
   - based on above analysis decide if additional dictionaries need to be used, e.g. to account for conjugations
   - adjust for use of punctuation marks (e.g. 'n.v.t.' or 'nvt')
4. Accuracy improvements. Accuracy has increased by 11.6% since last sprint, however, it is still away from its goal of 99+%. To further increase accuracy it is vital to include the agreed upon 'privacy definitions' into SEAA. In short, the definitions that should be added to SEAA are:
    - Classify any answer that contains at least one word related to illness as possibly containing privacy data.
    - Classify any answer with words related to teachers and/or students as possibly containing privacy data.
We could use the Inholland dictionary to implement this.
5. Code optimization & performance.
   - Benchmark SEAA using two different approaches: join-method and word-for-word search method. Also, different libraries could be faster (e.g. numphy migth be faster than pandas).
