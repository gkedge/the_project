from typing import Dict, Any

from the_plugins_namespace.plugin_api import PluginApi


class ExamplePlugin(PluginApi):

    @property
    def name(self) -> str:
        return 'ExamplePlugin'

    @property
    def description(self) -> str:
        return 'A plugin that provides an example of the plugin_api'

    def run(self, config: Dict[str, Any]) -> str:
        return 'ran example'
