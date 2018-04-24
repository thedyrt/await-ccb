from google.oauth2 import service_account
from time import sleep
import googleapiclient.discovery

class BuildPoller:
    INCOMPLETE_STATES = ('QUEUED', 'WORKING')
    SUCCESSS_STATES = ('SUCCESS',)

    def __init__(self, credentials_path, project, repo, sha, trigger,
                 search_limit=3, poll_limit=360, poll_interval=5):
        self.credentials = self.__load_credentials(credentials_path)
        self.project = project or self.credentials.project_id
        self.search_limit = search_limit
        self.poll_limit = poll_limit
        self.poll_interval = poll_interval
        self.repo = repo
        self.sha = sha
        self.trigger_build = trigger
        self.client = googleapiclient.discovery.build(
                        'cloudbuild', 'v1', credentials=self.credentials)

    def __load_credentials(self, credentials_path):
        if not credentials_path:
            print((
                'Could not load credentials. Proivde account credentials via '
                '--credentials or set GOOGLE_APPLICATION_CREDENTIALS'))
            exit(2)

        return service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform'])

    def await_success(self):
        builds = []

        def log_builds():
            if builds:
                for b in builds:
                    print('- {0}: {1}'.format(b['status'], b['id']))
                print('===')
            else:
                print('No builds found')

        def any_successful():
            return any([b['status'] in self.SUCCESSS_STATES for b in builds])

        def any_incomplete():
            return any([b['status'] in self.INCOMPLETE_STATES for b in builds])

        print('Searching for active or successful builds...')
        for search_attempt in range(1, self.search_limit):
            builds = self.builds_for_commit()
            log_builds()
            if any_incomplete() or any_successful():
                break

            sleep(self.poll_interval)

        if self.trigger_build and not (any_successful() or any_incomplete()):
            build = self.run_trigger()
            if build:
                builds = [build]
                log_builds()

        if any_incomplete():
            print('Waiting for builds to complete...')

        for poll_attempt in range(1, self.poll_limit):
            log_builds()
            if not any_incomplete():
                break

            sleep(self.poll_interval)
            builds = self.builds_for_commit()

        return any_successful()

    def run_trigger(self):
        trigger = self.repo_trigger()

        if not trigger:
            return None

        print('Running build trigger {0}'.format(trigger['id']))

        result = (
            self.client
            .projects()
            .triggers()
            .run(
                projectId=self.project,
                triggerId=trigger['id'],
                body={
                    'projectId': self.project,
                    'repoName': self.repo,
                    'commitSha': self.sha,
                })
            .execute())

        if 'metadata' in result and 'build' in result['metadata']:
            return result['metadata']['build']
        else:
            return None

    def repo_trigger(self):
        result = (
            self.client
            .projects()
            .triggers()
            .list(projectId=self.project)
            .execute())

        if 'triggers' in result:
            trigger = [
                t for t in result['triggers']
                if t['triggerTemplate']['repoName'] == self.repo
            ]

            if trigger:
                return trigger[0]

    def builds_for_commit(self):
        return self.find_builds((
            'source.repo_source.repo_name="{0}"'
            ' AND source_provenance.resolved_repo_source.commit_sha="{1}"'
            ).format(self.repo, self.sha))

    def find_builds(self, query):
        result = self.client.projects().builds().list(
            projectId=self.project,
            filter=query
        ).execute()

        if 'builds' in result:
            return result['builds']
        else:
            return []
