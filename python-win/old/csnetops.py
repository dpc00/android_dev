import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file /sdcard/token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive"]
service = None


def uploadFile(fid, sd, td, tcfc):
    try:
        file_metadata = {
            "id": None,
            "name": str(td),
            "mimeType": None,
            "parents": ["root"],
        }
        media = MediaFileUpload(
            str(sd), mimetype=None, chunksize=1 << 20, resumable=True
        )
        file = (
            service.files()
            .create(
                body=file_metadata, media_body=media, fields="Id, ModTime, Size, Hashes"
            )
            .execute()
        )
        print("File ID: " + file.get("id"))
        tcfc[0] += 1
        return 0
    except Exception as e:
        print(e)
        tcfc[1] += 1
        return 1


def init():
    global service
    creds = None
    if os.path.exists("/sdcard/token.pickle"):
        with open("/sdcard/token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets2.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("/sdcard/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("drive", "v3", credentials=creds)
    return service


def getChanges():
    ch = init().changes()
    print(ch, dir(ch))
    ptrr = ch.getStartPageToken().execute()
    print(ptrr, dir(ptrr))
    pt = int(ptrr["startPageToken"])
    for i in range(pt, 78800, -10):
        print(pt)
        resr = ch.list(pageSize=100, pageToken=i).execute()
        # print('resr',resr)
        items = resr["changes"]
        fid = None
        if not items:
            print("No changes found.")
        else:
            print("Changes:")
            for item in items:
                print(" ", item["file"]["name"])
        pt -= 1


if __name__ == "__main__":
    from pathlib import Path

    f1 = Path("/sdcard/Videos").glob()[0]
    print(f1)
    uploadFile(f1, f1.relative_to("/sdcard"))
