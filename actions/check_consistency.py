import difflib
import os
import shutil
import tempfile

from lib.action import NapalmBaseAction

import git


class TempRepo(object):
    def __enter__(self):
        self.name = tempfile.mkdtemp()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.name)


class NapalmCheckConsistency(NapalmBaseAction):
    """Check that the device's configuration is consistent with the 'golden' config in a Git repository
    """

    def get_golden_config(self, repo, device):

        with TempRepo() as tmpdir:
            repo_path = os.path.join(tmpdir, 'repo')
            repo = git.Repo.clone_from(repo, repo_path, branch='master')
            with open('%s/%s.txt' % (repo_path, device)) as config_file:
                return "".join(config_file.readlines())


    def run(self, repository, **std_kwargs):

        result = {
            "deviation": False,
            "diff_contents": ""
        }

        try:

            with self.get_driver(**std_kwargs) as device:

                # Get golden and actual configs
                golden_config = self.get_golden_config(repository, self.hostname)
                actual_config = device.get_config()['running']

                # Generate diff
                golden=golden_config.splitlines(1)
                actual=actual_config.splitlines(1)
                diff=difflib.unified_diff(golden, actual)

                if diff:
                    result['deviation'] = True
                    result['diff_contents'] = ''.join(diff)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
