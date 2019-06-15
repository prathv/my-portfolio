import zipfile
import boto3
from io import BytesIO

def lambda_handler(event,context):
    try:
        sns = boto3.resource("sns")
        topic = sns.Topic("arn:aws:sns:us-west-2:356227741561:MyPortfolioTopic")
        s3 = boto3.client("s3")

        build_bucket = "portfoliobuild.prathveerrai.info"
        portfolio_bucket = "portfolio.prathveerrai.info"
        portfolio_zip = BytesIO()
        s3.download_fileobj(build_bucket,'portfoliobuild.zip',portfolio_zip)


        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm,"r")
                s3.upload_fileobj(obj,portfolio_bucket,nm)

        topic.publish(Subject="Portfolio Update Complete",Message="Hey Patty, completed deploying new updated portfolio")
        return "Completed Running new deployment"
    except:
        topic.publish(Subject="Portfolio Update Failed",Message="Hey Patty, failed deploying new updated portfolio")
