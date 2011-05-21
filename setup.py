from setuptools import setup, find_packages
import sys, os

extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
        use_2to3_fixers=[]
    )

version = '1.1.0a2'

setup(
    name="holland",
    version=version,
    description="Holland Core Framework",
    long_description="""\
    This package provides the core functionality for
    performing backups along with a command line client interface.
    """,
    author="Rackspace",
    author_email="holland-discuss@lists.launchpad.net",
    url='http://www.hollandbackup.org',
    license="3-Clause BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=[
    ],
    entry_points="""
    # Scripts generated by setuptools
    [console_scripts]
    holland = holland.cli.main:holland

    # Holland backup plugins exposed by holland-core
    [holland.backup]
    noop            = holland.core.backup.plugin:NoopBackupPlugin
    backup-test     = holland.test:TestBackupPlugin

    [holland.stream]
    builtin         = holland.core.stream:StreamPlugin

    # Holland subcommands
    [holland.commands]
    help            = holland.cli.cmd:Help
    list-plugins    = holland.cli.cmd:ListPlugins
    list-commands   = holland.cli.cmd:ListCommands
    list-backups    = holland.cli.cmd:ListBackups
    backup          = holland.cli.cmd:Backup
    mk-config       = holland.cli.cmd:MakeConfig
    purge           = holland.cli.cmd:Purge

    [paste.paster_create_template]
    holland:backup  = holland.devtools:HollandBackupTemplate
    """,
    namespace_packages=[],
    **extra
)
