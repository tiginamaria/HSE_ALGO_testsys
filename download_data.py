import argparse
import os
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_table_from_page(page):
    html = BeautifulSoup(page.text)
    table = html.find("table", {"class": "mtab"})

    header = []
    for cell in table.findAll("tr", {"class": "head"})[0].findAll("th")[1:-3]:
        header.append(cell.text)

    results = [header]
    for row in table.findAll("tr", {"class": ['even', 'odd']})[:-4]:
        result = []
        cells = row.findAll("td")
        result.append(cells[1].text[4:])
        for cell in cells[2:-3]:
            result.append(cell['class'][0])
        results.append(result)

    results[0][0] = 'User'

    return results


def download_monitor(login: str, token: str, contests_path: str, monitors_path: str):
    df_contests = pd.read_csv(contests_path)

    if not os.path.exists(monitors_path):
        os.makedirs(monitors_path)

    for contest in df_contests['Contest'].values:
        page = requests.get("https://acm.math.spbu.ru/tsweb/monitor",
                            cookies={'freshness': '5', 'tsw': f'{login}|{token}|{contest}|'},
                            headers={'Cache-Control': 'no-cache'})
        results = get_table_from_page(page)
        pd.DataFrame(results[1:], columns=results[0]) \
            .to_csv(os.path.join(monitors_path, f'{contest}.csv'), index=False)


def download_results(contests_path: str, results_path: str):
    df_contests = pd.read_csv(contests_path)

    if not os.path.exists(results_path):
        os.makedirs(results_path)

    for contest in df_contests['Contest'].values:
        page = requests.get(f"http://acm.math.spbu.ru/cgi-bin/monitor_au.pl/m{contest}.dat")
        results = get_table_from_page(page)
        pd.DataFrame(results[1:], columns=results[0]) \
            .to_csv(os.path.join(results_path, f'{contest}.csv'), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('contests_path', type=str, help='Path to .csv file with list of contests.')
    parser.add_argument('monitors_path', type=str, help='Path to directory where to save monitors for each contest.')
    parser.add_argument('results_path', type=str, help='Path to directory where to save results for each contest.')

    parser.add_argument('login', type=str, help='Test sys login.')
    parser.add_argument('token', type=str, help='Test sys token.')

    args = parser.parse_args(sys.argv[1:])

    download_monitor(args.login, args.token, args.contests_path, args.monitors_path)
    download_results(args.contests_path, args.results_path)
