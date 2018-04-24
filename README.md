# await-ccb

Given a git SHA, waits for a corresponding [Google Cloud Container Builder](https://cloud.google.com/container-builder/) build to complete successfully.


- If a successful build exists, exits 0.
- If a running or queued build exists, polls until no running builds are found
  or the --poll-limit is reached.
- If no running/queued build is found in the initial search, repeats the search
  up to --search-limit times to see if a running build appears.

## Install

    pip install await-ccb
    
## Usage

```
Usage:
    await-ccb -c credentials.json -r repo-name -s git-sha
        [-t -p my-project --poll-interval 5 --poll-limit 360 --search-limit 5]
    await-ccb --help
    await-ccb --version

Options:
    -c CREDENTIALS_JSON, --credentials CREDENTIALS_JSON
        Path to service account credentials in Google JSON format

    -p PROJECT, --project PROJECT
        Google Code Project ID, defaults to project from credentials

    -r REPO, --repo REPO
        Repo name, as known to CCB (e.g. github-thedyrt-await-ccb)

    -s SHA, --sha SHA
        Git SHA to observer builds for

    -t, --trigger
        Trigger a build if none are found. Requires an existing build trigger
        to be configured for the repo in the Google Cloud Console.

    --search-limit LIMIT
        Number of attempts to make in the initial search for running builds
        [Default: 3]

    --poll-limit LIMIT
        Number of poll requests to make before giving waiting on running builds
        to complete. Total polling time is --poll-limit * --poll-interval.
        [Default: 360]

    --poll-interval SECONDS
        Number of seconds to wait between requests
        [Default: 5]

    -h, --help
        Show this help

    --version
        Show version info

```
