import pandas as pd

# Create sample data
data = {
    'Answer': [
        "De docenten zijn over het algemeen erg behulpzaam en deskundig. Vooral bij de eerstejaars vakken wordt er veel tijd genomen om concepten goed uit te leggen.",
        "Het studiemateriaal is helaas niet altijd even duidelijk gestructureerd. Soms mis ik concrete voorbeelden en moet ik veel tijd besteden aan het zoeken naar aanvullende bronnen.",
        "Mijn mentor mevrouw De Vries heeft mij uitstekend begeleid met mijn persoonlijke uitdagingen tijdens het eerste semester.",  # privacy concern
        "De prijzen in de kantine zijn het afgelopen jaar flink gestegen. Een gezonde lunch is bijna niet meer te betalen voor studenten.",
        "Het lesrooster is behoorlijk onvoorspelbaar en verandert regelmatig op het laatste moment, wat het lastig maakt om werk en studie te combineren.",
        "De werkgroepen zijn leerzaam maar te groot.",
        "Ik heb last van migraine waardoor ik soms lessen mis.",  # privacy concern
        "Het computerlab moet nodig geupgraded worden.",  # avg word
        "De bibliotheek is een fijne studyplek.",  # avg word
        "De feedback van docenten komt vaak te laat.",
        "Het gebouw is moeilijk bereikbaar met ov.",
        "De online leeromgeving blackboard werkt niet optimaal.",
        "De tentamens zijn goed georganiseerd.",
        "Er zijn te weinig stopcontacten in lokaal A4.23.",
        "De wifi connectie is vaak slecht.",  # avg word
        "Ik zou graag meer praktijkgerichte assignments willen.",  # avg word
        "De studieadviseur mevrouw Pietersen is zeer behulpzaam.",  # privacy concern
        "Het niveau van de workshops is uitstekend.",
        "De koffieautomaat op de 3e verdieping is vaak kapot.",
        "Er zou meer aandacht voor sustainability moeten zijn.",  # avg word
        "De deadlines zijn soms te kort op elkaar gepland.",
        "Het groepswerk is goed georganiseerd.",
        "Mijn RSI klachten maken het typen lastig.",  # privacy concern
        "De printers zijn vaak offline.",
        "Er zijn te weinig chilplekken.",  # avg word
        "De examens zijn te theoretisch. Vooral professor van der Veen is het te theoretisch.",
        "Het mentoraat systeem werkt goed.",
        "De powerpoints zijn duidelijk en informatief.",
        "Er is te weinig parkeerruimte voor scooters.",
        "De internationale studenten worden goed begeleid.",
        "De internationale sfeer op de campus is geweldig. Er worden veel culturele evenementen georganiseerd die bijdragen aan een inclusieve studieomgeving.",
        "Het nieuwe digitale aanmeldsysteem voor tentamens werkt veel efficiënter dan het oude systeem. Wel jammer dat er soms technische problemen zijn.",
        "De studieruimtes in het B-gebouw zijn recent gerenoveerd en voorzien van moderne faciliteiten. Dit heeft de studeer-ervaring aanzienlijk verbeterd.",
        "Het vak Onderzoeksmethoden zou beter aansluiten bij de praktijk als er meer actuele casestudies werden behandeld.",
        "De studentenpsycholoog heeft mij enorm geholpen met mijn faalangst tijdens tentamenperiodes.",  # privacy concern
    ],
    'respondent_id': range(1, 101),
    'question_id': ['Q1'] * 100
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV with semicolon separator
df.to_csv('../data/demo_answers.csv', sep=';', index=False, encoding='utf-8-sig')

print("Sample CSV file 'demo_answers.csv' has been created with 100 responses.")