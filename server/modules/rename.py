from .moduleimpl import ModuleImpl
import json

s_map = [',', ';', '\t', '\n']

def parse_list(wf_module, table):
    list_string = wf_module.get_param_string('list_string')
    if not list_string:
        return table

    table_width = len(table.columns)
    separator_counts = [list_string.count(x) for x in s_map]

    if sum(separator_counts) == 0:
        return (table, 'Separator between names not detected.')

    separator = s_map[separator_counts.index(max(separator_counts))]
    # Strip values and remove null values
    new_columns = [x.strip() for x in list_string.split(separator) if x.strip()]

    if table_width < len(new_columns):
        return (table, f"Length of input list ({len(new_columns)}) does not match width of table ({table_width}).")
    elif table_width > len(new_columns):
        new_columns = fill_column_names(new_columns, table_width)

    try:
        table.columns = new_columns
        return table
    except Exception as e:
        return(table, str(e.args[0]))

def fill_column_names(column_names, expected_length):
    start = len(column_names) + 1
    for x in range(start, expected_length + 1):
        proposed_name = f'Column {x}'
        proposed_name_prefix = proposed_name
        num_attempt = 1
        while proposed_name in column_names:
            proposed_name = f'{proposed_name_prefix}_{num_attempt}'
            num_attempt += 1
        column_names.append(proposed_name)
    return column_names

class RenameFromTable(ModuleImpl):
    # Rename entry structure: Dictionary of {old_name: new_name}
    @staticmethod
    def render(wf_module, table):
        custom_list = wf_module.get_param_checkbox('custom_list')
        if not custom_list:
            entries_json = wf_module.get_param_raw('rename-entries', 'custom')
            entries = {}
            try:
                entries = json.loads(entries_json)
            except:
                return table

            og_columns = table.columns.tolist()
            new_columns = [entries.get(col, col) for col in og_columns]
            table.columns = new_columns
            return table
        else:
            return parse_list(wf_module, table)
