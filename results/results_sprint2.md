# Pilot SEAA - Sprint 2 (7 Dec - 21 Dec)

**Dictionary**. In the second week we changed the data cleaning step such that the dictionary words are no longer changed to all smallcase. This means that all person names in answers will be classified as containing privacy information that could be traced back to the individual.

**Validation data definition**. In a meeting with different stakeholders (product owner, privacy officer, development team) we determined a first version of 'privacy definitions'. These are a set of rules that determine when the SEAA algorithm should or should not classify an answer as possibly containing privacy data.

**Accuracy definition change**. For SEAA it is of vital importance that all cases containing any type of privacy related information are classified as such. We have changed the calculation of accuracy to reflect this. Accuracy is now defined as the proporition of correctly classified cases (true positives) with respect to the total number of cases that contain privacy-related data.

**Code optimization**. The code was optimized by introducing functionization (separating the code into separate functions that can be called from main). This makes the code more easy to read and also to (re)use.

## Results

A second version of SEAA was developed with above dictionary improvements. Also, the validation dataset was updated to the agreed-upon privacy definitions.

Running SEAA on the validation dataset resulted in the following:
Efficiency = 73.1% (down 0.4% from last sprint), accuracy = 76.1% (up 11.6% from last sprint).

## Discussion

Accuracy improvement. Accuracy has increased by 11.6% since last sprint, however, it is still away from its goal of 99+%. To further increase accuracy it is vital to include the agreed upon 'privacy definitions' into SEAA. In short, the definitions that should be added to SEAA are:
    - Classify any answer that contains at least one word related to illness as possibly containing privacy data.
    - Classify any answer with words related to teachers and/or students as possibly containing privacy data.
