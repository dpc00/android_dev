from pdf2csv.converter import convert

pdf_path = "netspend-statement.pdf"
output_dir = r"C:\Users\dpchitester\Downloads"
rtl = True
output_format = "xlsx"

dfs = convert(pdf_path, output_dir=output_dir, rtl=rtl, output_format=output_format)
for df in dfs:
    print(df)
