import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_urls_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        urls = []
        for a_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, a_tag["href"])  # Convert to absolute URL
            urls.append(full_url)
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def save_url_to_file(url, filepath):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        response = requests.get(url)
        response.raise_for_status()

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Saved content from {url} to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_to_file(url, year):
    urls =  get_urls_from_page(url)
    for url in urls:
        if str(year) not in url:
            print(f"Skipping {url}.")
            continue
        filepath = "../html/" + str(year) + "/" + url.split("/")[-1]
        save_url_to_file(url, filepath)


def main():
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2002.html", 2002)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2003.html", 2003)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2004.html", 2004)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2005.html", 2005)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2006.html", 2006)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2007.html", 2007)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2008.html", 2008)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2009.html", 2009)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2010.html", 2010)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2011.html", 2011)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2012.html", 2012)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2013.html", 2013)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2014.html", 2014)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2015.html", 2015)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2016.html", 2016)
    save_to_file("https://www.scei-concours.fr/statistiques/stat_sommaire_2017.html", 2017)

    save_to_file("https://www.scei-concours.fr/stat2018/stat_sommaire_2018.html", 2018)
    save_to_file("https://www.scei-concours.fr/stat2019/stat_sommaire_2019.html", 2019)
    save_to_file("https://www.scei-concours.fr/stat2020/stat_sommaire_2020.html", 2020)
    save_to_file("https://www.scei-concours.fr/stat2021/stat_sommaire_2021.html", 2021)
    save_to_file("https://www.scei-concours.fr/stat2022/stat_sommaire_2022.html", 2022)
    save_to_file("https://www.scei-concours.fr/statistiques.php", 2023)

if __name__ == "__main__":
    main()
