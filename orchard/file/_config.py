# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._yaml_file import YAMLFile

from ..module import Module, Argument, Exclusive


class ConfigFile(YAMLFile):
    # If fromfile is true then filedata is a filepath that we open. Else
    # filedata is a dictionary that contains the new ConfigFile's data and
    # we just use it directly
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

    def _build_config_dict(self, module, key):
        result = []
        for value in getattr(module, key):
            if isinstance(value, Argument):
                result.append({value.name: value.value})
            elif isinstance(value, Exclusive):
                exc_data = {'exclusive': []}
                for exc_arg in value.arguments:
                    exc_data['exclusive'].append({exc_arg.name: exc_arg.value})
                result.append(exc_data)
        return result

    # Gets the ConfigFile's data structure. This needs to be rebuilt every time
    # in case any of the values contained within their modules/arguments have
    # been updated
    def get_yaml(self):
        data = {'modules': []}
        for module in self.modules:
            module_data = {}

            module_data['name'] = module.name
            module_data['arguments'] = self._build_config_dict(module,
                                                               'arguments')
            if module.optionals:
                module_data['modules'] = self._build_config_dict(module,
                                                                 'optionals')
            data['modules'].append(module_data)

        return data
