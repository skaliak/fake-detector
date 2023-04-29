
class DataAccessInterface:
    def __init__(self):
        pass

    def get_r4r_subreddit_names(self) -> list[str]:
        pass


# implementation of DataAccessInterface that uses hard-coded data
class HardCodedDataAccess(DataAccessInterface):
    def __init__(self):
        super().__init__()
        self._hc_data = self.__raw_data.splitlines()

    def get_r4r_subreddit_names(self) -> list[str]:
        return self._hc_data
    
    __raw_data = """r4r
polyamoryR4R
BreedingR4R
R4R30Plus
Kikpals
r4rDFW
r4rCanada
SFr4r
r4rMelbourne
r4rOntario
r4rSydney
TelegramR4R
SoCalR4R
VirginiaR4R
KansasCity_r4r
R4R40Plus
r4r_germany
r4rUtrecht
r4rOttawa
PhoenixR4R
IndiaR4R
r4rMississauga
peyups_R4R
phr4r
r4rindia
r4rScotland
EgyptR4R
houstonr4r
bostonr4r
r4rSeattle
r4rCalifornia
r4rNYC
r4rPortland
r4rtoronto
r4rmontreal
r4rinterracial
R4Rstralia
r4ruk
atlantar4r
BaltimoreAndDCr4r
IndoR4R
Floridar4r
r4rph
r4rdesis
r4rAsexual
r4rdatingindia
"""