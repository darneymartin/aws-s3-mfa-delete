# aws-s3-mfa-delete
A Python script used to enable MFA Delete on S3 Buckets. This script provides an easier way of enabiling MFA Delete option by wrapping the boto3 module and using a much simpler API.

## Setup
Follow the steps to install all of the requirements.

* git clone https://github.com/darneymartin/aws-s3-mfa-delete.git
* cd aws-s3-mfa-delete
* pip3 install -r requirements.txt
## Usage
* `python3 mfa-delete.py --enable --bucket your_s3_bucket` - Enable MFA Delete on the specified S3 Bucket
* `python3 mfa-delete.py --disable --bucket your_s3_bucket` - Disable MFA Delete on the specified S3 Bucket
* `python3 mfa-delete.py --enable` - Loop through all buckets in account and enable MFA Delete

## Options
* --enable  : Option to Enable MFA Delete 
* --disable : Option to Disable MFA Delete
* --profile : AWS Profile to use, the default is the `default` profile
* --force   : Do not prompt user to ask if they want to perform the action.
* --bucket  : Specify the bucket to apply the settings too
* --verbose : Option to give verbose output
## Requirements
Python 3
boto3
awscli