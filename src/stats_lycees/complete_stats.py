import pandas as pd
import re


def get_code(s):
    # Below fails when several brackets
    # return s.split("(")[1].split(")")[0]
    ret = re.findall(r'\(.*?\)', s)
    assert(len(ret) > 0)
    return ret[-1]


def get_name(s):
    # Below fails when several brackets
    # return " ".join(s.split("(")[0].split())
    idx = -1
    for i, ch in enumerate(s):
        if (ch == "("):
            idx = i
    assert(idx >= 0)
    return " ".join(s[:idx].split())


def make_dict(with_code):
    keys = [get_code(el) for el in with_code]
    vals = [get_name(el) for el in with_code]
    # need to assert only there is no duplicate keys.
    # return dict(zip(keys, vals))
    ret = {}
    for k, v in zip(keys, vals):
        if not ret.__contains__(k):
            ret[k] = set()
        ret[k].add(v)
    return ret


def main():
    filename = "stats_lycees.csv"
    df = pd.read_csv(filename)
    lycees = df["etablissement"]
    assert(all([el.count("(") == el.count(")") for el in lycees]))
    with_code = [el for el in lycees if el.count("(") > 0]
    without_code = [el for el in lycees if el.count("(") == 0]
    assert(len(with_code) + len(without_code) == len(lycees))
    d = make_dict(with_code)
    # for el in d:
    #     print(el, "->", d[el])
    print("# of codes:                   ", len(d))
    print("# codes matching dupl lycees: ", len(["" for el in d if len(d[el]) != 1]))
    print("# of lycees without code:     ", len(set(without_code)))

    for dupl in [d[el] for el in d if len(d[el]) != 1]:
        print(dupl)

    print("Lycees without codes")
    for el in set(without_code):
        print(el)

    # I should check if there are several lycees with the same name but with different codes
    # if so, then I should see if I can use the city to tell them apart.


if __name__ == "__main__":
    main()
