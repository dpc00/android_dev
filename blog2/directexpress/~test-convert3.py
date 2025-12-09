import pandas as pd
import tabula

# Convert tables from 'input.pdf' to a list of DataFrames
dfs = tabula.read_pdf("netspend-statement.pdf", pages="all", multiple_tables=True)
# Save each DataFrame to a separate sheet in an Excel file

print(dfs)
