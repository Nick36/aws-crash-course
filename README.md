# AWS Crash Course

A brief but comprehensive introduction into Amazon Web Services (AWS) with strong focus on the serverless services (S3, DynamoDB, Lambda and API Gateway) from a developer's perspective.

Includes a set of command-line interface (AWS CLI) excercises covering some of the most useful everyday operations.

## Supplementary Material

* `AWS Crash Course.pptx` -> introduction into AWS terminology and serverless services; command-line interface (AWS CLI) excercises
* rest of the `README` -> set up AWS CLI

## Set up AWS CLI

### Installation

#### Windows

[Install scoop](https://scoop.sh/)

```bash
scoop install aws
```

[Install Git Bash](https://gitforwindows.org/)

#### MAC

```bash
brew install awscli
```

#### [Instructions for other operating systems](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Configuration

To configure AWS CLI, create a text file `C:\Users\§USERNAME\.aws\config` (Windows) or `~/.aws/config` (Unix) with the following content:

```
[default]
region=us-east-1
AWS_ACCESS_KEY_ID=*****
AWS_SECRET_ACCESS_KEY=*****
```

All that you need for the AWS CLI exercises is a (temporary) AWS account with an account number, an `AWS_ACCESS_KEY_ID`, and an `AWS_SECRET_ACCESS_KEY`.
You can for instance [create an AWS free tier account](https://aws.amazon.com/free/) or [open a cloud sandbox with A Cloud Guru](https://learn.acloud.guru/cloud-playground/cloud-sandboxes).
A Cloud Guru sandbox comes with certain [limitations](https://help.pluralsight.com/help/aws-sandbox). 
For example, you can only use region us-east-1 or us-east-2.

### Useful Links

[AWS CLI reference](https://docs.aws.amazon.com/cli/latest/)

[AWS CloudShell with auto-completion](https://github.com/awslabs/aws-shell)

[AWS cheatsheets and more](https://blog.awsfundamentals.com/)
