import html
import wikitextparser

from . import list_
from ..prototype import WikiTextHtml


def _render_table(instance: WikiTextHtml, table: wikitextparser.Table):
    content = ""
    if table.caption:
        content += "Table %s:\n" + table.caption
        
    for row in table.data():
        content += "%s\n" % "|".join(row)

    index = instance.store_snippet(content)
    table.string = "{{" + f"__snippet|wikilink|{index}|table" + "}}"


def replace(instance: WikiTextHtml, wikitext: wikitextparser.WikiText):
    for table in reversed(wikitext.get_tables(recursive=True)):
        # Resolve all lists inside the table next
        list_.replace(instance, table)

        # Now render the table and replace it with a marker
        _render_table(instance, table)
