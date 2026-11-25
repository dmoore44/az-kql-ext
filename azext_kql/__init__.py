from azure.cli.core import AzCommandsLoader

from azext_kql._help import helps  # noqa: F401  # pylint: disable=unused-import


class KqlCommandsLoader(AzCommandsLoader):
    """Command loader for the az kql extension."""

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType

        custom_type = CliCommandType(operations_tmpl='azext_kql.custom#{}')
        super().__init__(cli_ctx=cli_ctx, custom_command_type=custom_type)

    def load_command_table(self, args):
        from azext_kql.commands import load_command_table

        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_kql._params import load_arguments

        load_arguments(self, command)


COMMAND_LOADER_CLS = KqlCommandsLoader
