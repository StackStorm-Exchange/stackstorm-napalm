import difflib
import logging
import os
import re
import shutil
import tempfile

from lib.action import NapalmBaseAction

import git

# Suppressing the 'No handlers could be found for logger "st2.st2common.util.loader"' message
# that appears when including the TempRepo class, until I have a chance to troubleshoot why
# this is happening TODO(mierdin)
loaderlog = logging.getLogger('st2.st2common.util.loader')
loaderlog.setLevel(logging.DEBUG)
loaderlog.addHandler(logging.NullHandler())


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
            git.Repo.clone_from(repo, repo_path, branch='master')

            try:

                with open('%s/%s.txt' % (repo_path, device)) as config_file:
                    return "".join(config_file.readlines())

            except IOError:
                self.logger.error("Golden config not present in repo")
                raise

    def run(self, repository=None, **std_kwargs):

        if not self.config['config_repo'] and not repository:
            raise Exception("Golden configs repository not provided in args or config")
        else:
            # Use config if arg not provided
            if not repository:
                repository = self.config['config_repo']

        result = {
            "deviation": False,
            "diff_contents": ""
        }

        try:

            with self.get_driver(**std_kwargs) as device:

                # Get golden and actual configs
                golden_config = self.get_golden_config(repository, self.hostname)
                actual_config = device.get_config()['running']

                # Regular expressions for matching lines to ignore
                # Lot of network devices have lines like "last modified" that we don't
                # want to include in the diff
                #
                # In the future, this may be a configurable option, but we're doing
                # this statically for now.
                ignore_regexs = [
                    "## .*\n"
                ]
                for pattern in ignore_regexs:
                    actual_config = re.sub(pattern, "", actual_config)
                    golden_config = re.sub(pattern, "", golden_config)

                # Generate diff
                golden = golden_config.splitlines(1)
                actual = actual_config.splitlines(1)
                diff = difflib.unified_diff(golden, actual)
                diff = ''.join(diff)

                if diff:
                    result['deviation'] = True
                    result['diff_contents'] = ''.join(diff)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
