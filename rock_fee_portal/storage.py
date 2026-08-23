from storages.backends.s3 import S3Storage


class SupabaseStorage(S3Storage):
    location = "payment_proofs"
    file_overwrite = False
    default_acl = None
    signature_version = "s3v4"
