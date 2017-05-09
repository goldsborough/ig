"""Version-bumping script."""

from __future__ import print_function

import os.path
import re

def bump(match):
    """Bumps the version"""
    before, old_version, after = match.groups()
    major, minor, patch = map(int, old_version.split('.'))
    patch += 1
    if patch == 10:
        patch = 0
        minor += 1
        if minor == 10:
            minor = 0
            major += 1
    new_version = '{0}.{1}.{2}'.format(major, minor, patch)

    print('{0} => {1}'.format(old_version, new_version))

    return before + new_version + after


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project = os.path.split(root)[-1]
    init_path = os.path.join(root, project, '__init__.py')
    with open(init_path) as source:
        original = source.read()
    pattern = re.compile(r'^(\s*__version__\s*=\s*[\'"])([^\'"]*)([\'"])', re.M)
    replaced = re.sub(pattern, bump, original)
    if replaced == original:
        raise RuntimeError('Could not find version!')
    with open(init_path, 'w') as destination:
        destination.write(replaced)


if __name__ == '__main__':
    main()
