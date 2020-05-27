from typing import Dict, Any

from the_plugins_namespace.plugin_api import PluginApi


class TheProjectPlugin(PluginApi):

    @property
    def name(self) -> str:
        return 'TheProjectPlugin'

    @property
    def description(self) -> str:
        return "The project's official plugin"

    def run(self, config: Dict[str, Any]) -> str:
        return 'ran the_project plugin'
