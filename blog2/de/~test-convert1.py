# Import Module
import tabula

# Read PDF File
# this contain a list
# df = tabula.read_pdf(r"netspend-statement.pdf",pages="all")

tabula.convert_into(
    "netspend-statement.pdf", "netspend-statement.csv", pages="all", output_format="csv"
)
