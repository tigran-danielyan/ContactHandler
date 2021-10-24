from storages.backends.s3boto3 import S3Boto3Storage

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media')


def upload_to_aws_folder(path, file) -> str:
    """
    takes the path of the file (within s3 bucket) and stores file in S3 returns file url
    path: full S3 directory where the file should be stored
    file: file object opened in rb mode
    return: s3 url of the file
    """

    storage = MediaRootS3BotoStorage()
    storage.save(path, file)

    return storage.url(path)
