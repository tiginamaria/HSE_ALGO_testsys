import argparse
import os
import sys

import pandas as pd


def get_contest_scores(df: pd.DataFrame, user: str):
    df_user = df[df['User'] == user]
    contest_scores = []
    for i in range(0, ord(df.columns[1][-1]) - ord('A')):
        contest_scores.append('')
    if df_user.shape[0] > 0:
        contest_scores += list(df_user.iloc[0].values)[1:]
    else:
        contest_scores += list(['no'] * (df.shape[1] - 1))

    return contest_scores


def compare_contest_scores(user_results, user_monitor):
    contest_scores = []
    for (result, monitor) in zip(user_results, user_monitor):
        if result not in ['ok', 'firstokeven'] and monitor in ['ok', 'firstokeven']:
            contest_scores.append(f'[{monitor}]')
        else:
            contest_scores.append(monitor)
    return contest_scores


def search_user_results(contests_path: str, monitors_path: str, results_path: str, scores_path: str, users_path: str):
    df_users = pd.read_csv(users_path)
    df_contests = pd.read_csv(contests_path)

    for user in df_users['User'].values:
        contests_scores = []

        for contest in df_contests['contest']:
            df_results = pd.read_csv(os.path.join(results_path, f'{contest}.csv'))
            df_monitor = pd.read_csv(os.path.join(monitors_path, f'{contest}.csv'))
            user_results = get_contest_scores(df_results, user)
            user_monitor = get_contest_scores(df_monitor, user)
            contest_scores = compare_contest_scores(user_results, user_monitor)

            contests_scores.append([contest, len(contest_scores)] + contest_scores)

        size = max(list(map(lambda result: len(result), contests_scores)))
        for contest_scores in contests_scores:
            if len(contest_scores) < size:
                contest_scores += [''] * (size - len(contest_scores))

        columns = [chr(ord('A') + i) for i in range(0, size - 2)]
        pd.DataFrame(contests_scores, columns=['Contest', 'Total'] + columns) \
            .to_csv(os.path.join(scores_path, f'{user}.csv'), index=False, sep='\t')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('contests_path', type=str, help='Path to .csv file with list of contests.')
    parser.add_argument('monitors_path', type=str, help='Path to directory where to save monitors.')
    parser.add_argument('results_path', type=str, help='Path to directory where to save results.')
    parser.add_argument('users_path', type=str, help='Path to directory with list of users in .csv format.')
    parser.add_argument('scores_path', type=str, help='Path to directory where to save users scores.')

    args = parser.parse_args(sys.argv[1:])

    search_user_results(args.contests_path, args.monitors_path, args.results_path, args.scores_path, args.users_path)
