import pandas as pd


def main():
    filename = "stats_lycees.csv"
    df = pd.read_csv(filename)
    n = len(df)

    total = {"inscrits":    list(df["inscrits"]),
             "admissibles": list(df["admissibles"]),
             "classes":     list(df["classes"]),
             "integres":    list(df["integres"]),
             }

    filles = {"inscrits":    list(df["inscrits dont filles"]),
              "admissibles": list(df["admissibles dont filles"]),
              "classes":     list(df["classes dont filles"]),
              "integres":    list(df["integres dont filles"]),
             }

    sub = lambda x, y: [a - b for a, b in zip(x, y)]
    garcons = {"inscrits":    sub(total["inscrits"], filles["inscrits"]),
               "admissibles": sub(total["admissibles"], filles["admissibles"]),
               "classes":     sub(total["classes"], filles["classes"]),
               "integres":    sub(total["integres"], filles["integres"]),
               }

    results = {"total": total, "filles": filles, "garcons": garcons}

    checks =[["inscrits", "admissibles"],
             ["inscrits", "classes"],
             ["inscrits","integres"],
             ["admissibles", "classes"],
             ["admissibles", "integres"],
             ["classes", "integres"],
             ]

    # incoherences = set()
    incoherences = dict()
    for r_key in results:
        for [a, b] in checks:
            incoherences[" ".join([r_key, a, b])] = 0

    counts = dict(zip([el for el in results], [0] * len(results)))
    for r_key in results:
        r = results[r_key]
        for i in range(n):
            for [a, b] in checks:
                if r[a][i] < r[b][i]:
                    print(r_key,[a, b], [df[el][i] for el in df])
                    # incoherences.add(" ".join([r_key, a, b]))
                    incoherences[" ".join([r_key, a, b])] += 1
                    counts[r_key] += 1
    for inc in incoherences:
        print(inc, "->", incoherences[inc])
    print(counts)
    total = sum([counts[el] for el in counts])
    print(total)
    print(100 * (total / len(df)), "%")


if __name__ == "__main__":
    main()
