import os
from bs4 import BeautifulSoup


def list_prepas() :
    return ["BCPST",  "MP",  "PC",  "PSI",  "PT",  "TSI", "TPC", "TB"]


def sanitize_string(s):
    replace_to = {}
    non_break_space = u'\xa0'
    replace_to[non_break_space] = "¥"
    replace_to["¥¥"] = "¥"
    replace_to["\n"] = ""
    replace_to["\t"] = ""
    replace_to[" -"] = "-"
    replace_to["- "] = "-"
    replace_to["  "] = " "
    for key, value in replace_to.items():
        while key in s:
            s = s.replace(key, value)
    s = s.lstrip(" ")
    s = s.rstrip(" ")
    return s


def sanitize_number(s):
    replace_to = {}
    replace_to[","] = "."
    replace_to["%"] = ""
    replace_to["*"] = ""
    for key, value in replace_to.items():
        while key in s:
            s = s.replace(key, value)
    return s


def get_files():
    year_start = 2002
    year_end = 2020 # For consistency, but no lycee data in 2020
    years = range(year_start, year_end + 1)
    ret = []
    for year in years:
        path = "../../data/stat" + str(year) + "/"
        for f in os.listdir(path):
            if "lycee" not in f: continue
            if os.path.isdir(path + f):
                for ff in os.listdir(path + f):
                    ret.append(path + f + "/" + ff)
            else:
                ret.append(path + f)
    return ret


def sanitize_h1(h1):
    year_start = 2002
    year_end = 2020 # For consistency, but no lycee data in 2020
    years = range(year_start, year_end + 1)
    for year in years:
        h1 = h1.replace(str(year), "")
    h1 = h1.replace("?", "")
    h1 = h1.replace("\n","")
    h1 = h1.replace(".", ". ")
    h1 = h1.replace("  ", " ")
    # return h1
    return " ".join(h1.split())


def get_prepa(h1):
    prepas = list_prepas()
    l = h1.split(" ")
    for el in l:
        for prepa in prepas:
            if (prepa.casefold() == el.casefold()):
                return prepa
    for el in l:
        if "PS" in el or "X-ESPCI" in el:
            return "PSI"
        elif "TS" in el:
            return "TSI"
    assert(False)


def get_concours(f, h1):
    prepa = get_prepa(h1)
    if f.count("/") == 4:
        return sanitize_concours(get_concours_from_h1(h1), prepa)
    elif f.count("/") == 5:
        return sanitize_concours(get_concours_from_f(f, prepa), prepa)
    assert(False)



def get_concours_from_f(f, prepa):
    # the order is important. Should go from reverse topolgical order for substrings.
    remove = [".html", ".htm", "AfficheStatLyceePT.", "AfficheStatLycee",
              "lycees", "lycee", "stat--", "-2007", "()", "banque"]
    s = f.split("/")[-1].casefold()
    for el in remove:
        s = s.replace(el.casefold(), "")
    # return " ".join(filter(lambda el: len(el) > 0, s.split("_")))
    ret = " ".join(filter(lambda el: len(el) > 0, s.split("_")))
    return " ".join(filter(lambda el: el.casefold() != prepa.casefold(), ret.split()))



def get_concours_from_h1(h1):
    concours = h1.strip()
    if concours[-1] == '-':
        concours = concours[:-1]
        concours = concours.strip()
    this_prepa = [get_prepa(h1).casefold()]
    if this_prepa[0] == "PSI".casefold():
        this_prepa.append("PS".casefold())
    if this_prepa[0] == "TSI".casefold():
        this_prepa.append("TS".casefold())
    is_ok = lambda el : len(el) > 0 and el.casefold() not in this_prepa
    concours = " ".join([el for el in concours.split(" ") if is_ok(el)])
    for e in ['Ú', 'é', 'è', 'Ã©']:
        concours = concours.replace(e, "e")
    for E in ['É']:
        concours = concours.replace(E, "E")
    assert(concours.isascii())
    return concours


def get_h1(path):
    soup = BeautifulSoup(open(path, encoding="iso-8859-15"), 'lxml')
    return sanitize_h1(soup.find("h1").text)


def get_year(path):
    return path.split("/")[3][-4:]


def parse_to_file(f, path):
    soup = BeautifulSoup(open(path, encoding="iso-8859-15"), 'lxml')
    table = soup.find('table')
    rows = table.find_all("tr")
    french_characters =  ['é', 'è', 'É', 'ç', 'â', 'ô', 'à', 'ê', 'î']
    encoding_errors = {'Ã©': 'é',
                       'Ãª': 'ê',
                       'Ã§': 'ç',
                       'Ãš': 'è',
                       'ÃŽ': 'ô',
                       'Ã¢': 'â',
                       'Ã ': 'à',
    }
    to_ascii = {'Ã©': 'e',
                # 'Ãª': 'e',
                # 'Ã§': 'c',
                # 'Ãš': 'e',
                # 'ÃŽ': 'o',
                # 'Ã¢': 'a',
                # 'Ã ': 'a',
                'é': 'e',
                # 'è': 'e',
                # 'É': 'E',
                # 'ç': 'c',
                # 'â': 'a',
                # 'ô': 'o',
                # 'à': 'a',
                # 'ê': 'e',
                # 'î': 'i',
    }

    for row in rows:
        heads = row.find_all("th")
        cells = row.find_all("td")
        #
        hs = [" ".join(hi.text.split()) for hi in heads]
        cs = [" ".join(ci.text.split()) for ci in cells]
        header = ",".join(hs)
        line = ",".join(cs)
        #
        for err in encoding_errors:
            header = header.replace(err, encoding_errors[err])
            line = line.replace(err, encoding_errors[err])
        for el in to_ascii:
            header = header.replace(el, to_ascii[el])
        header = header.lower()
        #
        assert(line.count(",") in [0, 9])
        assert(header.count(",") in [0, 9])
        only_one = lambda a, b: (a or b) and (not(a and b))
        assert(only_one((len(line) == 0), (len(header) == 0)))
        # Verify there's no comma in the content
        for hi in hs:
            assert(hi.count(",") == 0)
        for ci in cs:
            assert(ci.count(",") == 0)
        #verify all the caracters are ascii
        is_ok = lambda el: (el.isascii()) or (el in french_characters)
        assert(all([is_ok(el) for el in header]))
        assert(all([is_ok(el) for el in line]))
        content = header if len(header) > 0 else line
        f.write(content + "\n")


def parse_to_single_file(f, path):
    soup = BeautifulSoup(open(path, encoding="iso-8859-15"), 'lxml')
    table = soup.find('table')
    rows = table.find_all("tr")
    h1 = get_h1(path)
    concours = get_concours(path, h1)
    prepa = get_prepa(h1)
    year = get_year(fi)
    french_characters =  ['é', 'è', 'É', 'ç', 'â', 'ô', 'à', 'ê', 'î']
    encoding_errors = {'Ã©': 'é',
                       'Ãª': 'ê',
                       'Ã§': 'ç',
                       'Ãš': 'è',
                       'ÃŽ': 'ô',
                       'Ã¢': 'â',
                       'Ã ': 'à',
    }
    to_ascii = {'Ã©': 'e',
                # 'Ãª': 'e',
                # 'Ã§': 'c',
                # 'Ãš': 'e',
                # 'ÃŽ': 'o',
                # 'Ã¢': 'a',
                # 'Ã ': 'a',
                'é': 'e',
                # 'è': 'e',
                # 'É': 'E',
                # 'ç': 'c',
                # 'â': 'a',
                # 'ô': 'o',
                # 'à': 'a',
                # 'ê': 'e',
                # 'î': 'i',
    }

    for row in rows:
        cells = row.find_all("td")
        cs = [" ".join(ci.text.split()) for ci in cells]
        line = ",".join(cs)
        if (len(line) == 0): continue
        #
        for err in encoding_errors:
            line = line.replace(err, encoding_errors[err])
        assert(line.count(",") in [0, 9])
        # Verify there's no comma in the content
        for ci in cs:
            assert(ci.count(",") == 0)
        #verify all the caracters are ascii
        is_ok = lambda el: (el.isascii()) or (el in french_characters)
        assert(all([is_ok(el) for el in line]))
        to_write = (",".join([year, concours, prepa])) + "," + line
        f.write(to_write + "\n")



def sanitize_concours(concours, prepa):
    BCPST = {"ens": "ens",
             "Banque Agro": "agro",
             "agro": "agro",
             "Banque G2E": "g2e",
             "g2e": "g2e",
    }
    MP = {"x-ens": "x-ens",
          "mine pont": "mines-ponts",
          "ecole polytech": "x",
          "Banque INTER-ENS": "ens",
          "Banque CCP": "ccp",
          "epita": "epita",
          "mines": "mines-ponts",
          "polytech": "x",
          "cs": "centrale-supelec",
          "Concours Ec. poly.": "x",
          "e3a": "e3a",
          "x": "x",
          "ccinp": "ccp",
          "Banque Centrale-Supelec": "centrale-supelec",
          "x ens": "x-ens",
          "centrale": "centrale-supelec",
          "ccp": "ccp",
          "Banque Mines Ponts": "mines-ponts",
          "ccmp": "mines-ponts",
          "mine": "mines-ponts",
          "ecp": "centrale-supelec",
          "ecole poly": "x",
    }
    PC = {"x-ens": "x-ens",
          "mine pont": "mines-ponts",
          "ecole polytech": "x",
          "Banque INTER-ENS": "ens",
          "Banque CCP": "ccp",
          "epita": "epita",
          "mines psi": "mines-ponts",
          "ecp": "centrale-supelec",
          "mines": "mines-ponts",
          "cs": "centrale-supelec",
          "e3a": "e3a",
          "x": "x",
          "ccinp": "ccp",
          "Banque Centrale-Supelec": "centrale-supelec",
          "x ens": "x-ens",
          "centrale": "centrale-supelec",
          "ccp": "ccp",
          "Banque Mines Ponts": "mines-ponts",
          "Banque Ec. poly. -ESPCI": "x",
          "ccmp": "mines-ponts",
          "mine": "mines-ponts",
          "polytech": "x",
          "ecole poly": "x",
    }
    PSI = {"centrale": "centrale-supelec",
           "ccp": "ccp",
           "Banque Mines Ponts": "mines-ponts",
           "e3a": "e3a",
           "x ens": "x-ens",
           "x-ens": "x-ens",
           "mines": "mines-ponts",
           "mine pont": "mines-ponts",
           "x": "x",
           "ccmp": "mines-ponts",
           "ccinp": "ccp",
           "cs": "centrale-supelec",
           "Banque Centrale-Supelec": "centrale-supelec",
           "Banque CCP": "ccp",
           "ecp": "centrale-supelec",
           "Banque ENS Cachan/X": "x-ens",
           "Banque ENS Cachan/X-ESPCI": "x-ens",
           "epita": "epita",
    }
    PT = {"stat-pt-x": "x",
          "Concours Centrale-Supelec": "centrale-supelec",
          "Concours commun Polytechnique": "ccp",
          "stat-pt-ensam": "ensam",
          "stat-pt-centrale": "centrale-supelec",
          "Concours Commun Mines-Ponts": "mines-ponts",
          "Concours Ecole Polytechnique": "x",
          "ensam": "ensam",
          "polytechniquept": "x",
          "Concours Ensam": "ensam",
          "cc mines ponts": "mines-ponts",
          "mines": "mines-ponts",
          "cs": "centrale-supelec",
          "stat-pt-ccp": "ccp",
          "centrale supelec": "centrale-supelec",
          "x": "x",
          "minespt": "mines-ponts",
          "ccinp": "ccp",
          "ccppt": "ccp",
          "centrale": "centrale-supelec",
          "ccp": "ccp",
          "centralept": "centrale-supelec",
          "ccmp": "mines-ponts",
          "stat-pt-ccmp(pt)": "mines-ponts",
          "ensampt": "ensam",
    }
    TSI = {"centrale": "centrale-supelec",
           "ccp": "ccp",
           "ccinp": "ccp",
           "cs": "centrale-supelec",
           "Banque Centrale-Supelec": "centrale-supelec",
           "Banque CCP": "ccp",
           "ecp": "centrale-supelec",
           "epita": "epita",
    }
    if prepa == "BCPST":
        return BCPST[concours]
    elif prepa == "MP":
        return MP[concours]
    elif prepa == "PC":
        return PC[concours]
    elif prepa == "PSI":
        return PSI[concours]
    elif prepa == "PT":
        return PT[concours]
    elif prepa == "TSI":
        return TSI[concours]
    elif prepa == "TPC":
        assert(False)
    elif prepa == "TB":
        assert(False)
    else:
        assert(False)



# path = "../../data/stats_lycees/"
path = "./"
files = get_files()
for fi in files:
    h1 = get_h1(fi)
    # this_prepa = get_prepa(h1)
    concours = get_concours(fi, h1)
    prepa = get_prepa(h1)
    year = get_year(fi)

    fname = path + "_".join([year, prepa, concours]) + ".csv"
    with open(fname, "w") as f:
        parse_to_file(f, fi)


fname = "stats_lycees.csv"
with open(path + fname, "w") as f:
    f.write("year,concours,prepa,ville,etablissement,inscrits,dont filles,admissibles,dont filles,classes,dont filles,integres,dont filles\n")
    for fi in files:
        parse_to_single_file(f, fi)
