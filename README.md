# HSE_ALGO_testsys

Scripts for automation process of score counting.
Description:

* [download_data.py](download_data.py) -- script to load data from testsys. 
```commandline
usage: download_data.py [-h] contests_path monitors_path results_path login token

positional arguments:
  contests_path  Path to .csv file with list of contests.
  monitors_path  Path to directory where to save monitors for each contest.
  results_path   Path to directory where to save results for each contest.
  login          Test sys login.
  token          Test sys token.
```


* [search_data.py](search_data.py) -- script to search data from testsys. 

```commandline
usage: search_data.py [-h] contests_path monitors_path results_path users_path scores_path 

positional arguments:
  contests_path  Path to .csv file with list of contests.
  monitors_path  Path to directory with monitors for each contets.
  results_path   Path to directory with results for each contest.
  users_path     Path to directory with list of users in .csv format.
  scores_path    Path to directory where to save users' scores.

```

Result output for each user contains scores for all contests and tasts (A, B, C, ...) in format .csv file: \
ok	- ok before deadline \
\[ok\]	- ok after deadline \
no	- not passed \
wa	- wrong answer 
