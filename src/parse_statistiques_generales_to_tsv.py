import os
from bs4 import BeautifulSoup


def is_statistique_generale(year):
    filieres = ["bcp", "bcpst", "mp", "mpi", "pc", "psi", "pt", "tb", "tpc", "tsi"]
    is_filiere = lambda x: any(f in x.casefold() for f in filieres)

    year_actions = {
        "2002": lambda x: "recap_concours_" in x and is_filiere(x),
        "2003": lambda x: "recap_concours_" in x and is_filiere(x),
        "2004": lambda x: "recap_concours_" in x and is_filiere(x),
        "2005": lambda x: "recap_concours_" in x and is_filiere(x),
        "2006": lambda x: "_" not in x and is_filiere(x),
        "2007": lambda x: "StatSession" in x and is_filiere(x),
        "2008": lambda x: "_" not in x and "lycee" not in x.casefold() and is_filiere(x),
        "2009": lambda x: "_" not in x and is_filiere(x) and "ccmp" not in x,
        "2010": lambda x: "_" not in x and is_filiere(x),
        "2011": lambda x: "AfficheStatGenerale" in x and is_filiere(x),
        "2012": lambda x: "AfficheStatGenerale" in x and is_filiere(x),
        "2013": lambda x: "_" not in x and is_filiere(x),
        "2014": lambda x: "_" not in x and is_filiere(x),
        "2015": lambda x: "_" not in x and is_filiere(x),
        "2016": lambda x: "_" not in x and is_filiere(x),
        "2017": lambda x: "_" not in x and is_filiere(x),
        "2018": lambda x: "_" not in x and is_filiere(x),
        "2019": lambda x: "_" not in x and is_filiere(x),
        "2020": lambda x: "_" not in x and is_filiere(x),
        "2021": lambda x: "_" not in x and is_filiere(x),
        "2022": lambda x: "_" not in x and is_filiere(x),
        "2023": lambda x: "_" not in x and is_filiere(x),
        "2024": lambda x: "_" not in x and is_filiere(x),
    }
    return year_actions[year]


def statistiques_generales_paths(file_path):
    ret = {}
    for entry in os.listdir(file_path):
        entry_path = os.path.join(file_path, entry)
        assert os.path.isdir(entry_path)
        ret[entry] = [
            os.path.relpath(os.path.join(entry_path, sub_entry), start=os.getcwd())
            for sub_entry in os.listdir(entry_path)
            if is_statistique_generale(entry)(sub_entry)
        ]
    return ret


def sanitize_string(s):
    s = " ".join(s.split())
    non_break_space = u"\xa0"
    s.replace(non_break_space, "¥")
    return s


def get_title(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        h1 = soup.find("h1")
        if h1 is not None:
            return h1.get_text(strip=True)
        h4 = soup.find("h4")
        if h4 is not None:
            return h4.get_text(strip=True)
        assert(False)


def parse(year, filenames, header_fn, parse_fn):
    header = header_fn()

    tsv_directory = os.path.join("../tsv", year)
    os.makedirs(tsv_directory, exist_ok=True)

    for filename in filenames:
        filiere = get_title(filename).split(" - ")[0]
        target = os.path.join(tsv_directory, f"{filiere}.tsv")

        print(f"Parsing {filename} into {target}...")
        with open(target, "w") as f:
            f.write("\t".join(header) + "\n")
            parse_fn(f, filename, filiere, year, "\t")
        print("Done.")


def header_v1():
    return [
        "year", "filiere", "banque", "ecole",
        "inscrits_nb", "inscrits_filles", "inscrits_cinq_demi",
        "admissibles_nb", "admissibles_filles", "admissibles_cinq_demi",
        "classes_nb", "classes_filles", "classes_cinq_demi",
        "appeles",
        "integres_nb", "integres_filles", "integres_cinq_demi",
        "places"
    ]


def parse_v1(year, filenames):
    parse(year, filenames, header_v1, parse_to_file_v1)


def header_v2():
    return [
        "year", "filiere", "banque", "ecole",
        "inscrits_nb", "inscrits_filles", "inscrits_cinq_demi",
        "admissibles_nb", "admissibles_filles", "admissibles_cinq_demi",
        "classes_nb", "classes_filles", "classes_cinq_demi",
        "rang_du_dernier_appele",
        "integres_nb", "integres_filles", "integres_cinq_demi",
        "places"
    ]

def parse_v2(year, filenames):
    parse(year, filenames, header_v2, parse_to_file_v1)


def header_v3():
    return [
        "year", "filiere", "banque", "ecole",
        "inscrits_nb", "inscrits_filles", "inscrits_cinq_demi",
        "admissibles_nb", "admissibles_filles", "admissibles_cinq_demi",
        "classes_nb", "classes_filles", "classes_cinq_demi",
        "integres_nb", "integres_filles", "integres_cinq_demi",
        "integres_rg_median", "integres_rg_moyen",
        "places"
    ]


def parse_v3(year, filenames):
    parse(year, filenames, header_v3, parse_to_file_v2)


def header_v4():
    return [
        "year", "filiere", "banque", "ecole",
        "inscrits_nb", "inscrits_filles", "inscrits_cinq_demi",
        "admissibles_nb", "admissibles_filles", "admissibles_cinq_demi",
        "classes_nb", "classes_filles", "classes_cinq_demi",
        "integres_nb", "integres_filles", "integres_cinq_demi",
        "integres_rg_median", "integres_rg_moyen",
        "nb_integres_interfilieres",
        "places"
    ]


def parse_v4(year, filenames):
    parse(year, filenames, header_v4, parse_to_file_v3)


def parse_to_file_v1(f, path, filiere, year, sep):
    parse_to_file(f, path, filiere, year, sep, skip_length=12, content_length=18)


def parse_to_file_v2(f, path, filiere, year, sep):
    parse_to_file(f, path, filiere, year, sep, skip_length=14, content_length=19)


def parse_to_file_v3(f, path, filiere, year, sep):
    parse_to_file(f, path, filiere, year, sep, skip_length=14, content_length=20)


def parse_to_file(f, path, filiere, year, sep, skip_length, content_length):
    soup = BeautifulSoup(open(path, encoding="iso-8859-15"), "lxml")

    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")

        banque = ""
        for row in rows:
            heads = row.find_all("th")
            if len(heads) == 1:
                banque = sanitize_string(heads[0].text)
            cells = [sanitize_string(el.text) for el in row.find_all("td")]

            # Skip the line "Nb, Filles, 5-demi, Nb, Filles, 5-demi, Nb, Filles, 5-demi, Nb, Filles, 5-demi"
            if(len(cells) == skip_length): continue
            for cell in cells:
                assert(cell != "Nb")
                assert(cell != "appelés")
            contents = [year, filiere, banque] + cells
            if len(contents) == content_length:
                f.write(sep.join(contents) + "\n")


def main():
    path = "../html/"
    statistiques_generales = statistiques_generales_paths(path)

    for year in range(2002, 2024):
        filenames = statistiques_generales[str(year)]
        if year in range(2002, 2004):
            parse_v1(str(year), filenames)
        elif year in range(2004, 2013):
            parse_v2(str(year), filenames)
        elif year in range(2013, 2018):
            parse_v2(str(year), filenames)
        elif year in range(2018, 2022):
            parse_v3(str(year), filenames)
        elif year in range(2022, 2024):
            parse_v4(str(year), filenames)


if __name__ == "__main__":
    main()
