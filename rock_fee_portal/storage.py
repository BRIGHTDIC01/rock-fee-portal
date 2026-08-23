from storages.backends.s3 import S3Storage


class SupabaseStorage(S3Storage):
    # Keep the storage root at the bucket root.
    # Payment.upload_to already supplies the single "payment_proofs/" folder.
    location = ""
    file_overwrite = False
    default_acl = None
    querystring_auth = True
    signature_version = "s3v4"
