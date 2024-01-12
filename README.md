# SEAA
semi-automatische anonimisering

Open antwoorden NSE
Woordenboek met alle Nederlandse woorden. Probleem dat hier ook namen in voorkomen.
Lijst met namen en achternamen

Nederlandse voor- en achternamen verwijderen uit woordenboek.
Alle woorden die niet in het woordenboek staan filteren.

AVG 0/1 kolom toevoegen. 
0=niet gevoelig. Alle woorden uit open antwoord komen overeen met gefilterd woordenboek.
1=één of meerdere AVG gevoelige worden gevonden in open antwoord.

Toelichtingen kolom toevoegen.
Overzicht van welke woorden we niet geclassificeerd hebben als AVG gevoelig. 

Open antwoorden inlezen
Woordenlijst inlezen
Matchen woordenlijst op open antwoorden

## Privacy definitions

In general SEAA follows the Dutch implementation of the GDPR as provided by the [Autoriteit Persoonsgegevens](https://www.autoriteitpersoonsgegevens.nl/) (i.e. the [Dutch Data Protection Authority](https://www.autoriteitpersoonsgegevens.nl/en/about-the-dutch-dpa/tasks-and-powers-of-the-dutch-dpa)). Since SEAA is an algorithm, a set of specified rules about when exactly privacy-concerns arise are needed. The enforcement of GDPR on data, however, is not specified in detail so a specific set of rules was defined based on the GDPR.
A word and/or sequence of words is defined as “possibly containing privacy-related information” when one of the following:

- Contains information directly relatable to a person. That is:
  - First name, last name
  - Email address
  - IP address
  - Address
  - Phone number
  - Student number
  - BSN number
- Contains any mention of illness(type).
- Contains a term that identifies a type of educational person (e.g. ‘student’ and ‘professor’)
