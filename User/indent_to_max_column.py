import sublime, sublime_plugin


class IndentToMaxColumnCommand(sublime_plugin.TextCommand):
    """
    Plugin to indent all selections to the same column. Optionally
    aligns the right columns of selections if the run() method's justify
    argument is 'right', otherwise selections are left-justified.

    If there are multiple selections on each line, only the first selection
    for that line is indented and later ones are ignored.
    """


    def __init__(self, *args):
        super().__init__(*args)
        self.__row_sort = lambda regioncol: regioncol[0].begin()


    def lines_to_columns(self, selections, right = False):
        """
        Maps each line to its region and column, respectively. Essentially
        returns a dictionary of { line => (region, column), ... }.
        """

        view = self.view
        rows = {}

        for sel in selections:
            sel_end = sel.end() if right else sel.begin()
            rowcol = view.rowcol(sel_end)

            if rowcol[0] in rows:
                if not right and rows[rowcol[0]][1] < rowcol[1]:
                    continue
                elif right and rows[rowcol[0]][1] >= rowcol[1]:
                    continue

            rows[rowcol[0]] = (sel, rowcol[1])

        return rows


    def max_column(self, selections, rows = None):
        """
        Returns the max column for the given selections. If there's already a
        result from lines_to_columns, it may be passed in as the rows argument,
        otherwise it will be computed as needed.
        """

        if rows is None:
            rows = self.lines_to_columns(selections)

        return max(col for sel, col in rows.values())


    def justify_lines(self, edit, aligned_column, rows = None, right = False):
        """
        Indents all selected lines to the given aligned_column. If a result
        from lines_to_columns has already been computed, it may be passed as
        the rows argument, otherwise it will be computed on demand.
        """

        view = self.view

        if rows is None:
            rows = self.lines_to_columns(selections, right = right)

        rowvals = sorted(rows.values(), key = self.__row_sort, reverse = True)

        for region, column in rowvals:
            if column < aligned_column:
                indent = " " * (aligned_column - column)
                view.insert(edit, region.begin(), indent)


    def trim_whitespace_from_region(self, region):
        new_region = None

        view = self.view

        if region.empty():
            new_region = view.word(region)
        else:
            new_region = sublime.Region(region.begin(), region.end())

        while view.substr(new_region.a) == ' ' or view.substr(new_region.a) == '\t':
            new_region.a += 1

        while view.substr(new_region.b) == ' ' or view.substr(new_region.b) == '\t':
            new_region.b -= 1

        if region.a > region.b:
            temp = new_region.a
            new_region.a = new_region.b
            new_region.b = temp

        return new_region


    def filter_whitespace(self, regions):
        filtered = []
        return list(self.trim_whitespace_from_region(region) for region in regions)


    def run(self, edit, justify = None, strip_whitespace = True):
        """
        When run, all selections are indented by spaces to the max column of
        all selected regions' starting points.
        """

        if justify is None:
            justify = 'left'

        view = self.view
        selections = view.sel()
        split_regions = []

        for region in selections:
            split_regions += view.split_by_newlines(region)

        if strip_whitespace:
            split_regions = self.filter_whitespace(split_regions)

        # terminate early if possible
        if len(split_regions) < 2:
            return

        rows = self.lines_to_columns(split_regions, right = justify == 'right')

        aligned_column = self.max_column(split_regions, rows = rows)
        self.justify_lines(edit, aligned_column, rows = rows)


    def description(self):
        return (
            """Indents all selections to the collective max column using """
            """spaces. Does not attempt to align specific character """
            """sequences. This is not intelligent indentation. Takes a """
            """`justification' argument -- if 'right', will right-justify """
            """selections to the right, otherwise text is left-justified.""")
