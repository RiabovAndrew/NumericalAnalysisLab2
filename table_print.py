try:
    from prettytable import PrettyTable
except ModuleNotFoundError as mnfe:
    print(mnfe)
    exit()


DEBUG = False


class TablePrinter:  # Just a simple adapter for more convinient usage.
    def __init__(self, *columns):
        if len(columns) == 0:
            raise RuntimeError('No columns to add detected.')

        self.table = PrettyTable()
        for column in columns:
            if len(column) != len(columns[0]):
                raise RuntimeError('Sizes of columns are not equal.')
            self.table.add_column(column[0], column[1::])


    def print_table(self):
        print(self.table)


if __name__ == '__main__':  # Tests. TDD is cool!
    if not DEBUG:
        print('WARNING! This file is not intended to be main file. Consider running "main.py".')
        print('If you want to just test if it all works - change the "DEBUG" variable to True.')
        exit()
    else:
        print('Table printer tests:')
    table = TablePrinter(['First', 1, 2, 3, 4, 5], ['Second', 1, 4, 9, 16, 25])
    table.print_table()
