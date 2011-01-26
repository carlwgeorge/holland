"""Plugin manager API"""

import logging
import pkg_resources
from holland.core.plugin.error import PluginError, PluginLoadError, \
                                      PluginNotFoundError

LOG = logging.getLogger(__name__)

class AbstractPluginManager(object):
    """Interface that PluginManager implementations should follow"""

    def load(self, group, name):
        """Load a plugin for the given name"""
        raise NotImplementedError()

    def iterate(self, group, name):
        """Iterate over plugins for the given name"""
        raise NotImplementedError()

class EntrypointPluginManager(AbstractPluginManager):
    """Plugin manager that uses setuptools entrypoints"""

    def load(self, group, name):
        """Load a plugin via a setuptools entrypoint for the given name

        Name must be in the format group.name
        """
        # XXX: Handle various pkg_resources exceptions more gracefully
        # These typically give no information about what was going on froma
        # str(exc) alone:
        # DistributionNotFoundError - A requested distribution was not found
        # VersionConflict - An already-installed version conflicts with the
        #                   requested version
        # These are raised when an entrypoint has declared dependencies
        for plugin in pkg_resources.iter_entry_points(group, name):
            try:
                return plugin.load()
            except (SystemExit, KeyboardInterrupt):
                raise
            except pkg_resources.DistributionNotFound, exc:
                raise EntrypointDependencyError(group, name,
                                                entrypoint=plugin,
                                                req=exc.args[0])
            except pkg_resources.VersionConflict, exc:
                raise EntrypointVersionConflictError(entrypoint=plugin,
                                                     *exc.args)
            except Exception, exc:
                LOG.exception("Exception when loading plugin")
                raise PluginLoadError(group, name, exc)
        raise PluginNotFoundError(group, name)

    def iterate(self, group):
        """Iterate over an entrypoint group and yield the loaded entrypoint
        object
        """
        for plugin in pkg_resources.iter_entry_points(group):
            try:
                yield plugin.load()
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                LOG.error("Failed to load plugin %r from group %s",
                          plugin, group, exc_info=True)

# specific to entrypoint plugins
class EntrypointDependencyError(PluginError):
    """An entrypoint or its python egg distribution requires some dependency
    that could not be found by setuptools/pkg_resources

    :attr entrypoint:  entrypoint that causes this error
    :attr req: requirement that could not be found
    """

    def __init__(self, group, name, entrypoint, req):
        self.group = group
        self.name = name
        self.entrypoint = entrypoint
        self.req = req

    def __str__(self):
        return "Could not find dependency '%s' for plugin %s in group %s" % \
               (req, name, group)

class EntrypointVersionConflictError(PluginError):
    def __init__(self, group, name, entrypoint, dist, req):
        self.group = group
        self.name = name
        self.ep = entrypoint
        self.dist = dist
        self.req = req

    def __str__(self):
        # XXX: this error message could be improved.
        return "Version Conflict. Requested %s Found %s" % (req, dist)