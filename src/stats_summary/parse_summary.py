import os
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


def get_files():
    return ["stat2002/tout_concours_confondu_2002.htm",
            "stat2003/tout_concours_confondu_2003.htm",
            "stat2004/stat_generale_2004.htm",
            "stat2005/stat_generale_2005.htm",
            "stat2006/stat_generale_2006.htm",
            "stat2007/stat_generale_2007.htm",
            "stat2008/stat_generale_2008.htm",
            "stat2009/stat_generale_2009.html",
            "stat2010/stat_generale_2010.html",
            "stat2011/stat_generale_2011.html",
            "stat2012/stat_generale_2012.html",
            "stat2013/stat_generale_2013.html",
            "stat2014/stat_generale_2014.html",
            "stat2015/stat_generale_2015.html",
            "stat2016/stat_generale_2016.html",
            "stat2017/stat_generale_2017.html",
            "stat2018/stat_generale_2018.html",
            "stat2019/stat_generale_2019.html",
            "stat2020/stat_generale_2020.html",
            "stat2021/stat_generale_2021.html",
    ]


def get_year(path):
    # return path.split("/")[3][-4:]
    f_ext = path.split("/")[-1]
    f = f_ext.split(".")[0]
    return f.split("_")[-1]


def fix_encoding_errors(s):
    encoding_errors = {'Ã©': 'é',
                       'Ãª': 'ê',
                       'Ã§': 'ç',
                       'Ãš': 'è',
                       'ÃŽ': 'ô',
                       'Ã¢': 'â',
                       'Ã ': 'à',
    }
    for err in encoding_errors:
        s = s.replace(err, encoding_errors[err])
    return s


def clean_row(row):
    return [fix_encoding_errors(el.text) for el in row.find_all("td")]


def get_file_content(path):
    soup = BeautifulSoup(open(path, encoding="iso-8859-15"), 'lxml')
    table = soup.find('table')
    rows = table.find_all("tr")
    return [clean_row(row) for row in rows]


def is_line_ok(l):
    if len(l) == 1: # only ['']
        return False
    if len(l) == 2 or len(l) == 3:
        if len("".join(l[0].split())) == 0: #  only ['', ''] or ['', '', '']
            return False
    if len(l) == 5: # only ['Tous Concours confondus :', '', '', '', '']
        return False
    if len(l) == 6: # only ['Tous Concours confondus :', '', '', '', '', '']
        return False
    if len(l) == 7 or len(l) == 9:
        if len("".join(l[0].split())) == 0: # only: empty lists, headers, or "total" lines.
            return False
    not_interested = ["totaux",
                      "tous concours confondus",
                      "tout concours confondus :",
                      "tous concours confondus :",
                      ]
    if l[0].casefold() in not_interested:
        return False
    return True


def parse_to_file(filename, files):
    header_list = ["year_of_source",
                   "year",
                   "prepa",
                   "inscrits",
                   "admissibles",
                   "classes",
                   "propositions",
                   "entres",
                   "places",
                   ]
    with open(filename, "w") as f:
        f.write(",".join(header_list) + "\n")
        data_year = ""
        for fi in ["../../data/" + fi for fi in files]:
            content = get_file_content(fi)
            file_year = get_year(fi)
            for l_raw in content:
                l = [" ".join(li.split()) for li in l_raw]
                if not is_line_ok(l): continue
                if l[0].isnumeric():
                    for i in range(1, len(l)):
                        assert(l[i] == "")
                    data_year = l[0]
                    continue
                assert(len(l[0]) != 0)
                if "Inter".casefold() in l[0].casefold():
                    l[0] = "Inter-Filière"
                to_write = [str(file_year), str(data_year)]
                for i in range(7):
                    to_write.append(l[i])
                f.write(",".join(to_write) + "\n")


files = get_files()
parse_to_file("summary.csv", files)
