# browserhist

> A CLI tool to fetch local browser data

History can either be dumped to a JSON file are uploaded to elasticsearch.

Currently supports:
 - Firefox on MacOS and Linux
 - Chromiumm on Linux
 - Google Chrome on MacOS

Results are of the format
```json
[
  {
    "url": "https://www.mozilla.org/en-US/firefox/59.0.1/firstrun/",
    "title": "Welcome to Firefox",
    "node": "machine01",
    "timestamp": "2018-03-17 21:01:30+00:00",
    "domain": "mozilla.org",
    "profile": "diacp6z2.default",
    "browser": "firefox",
    "local": {
      "timestamp": "2018-03-17 17:01:30-04:00",
      "hour": 17,
      "weekday": 5,
      "month": "Mar",
      "year": 2018
    }
  }
]
```

## Usage:
```sh
pip install "git+https://github.com/alella/browserhist.git"
browserhist --help
```


## Development
```sh
pipenv install
pipenv shell
pip install --editable .
browserhist --help
```
