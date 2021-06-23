## S3 event notification 

This experiment is about configuring S3 event notification to trigger Lambda and send a message to email through SNS in Lambda, by Cloudformation. The purpose of this experiment is
1. To get comfortable with the syntax of Cloudformation, python and bash
2. To acquire knowledge about Cloudformation requirements
3. To get comfortable with IaC 

### Prerequisite
1. AWS cli
2. Python and pip
3. AWS account and user
4. Change your bucket name, email address, iam user from `example.yml` and the bucket name from `example.py`

### How to run the project
1. give execution permission and run bash script `deploy.sh`
``` bash
$ chmod +x deploy.sh kill.sh
$ ./deploy.sh
```

2. Accept AWS SNS notification permission from your email, check your junk mail as well

3. Run `example.py` to push a simple zip file into s3 bucket 
``` python
$ python example.py
```

4. to kill the stack, make sure your s3 bucket is empty, then run the script below:
``` bash
$ ./kill.sh
```