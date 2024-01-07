import pandas as pd
from tabulate import tabulate


def printDF(df, showIndex=False, headers='keys', logger=None):
    logger.write(tabulate(df, headers=headers, tablefmt='pretty', showindex=showIndex))


def printTitle(title, logger=None):
    logger.write(f"\n\n***** {title} *****\n")


def dataframe_EDA(table_name, dataframe, logger=None):
    printTitle(table_name, logger=logger)
    logger.write(dataframe.info)

    logger.write(f"\n\nNumber of Unique Items in {table_name}:")
    logger.write(dataframe.nunique())

    logger.write(f"\n\nNumber of Unique Items in Each column for table {table_name}:")
    logger.write(dataframe.apply(pd.unique))

    logger.write(f"\n\nTable: {table_name}")
    printDF(dataframe.head(), logger=logger)
    printDF(dataframe.tail(), logger=logger)
