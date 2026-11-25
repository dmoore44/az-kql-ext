from azure.cli.core.commands import CliCommandType

kql_custom = CliCommandType(operations_tmpl='azext_kql.custom#{}')


def load_command_table(self, _):
    with self.command_group('kql', kql_custom) as g:
        g.custom_command('query', 'kql_query')
