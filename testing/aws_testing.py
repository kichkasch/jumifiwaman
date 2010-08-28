import boto

BUCKET_ID = 'testing.kichkasch.de'

def createBucket(s3):
    bucket = s3.create_bucket(BUCKET_ID)  # bucket names must be unique
    return bucket

def getBucket(s3):
    bucket = s3.get_bucket(BUCKET_ID)
    return bucket
    
def uploadFile(bucket, remoteName, localFile, acl = 'public-read'):
    key = bucket.new_key(remoteName)
    key.set_contents_from_filename(localFile)
    key.set_acl(acl)

def downloadFile(bucket, remoteName, localFile):
    key = bucket.get_key(remoteName)
    key.get_contents_to_filename(localFile)

s3 = boto.connect_s3()

#bucket = createBucket(s3)
#uploadFile(bucket, 'examples/helloWorld', 'data.txt')

bucket = getBucket(s3)
downloadFile(bucket, 'examples/helloWorld', "copy.txt")
