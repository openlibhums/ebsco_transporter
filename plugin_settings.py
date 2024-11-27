from utils import plugins

PLUGIN_NAME = 'EBSCO Transporter Plugin'
DISPLAY_NAME = 'EBSCO Transporter'
DESCRIPTION = 'FTP transporter for EBSCO.'
AUTHOR = 'Andy Byers'
VERSION = '0.1'
SHORT_NAME = 'ebsco_transporter'
MANAGER_URL = 'ebsco_transporter_manager'
JANEWAY_VERSION = "1.7"


class EBSCOTransporterPlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = DISPLAY_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL

    version = VERSION
    janeway_version = JANEWAY_VERSION


def install():
    EBSCOTransporterPlugin.install()


def hook_registry():
    EBSCOTransporterPlugin.hook_registry()


def register_for_events():
    pass
