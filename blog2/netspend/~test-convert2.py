from pdf2csv.converter import convert

dfs = convert("example.pdf", output_dir="./output", output_format="csv")
for df in dfs:
    df.to_csv("output.csv", index=False)  # Save each DataFrame to a CSV
