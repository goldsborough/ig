import os

WWW = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                   os.pardir,
                   'www')

if not os.path.exists(WWW):
    message = 'Could not find www directory for ig: {0}'
    raise EnvironmentError(message.format(WWW))
