import datetime
import os
from firebase_admin import storage
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
firebase_admin.initialize_app(cred, {
    'storageBucket': 'text-to-image-bot-657bb.appspot.com'
})


def upload_blob(source_file, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    # cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
    # firebase_admin.initialize_app(cred, {
    #     'storageBucket': 'text-to-image-bot-657bb.appspot.com'
    # })
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_file(source_file, if_generation_match=generation_match_precondition,
                          content_type='image/jpeg')
    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 60 minutes
        expiration=datetime.timedelta(minutes=60),
        # Allow GET requests using this URL.
        method="GET",
    )

    print(f"File {source_file} uploaded to {destination_blob_name}.")
    return url

if __name__ == '__main__':
    # default_app = firebase_admin.initialize_app()
    # print(default_app.project_id)

    # cred = credentials.Certificate(".." + GOOGLE_APPLICATION_CREDENTIALS)
    # firebase_admin.initialize_app(cred, {
    #     'storageBucket': 'text-to-image-bot-657bb.appspot.com'
    # })
    #
    # bucket = storage.bucket()
    # acl = bucket.acl
    # print(acl.all_authenticated())
    upload_blob("../requirements.txt", "requirements.txt")
