# A function to get the names of the medewerkers from the database
# and convert them to a list of names

from functions.db_functions import DB

def get_medewerkers_names(db):
    # Get the names of the medewerkers from the database
    db = DB()
    names = db.read_from_db(query='SELECT * FROM DM.D_MEDEWERKERS')
    # Convert the names to a list of names
    names_list = names.tolist()
    return names_list
