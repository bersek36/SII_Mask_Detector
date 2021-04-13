from __future__ import print_function
import os
import io

from apiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import httplib2

import auth


SCOPES = os.environ["SCOPES"]
CLIENT_SECRET_FILE = os.environ["CLIENT_SECRET_FILE"]
APPLICATION_NAME = os.environ["APPLICATION_NAME"]
VERSION_API = os.environ["VERSION_API"]
SERVICE = os.environ["SERVICE"]

authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build(SERVICE, VERSION_API, http=http)


def listFiles(size):
    results = (
        drive_service.files()
        .list(pageSize=size, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))


def uploadFile(filename, filepath, mimetype):
    file_metadata = {"name": filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)

    file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    print("File ID: %s" % file.get("id"))


def downloadFile(file_id, filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    with io.open(filepath, "wb") as f:
        fh.seek(0)
        f.write(fh.read())


def createFolder(name):
    file_metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    file = drive_service.files().create(body=file_metadata, fields="id").execute()
    print("Folder ID: %s" % file.get("id"))


def searchFile(size, query):
    results = (
        drive_service.files()
        .list(
            pageSize=size,
            fields="nextPageToken, files(id, name, kind, mimeType)",
            q=query,
        )
        .execute()
    )

    items = results.get("files", [])

    if not items:
        print("No files found.")
    else:
        print("Files:")

        for item in items:
            print(item)
            print("{0} ({1})".format(item["name"], item["id"]))


file_ids = [
    os.environ["TRIPLET_ID"],
    os.environ["ARIALBD_ID"],
    os.environ["CHECK_POINT_ID"],
]
file_names = [
    os.environ["TRIPLET_NAME"],
    os.environ["ARIALBD_NAME"],
    os.environ["CHECK_POINT_NAME"],
]

for file_id, file_name in zip(file_ids, file_names):
    path = f"../model/{file_name}"
    downloadFile(file_id, path)
# uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
# downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
# createFolder('Google')
searchFile(10, "name contains 'Getting'")
