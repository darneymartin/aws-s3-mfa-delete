#!/usr/bin/env python3

import boto3
import argparse
from botocore.exceptions import ClientError

###########################################################
#
# name: "main"
# type: "Function"
# description: main entry point function.
#
###########################################################
def main(arguments):
    session = boto3.Session(profile_name=arguments.profile)
    s3 = session.client('s3')
    iam = session.client('iam')
    device = iam.list_mfa_devices()["MFADevices"][0]["SerialNumber"]

    buckets = []
    if arguments.bucket is None:
        buckets = list_buckets(s3)
    else:
        buckets.append(arguments.bucket)

    for bucket in buckets:
        if arguments.enable:
            enable(s3, bucket, arguments.force, device)
        elif arguments.disable:
            disable(s3, bucket, arguments.force, device)
        else:
            print("error: please specify --enable or --disable")


###########################################################
#
# name: "prompt"
# type: "Function"
# description: Function used to get an MFA Token from 
#               the user.
#
###########################################################
def prompt():
    otp = None
    while not (otp and otp.isdigit()):
        otp = input(f'\nEnter six digit OTP: ')
    return otp



###########################################################
#
# name: "enable"
# type: "Function"
# description: Function used to enable MFA Delete on an
#               S3 Bucket.
#
###########################################################
def enable(client, bucket, force, device):
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError as e:
        if int(e.response['Error']['Code']) == 404:
            print('error: Bucket {:s} does not exist'.format(bucket))
            exit()

    if force is False:
        answer = input("Do you want to Enable MFA Delete on {:s}?: (y/n) ".format(bucket))
        if(answer == "y"):
            force = True
        elif(answer == "n"):
            print("info: MFA Delete was not enabled for Bucket {:s}".format(bucket))
            return()
        else:
            print("error: Incorrect value received")
            exit()
        
    token = prompt()
    try:
        print("info: Enabling MFA Delete on Bucket {:s}".format(bucket))
        client.put_bucket_versioning(Bucket = bucket,
                            MFA = "{:s} {:s}".format(device, token),
                            VersioningConfiguration = {
                                'MFADelete' : 'Enabled',
                                'Status' : 'Enabled'
                            }
                        )
    except ClientError as e:
        print(e)
        exit()

    print("info: MFA Delete Enabled on Bucket {:s}".format(bucket))
    return()

###########################################################
#
# name: "disable"
# type: "Function"
# description: Function used to disable MFA Delete on an
#               S3 Bucket.
#
###########################################################
def disable(client, bucket, force, device):
    try:
        client.meta.client.head_bucket(Bucket=bucket)
    except ClientError as e:
        if int(e.response['Error']['Code']) == 404:
            print('error: Bucket {:s} does not exist'.format(bucket))
            exit()

    if force is False:
        answer = input("Do you want to Disable MFA Delete on {:s}?: (y/n) ".format(bucket))
        if(answer == "y"):
            force = True
        elif(answer == "n"):
            print("info: MFA Delete was not disabled for Bucket {:s}".format(bucket))
            return()
        else:
            print("error: Incorrect value received")
            exit(1)
        
    token = prompt()
    try:
        print("info: Disabling MFA Delete on Bucket {:s}".format(bucket))
        client.put_bucket_versioning(Bucket = bucket,
                            MFA = "{:s} {:s}".format(device, token),
                            VersioningConfiguration = {
                                            'MFADelete' : 'Disabled',
                                            'Status' : 'Suspended'
                                            }
                        )
    except ClientError as e:
        print(e)
        exit(1)

    print("info: MFA Delete Disabled on Bucket {:s}".format(bucket))
    return()

#################################################
#
# type: Function
# description: Get List of S3 Bucket Names
#
#################################################
def list_buckets(client):
    response = client.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        buckets.append(bucket['Name'])
    return buckets

def request_mfa():
    pass

################################################################################
#
# This is the start of the program
#
################################################################################
if __name__ == '__main__':
    try:
        args = argparse.ArgumentParser(description="""ARG_HELP""", formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        
        args.add_argument('--profile','-p', dest='profile', type=str, default="default", help="Profile to use (Default: default)")
        args.add_argument('--force','-f', dest='force', action='store_true', default=False, help="Doesn't prompt users for input for bucket")
        args.add_argument('--disable','-d', dest='disable', action='store_true', default=False, help="Specify to Disable MFA Delete")
        args.add_argument('--enable','-e', dest='enable', action='store_true',default=False, help="Specify to Enable MFA Delete")
        args.add_argument('--bucket','-b', dest='bucket', type=str, help="Specify Bucket to Enable MFA Delete on")
        args.add_argument('--verbose','-v', dest='verbose', action='store_true', default=False, help="Show verbose output of program")
        args = args.parse_args()
        # Launch Main
        main(args)
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(1)
    exit(0)