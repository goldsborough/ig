'''Handles searching for the WWW path and copying operations.'''

import logging
import os
import shutil
import tempfile

log = logging.getLogger(__name__)


WWW = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                   os.pardir,
                   'www')

if not os.path.exists(WWW):
    message = 'Could not find www directory for ig: {0}'
    raise EnvironmentError(message.format(WWW))


def create_directory(directory):
    if directory is None:
        directory = tempfile.mkdtemp(prefix='ig-')
        log.debug('Created temporary directory %s', directory)

    if os.path.exists(directory):
        shutil.rmtree(directory)

    shutil.copytree(WWW, directory)

    log.debug('Copied contents of www folder to %s', directory)

    return directory
