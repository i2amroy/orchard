# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._yaml_file import YAMLFile

from ..module import Module


class ConfigFile(YAMLFile):

    def __init__(self, filedata, fromfile):
        if fromfile:
            super().__init__(filedata)
        else:
            self.data = filedata
            modules = self.data.get('modules')
            if modules:
                self.modules = []
                self._add_modules(modules)

    # Nothing fancy here, just add our module to self.modules
    def _add_modules(self, modules):
        for module in modules:
            self.modules.append(Module(module))
