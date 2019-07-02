import zipfile
import boto3
from io import BytesIO


def lambda_handler(event,context):
    location = {"bucketName":"portfoliobuild.prathveerrai.info","objectKey":"portfoliobuild.zip"}
    print(location)
    sns = boto3.resource("sns")
    topic = sns.Topic("arn:aws:sns:us-west-2:356227741561:MyPortfolioTopic")
    try:
        job = event.get("CodePipeline.job")
        if job:
            for artifact in job['data']['inputArtifacts']:
                if artifact['name'] == "BuildArtifact":
                    location = artifact["location"]["s3Location"]
        print("Build portfolio from "+location["bucketName"])
        s3 = boto3.client("s3")
        build_bucket = location["bucketName"]
        portfolio_bucket = "portfolio.prathveerrai.info"
        portfolio_zip = BytesIO()
        s3.Bucket(build_bucket).download_file("portfoliobuild.zip", "portfoliobuild.zip")


        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm,"r")
                s3.upload_fileobj(obj,portfolio_bucket,nm)

        topic.publish(Subject="Portfolio Update Complete",Message="Hey Patty, completed deploying new updated portfolio")
        return "Completed Running new deployment"

        if job:
            codepipeline = boto3.client("codepipeline")
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio Update Failed",Message="Hey Patty, failed deploying new updated portfolio")
        raise
