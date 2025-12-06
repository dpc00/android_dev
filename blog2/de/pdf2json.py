# makes json files from pdfs using veryfi
# this program charges $500 a month

import json

from veryfi import Client

import fngen

# from veryfi.bank_statements import BankStatements


"""

https://api.veryfi.com/

client id: vrffvtvV2vWdrl28tUTvyvYyoE7PmJ42Kf6GpwD
client secret: BHaFTVinssg2iv1lzsbl3KIirlbmlAktf74t0fc7DSTiPgwonvVyF2dZyewVFE4ogsEYBd21W2Mr9HgZZ0GeheBuNrca57ORMnAdyTbTsDcXougp9Pk4EZCgU8YyYiCs
user name: donaldchitester
api key: c87c42191b219e8a05b2a65300def1ac
"""


client_id = "vrffvtvV2vWdrl28tUTvyvYyoE7PmJ42Kf6GpwD"
client_secret = "BHaFTVinssg2iv1lzsbl3KIirlbmlAktf74t0fc7DSTiPgwonvVyF2dZyewVFE4ogsEYBd21W2Mr9HgZZ0GeheBuNrca57ORMnAdyTbTsDcXougp9Pk4EZCgU8YyYiCs"
username = "donaldchitester"
api_key = "c87c42191b219e8a05b2a65300def1ac"

veryfi_client = Client(client_id, client_secret, username, api_key)

print(veryfi_client)

categories = ["account statement"]

bs = veryfi_client
# print(bs)

e1 = ".pdf"
e2 = ".json"

fngen.clear()
fngen.init(e2)

while fngen.hasnext():
    fn = fngen.next()

    file_path = fn + e1  # or a URL
    json_path = fn + e2

    response = bs.process_bank_statement_document(file_path)

    with open(json_path, "wt") as f:
        json.dump(response, f, indent=4)
