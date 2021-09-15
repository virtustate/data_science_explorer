# this file populates endpoints in various dropdown lists
# rename to secret_endpoints.py and add your information
endpoints = {
    's3_aws': {'type': 's3', 'server': 's3.amazonaws.com', 'region':'us-west-2',
               'access_key': 'YOUR_ACCESS_KEY',
               'secret_key': 'YOUR_SECRET_KEY'},
    's3_minio': {'type': 's3', 'server': 'minio:9000', 'secure': False,
               'access_key': 'minioadmin',
               'secret_key':'minioadmin'},
}

