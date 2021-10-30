from bs4 import BeautifulSoup

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


def parse_to_file(f, path, filiere, year, sep):
    soup = BeautifulSoup(open(path, encoding="iso-8859-15"), 'lxml')
    table = soup.find_all('table')[1]
    rows = table.find_all("tr")
    #
    banque = ""
    for row in rows:
        heads = row.find_all("th")
        if len(heads) == 1:
            banque = sanitize_string(heads[0].text)
        cells = row.find_all("td")
        # Print the "year,filiere,banque" at beginning of line.
        do_print = True
        for idx, cell in enumerate(cells):
            # Remove the line
            # Inscrits, Admissibles, Classés, Rg du dernier appelé, Intégrés, Places
            if (cell.text == "Nb"): break
            content = sanitize_string(cell.text)
            if (content == "Rg dudernier appelé"): break
            if do_print:
                f.write(year + sep + filiere + sep + banque  + sep)
                do_print = False
            if (idx > 0):
                content = sanitize_number(content)
            end = sep if idx < len(cells) - 1 else "\n"
            f.write(sanitize_string(content) + end)


sep = '\t'

# Inscrits, Admissibles, Classés, Rg du dernier appelé, Intégrés, Places
header = "year" + sep + "filiere" + sep + "banque" + sep + "ecole" + sep + "inscrits_nb" + sep + "inscrits_filles" + sep + "inscrits_cinq_demi" + sep + "admissibles_nb" + sep + "admissibles_filles" + sep + "admissibles_cinq_demi" + sep + "classes_nb" + sep + "classes_filles" + sep + "classes_cinq_demi" + sep + "rg_dernier_appele" + sep +"integres_nb" + sep + "integres_filles" + sep + "integres_cinq_demi" + sep + "places"


prepas = ["bcpst",  "mp",  "pc",  "psi",  "pt",  "tsi"]

year = "2005"
path = "../../../data/stat" + year + "/"

for prepa in prepas:
    fname = year + "_" + prepa + ".tsv"
    prepend = "recap_concours_"
    file_loc = path + prepend + prepa + ".htm"
    # file_loc = path + prepa + ".html"
    # file_loc = path + "AfficheStatGenerale." + prepa + ".html"

    with open(fname, "w") as f:
        f.write(header + "\n")
        parse_to_file(f, file_loc, prepa, year, sep)
