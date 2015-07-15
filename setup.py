from setuptools import setup

from teamspeaknotifier import get_version

setup(
    name='teamspeaknotifier',
    version=get_version(),
    url='https://bitbucket.org/latestrevision/teamspeak-notification/',
    description='Show unobtrusive notifications when certain things happen in teamspeak.',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
    ],
    packages=['teamspeaknotifier',],
    entry_points={'console_scripts': [
        'teamspeak-notifier = teamspeaknotifier:run_from_cmdline']},
    install_requires = [
            'teamspeak3>=1.3',
        ]
)

# from setuptools import setup

# APP = ['teamspeaknotifier/notifier.py']
# DATA_FILES = []
# OPTIONS = {
#     'argv_emulation': True,
#     'plist': {
#         'LSUIElement': True,
#     },
#     'packages': ['rumps'],
# }

# setup(
#     app=APP,
#     version=get_version(),
#     data_files=DATA_FILES,
#     options={'py2app': OPTIONS},
#     setup_requires=['py2app','teamspeak3>=1.3'],
# )
