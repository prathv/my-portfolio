import zipfile
import boto3
from io import BytesIO

s3 = boto3.client("s3")

build_bucket = "portfoliobuild.prathveerrai.info"
portfolio_bucket = "portfolio.prathveerrai.info"
portfolio_zip = BytesIO()
s3.download_fileobj(build_bucket,'portfoliobuild.zip',portfolio_zip)


with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm,"r")
        s3.upload_fileobj(obj,portfolio_bucket,nm)

