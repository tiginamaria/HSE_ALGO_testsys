import argparse
import ast
import os
import sys
from typing import List

import pandas as pd


def get_contest_scores(df_contest: pd.DataFrame, user: pd.Series) -> pd.Series:
    df_user_contest = df_contest[df_contest['User'] == user['Login']]
    if df_user_contest.shape[0] != 0:
        return df_user_contest.iloc[0]

    scores = ['no'] * (df_contest.shape[1] - 2)
    return pd.Series(list(user.values) + scores, index=df_user_contest.columns)


def compare_contest_scores(user_results, user_monitor) -> List[str]:
    contest_scores = []
    for (result, monitor) in zip(user_results[2:], user_monitor[2:]):
        monitor = 'ok' if monitor in ['firstokeven', 'firstokodd'] else monitor
        result = 'ok' if result in ['firstokeven', 'firstokodd'] else result
        if result != 'ok' and monitor == 'ok':
            contest_scores.append(f'[{monitor}]')
        else:
            contest_scores.append(monitor)
    return contest_scores


def search_user_results(contests_path: str, monitors_path: str, results_path: str, scores_path: str, users_path: str):
    df_users = pd.read_csv(users_path, sep='\t')
    df_contests = pd.read_csv(contests_path)
    dones_count = []
    todos_count = []

    for _, user in df_users.iterrows():
        login = user['Login']
        if login == '-':
            dones_count.append(0)
            todos_count.append(0)
            continue

        contests_scores = []

        done_count, todo_count = 0, 0
        for _, contest in df_contests.iterrows():
            contest_name = contest['Contest']
            df_results = pd.read_csv(os.path.join(results_path, f'{contest_name}.csv'))
            df_monitor = pd.read_csv(os.path.join(monitors_path, f'{contest_name}.csv'))
            user_results = get_contest_scores(df_results, user)
            user_monitor = get_contest_scores(df_monitor, user)
            contest_scores = compare_contest_scores(user_results, user_monitor)

            musts = ast.literal_eval(contest['Must'])
            for i, _ in enumerate(musts):
                if contest_scores[i] == '[ok]':
                    done_count += 1
                elif 'ok' not in contest_scores[i]:
                    todo_count += 1

            contests_scores.append(list(contest.values[:1]) + [str(len(contest_scores))] + contest_scores)

        dones_count.append(done_count)
        todos_count.append(todo_count)

        size = max(list(map(lambda result: len(result), contests_scores)))

        for contest_scores in contests_scores:
            if len(contest_scores) < size:
                contest_scores += [''] * (size - len(contest_scores))

        columns = [chr(ord('A') + i) for i in range(0, size - 2)]
        pd.DataFrame(contests_scores, columns=['Contest', 'Total'] + columns) \
            .to_csv(os.path.join(scores_path, f'{login}.csv'), index=False, sep='\t')

    df_users['done'] = dones_count
    df_users['todo'] = todos_count
    df_users.to_csv(os.path.join(scores_path, f'total.csv'), index=False, sep='\t')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('contests_path', type=str, help='Path to .csv file with list of contests.')
    parser.add_argument('monitors_path', type=str, help='Path to directory where to save monitors.')
    parser.add_argument('results_path', type=str, help='Path to directory where to save results.')
    parser.add_argument('users_path', type=str, help='Path to directory with list of users in .csv format.')
    parser.add_argument('scores_path', type=str, help='Path to directory where to save users scores.')

    args = parser.parse_args(sys.argv[1:])

    search_user_results(args.contests_path, args.monitors_path, args.results_path, args.scores_path, args.users_path)
