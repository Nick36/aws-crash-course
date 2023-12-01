# AWS Crash Course

A brief but comprehensive introduction into Amazon Web Services (AWS) with strong focus on the serverless services (S3, DynamoDB, Lambda and API Gateway) from a developer's perspective.

## Supplementary Material

* `AWS Crash Course.pptx` -> introduction into AWS terminology and serverless services; command-line interface (AWS CLI) excercises
* `AWS Crash Course with Solutions.pptx` -> same as above with sample solutions of the excercises
* subfolders -> files from the sample solutions
* rest of the `README` -> a concise recap of the AWS CLI excercises and their sample solutions.

## AWS CLI exercises

In this section, you will find a set of command-line interface (AWS CLI) excercises with sample solutions.
They are covering some of the most useful everyday operations related to the serverless services S3, DynamoDB, Lambda and API Gateway.

### Set up AWS CLI

#### Installation

##### Windows

[Install scoop](https://scoop.sh/)

```bash
scoop install aws
```

##### MAC

```bash
brew install awscli
```

##### [Instructions for other operating systems](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

#### Configuration

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

#### Useful Links

[AWS CLI reference](https://docs.aws.amazon.com/cli/latest/)

[AWS CloudShell with auto-completion](https://github.com/awslabs/aws-shell)

[AWS cheatsheets and more](https://blog.awsfundamentals.com/)

### S3

Crete bucket s3-exercise-*****.

*The bucket name must be globally unique. A good way to find a unique name is to append some numbers.*

```bash
aws s3 mb s3://s3-exercise-464829
```

List all S3 buckets in your account.

```bash
aws s3 ls
```

Create files cv.txt, cv.pdf and cv.log and save them to the exercise bucket under /application.

*Three different ways to put a file into an exercise bucket are shown.*

```bash
aws s3 mv cv.txt s3://s3-exercise-464829/application/cv.txt
aws s3 cp cv.pdf s3://s3-exercise-464829/application/cv.pdf
echo "log entry" | aws s3 cp - s3://s3-exercise-464829/application/cv.log
```

List bucket contents.

```bash
aws s3 ls s3://s3-exercise-464829
```

Synchronise bucket contents with your local directory.

```bash
aws s3 sync . s3://s3-exercise-464829/application
```

Delete all non-text files from your bucket.

```bash
aws s3 sync . s3://s3-exercise-464829 --delete --exclude "*.txt" 
```

Delete all files under the /application prefix from your bucket.

```bash
aws s3 rm s3 ://s3-exercise-464829/application --recursive
```

Delete the exercise bucket.

*Only an empty bucket may be deleted, unless the --force option is specified.*

```bash
aws s3 rb s3://s3-exercise-464829 --force
```

### DynamoDB

Create table Music with partition key Artist and sort key SongTitle.

```bash
aws dynamodb create-table \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
```

List all tables.

```bash
aws dynamodb list-tables
```

Add a global secondary index AlbumIndex with hash attribute AlbumTitle to the table.

*If you are adding a new global secondary index to the table, AttributeDefinitions must include the key element(s) of the new index.
Primary key attributes and index key attributes are automatically projected.*

```bash
aws dynamodb update-table \
    --table-name Music \
    --attribute-definitions AttributeName=AlbumTitle,AttributeType=S \
    --global-secondary-index-updates "[
            {
                \"Create\": {
                    \"IndexName\": \"AlbumIndex\",
                    \"KeySchema\": [{\"AttributeName\":\"AlbumTitle\",\"KeyType\":\"HASH\"}],
                    \"Projection\":{
                        \"ProjectionType\":\"KEYS_ONLY\"
                    },
                    \"ProvisionedThroughput\": {
                        \"ReadCapacityUnits\": 1,
                        \"WriteCapacityUnits\": 1
                    }
                }
            }
        ]"
```

Describe the table.

```bash
aws dynamodb describe-table --table-name Music
```

Put at least two items into the table.

```bash
aws dynamodb put-item \
    --table-name Music \
    --item '{
        "Artist": {"S": "Led Zeppelin"},
        "SongTitle": {"S": "Black Dog"} }' \
    --return-consumed-capacity TOTAL


aws dynamodb put-item \
    --table-name Music \
    --item '{
        "Artist": {"S": "Led Zeppelin"},
        "SongTitle": {"S": "Ramble On"},
        "AlbumTitle": {"S": "Led Zeppelin II"} }' \
    --return-consumed-capacity TOTAL
```

Update the album title of an item.

```bash
aws dynamodb update-item \
    --table-name Music \
    --key '{ "Artist": { "S": "Led Zeppelin" }, "SongTitle": { "S": "Black Dog" } }' \
    --update-expression "SET AlbumTitle = :val" \
    --expression-attribute-values '{ ":val": { "S": "Led Zeppelin IV" } }'
```

Get an item by key.

```bash
aws dynamodb get-item \
    --table-name Music \
    --key '{ "Artist": { "S": "Led Zeppelin" }, "SongTitle": { "S": "Black Dog" } }'
```

Query the table by artist.

*Nota bene: Always use a query instead of a scan with a filter expression! 
The scan command is not only slow but also costly, as you will be charged for every scanned item. 
If you perform a query instead, you will only be charged for the matched results.*

```bash
aws dynamodb query \
    --table-name Music \
    --key-condition-expression "Artist = :val" \
    --expression-attribute-values '{ ":val": { "S": "Led Zeppelin" } }'
```

or

```bash
aws dynamodb query --table-name Music --key-conditions file://key-conditions.json
```

Query the table by album title.

```bash
aws dynamodb query --table-name Music \
    --index-name AlbumIndex \
    --key-condition-expression "AlbumTitle = :album" \
    --expression-attribute-values '{":album":{"S":"Led Zeppelin II"} }'
```

Scan the entire table into a JSON file.

```bash  
aws dynamodb scan --table-name Music --output json > music.json
```

Delete an item.

```bash   
aws dynamodb delete-item \
    --table-name Music \
    --key '{ "Artist": { "S": "Led Zeppelin" }, "SongTitle": { "S": "Ramble On" } }'
```

Delete the table.

```bash
aws dynamodb delete-table --table-name Music
```

### Lambda 

#### Hello World

Create a Lambda function that takes a name and returns *Hello {name}*.

#### Sample solution with Python

```bash
cd lambda-python-hello-world

zip hello-world.zip hello-world.py

aws iam create-role --role-name lambda-hello-world-role --assume-role-policy-document file://lambda-trust-policy.json

aws lambda create-function --function-name hello-world --zip-file fileb://hello-world.zip --handler hello-world.lambda_handler \
--runtime python3.9 --role arn:aws:iam::{aws-account-number}:role/lambda-hello-world-role

aws lambda invoke --function-name hello-world --cli-binary-format raw-in-base64-out --payload '{"name":"Martha"}' response.json

aws lambda delete-function --function-name hello-world

aws iam delete-role --role-name lambda-hello-world-role
```

#### Lambda with S3

Create a Lambda function that writes a string from user input to an S3 bucket.

#### Sample solution with Python

```bash
cd lambda-python-s3

aws s3 mb s3://s3-exercise-5321343

aws iam create-role --role-name lambda-s3-role --assume-role-policy-document file://lambda-trust-policy.json

aws iam create-policy --policy-name allow-s3-access-policy --policy-document file://s3-access-policy.json

aws iam attach-role-policy --role-name lambda-s3-role --policy-arn arn:aws:iam::{aws-account-number}:policy/allow-s3-access-policy

zip write-to-s3.zip write-to-s3.py

aws lambda create-function --function-name write-to-s3 --zip-file fileb://write-to-s3.zip --handler write-to-s3.save_to_bucket \
--runtime python3.9 --role arn:aws:iam::{aws-account-number}:role/lambda-s3-role

aws lambda invoke --function-name write-to-s3 --cli-binary-format raw-in-base64-out --payload '{"bucket-name":"s3-exercise-5321343", "file-path":"greeting/hello.txt", "file-content":"Hello, dear!"}' response.json

aws s3 cp s3://s3-exercise-5321343 . --recursive

aws s3 rb s3://s3-exercise-5321343 --force

aws lambda delete-function --function-name write-to-s3

aws iam detach-role-policy --role-name lambda-s3-role --policy-arn arn:aws:iam::{aws-account-number}:policy/allow-s3-access-policy

aws iam delete-policy --policy-arn arn:aws:iam::{aws-account-number}:policy/allow-s3-access-policy

aws iam delete-role --role-name lambda-s3-role
```

#### Lambda with DynamoDB

Create a Lambda function that stores a new item from user input into DynamoDB.

#### Sample solution with Python

```bash
cd lambda-python-dynamo-db

aws dynamodb create-table \
    --table-name Books \
    --attribute-definitions AttributeName=Author,AttributeType=S \
    --key-schema AttributeName=Author,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

aws iam create-role --role-name lambda-dynamo-db-role --assume-role-policy-document file://lambda-trust-policy.json

aws iam create-policy --policy-name allow-dynamo-db-access-policy --policy-document file://dynamo-db-policy.json

aws iam attach-role-policy --role-name lambda-dynamo-db-role --policy-arn arn:aws:iam::{aws-account-number}:policy/allow-dynamo-db-access-policy

zip write-to-dynamo-db.zip write-to-dynamo-db.py

aws lambda create-function --function-name write-to-dynamo-db --zip-file fileb://write-to-dynamo-db.zip --handler write-to-dynamo-db.put_into_table --runtime python3.9 --role arn:aws:iam::{aws-account-number}:role/lambda-dynamo-db-role

aws lambda invoke --function-name write-to-dynamo-db --cli-binary-format raw-in-base64-out --payload '{"new-item":
    {
        "Author": "Miguel de Cervantes",
        "Title": "Don Quijote de la Mancha",
        "Year": 1615
    }
}' response.json

aws dynamodb scan --table-name Books

aws dynamodb delete-table --table-name Books

aws lambda delete-function --function-name write-to-dynamo-db

aws iam detach-role-policy --role-name lambda-dynamo-db-role --policy-arn arn:aws:iam::{aws-account-number}:policy/allow-dynamo-db-access-policy

aws iam delete-policy --policy-arn arn:aws:iam::{aws-account-number}:policy/allow-dynamo-db-access-policy

aws iam delete-role --role-name lambda-dynamo-db-role
```

#### Further Useful Commands

##### Lambda

```bash
aws lambda list-functions

aws lambda update-function-configuration --function-name my-function --memory-size 256

aws lambda update-function-code --function-name my-function --zip-file fileb://my-function.zip
```

The `get-function` command returns Lambda function metadata and a presigned URL that you can use to download the function's deployment package.

```bash
aws lambda get-function --function-name my-function
```

##### Policy update and version deletion

In case you need to update your policy, use the following command:

```bash
aws iam create-policy-version --policy-arn arn:aws:iam::{aws-account-number}:policy/my-policy --policy-document file://my-policy.json --set-as-default
```

If you have several policy versions, you first need to delete all but the default one.
Below is the command for deleting policy version v1:

```bash
aws iam delete-policy-version --policy-arn arn:aws:iam::{aws-account-number}:policy/my-policy --version-id v1
```

#### Useful Links

[Lambda samples in different programming languages](https://docs.aws.amazon.com/lambda/latest/dg/lambda-samples.html)

[Lambda example with AWS CLI and NodeJS](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-awscli.html)

[Lambda example with Python in the management console](https://aws.amazon.com/tutorials/run-serverless-code/)

[IAM with AWS CLI](https://www.learnaws.org/2022/02/05/aws-cli-iam-guide/)

### API Gateway

*The API Gateway excercises would go beyound the scope of a one-day workshop.
Therefore, only references to readily available online solutions are provided.*

[Create an API gateway to manage a DynamoDB table.](https://aws.amazon.com/blogs/compute/using-amazon-api-gateway-as-a-proxy-for-dynamodb/)

[Create an API gateway for a Lambda function.](https://jeromedecoster.github.io/aws/api-gateway--lambda--aws-cli/)

[Same as above, but in the AWS management console.](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/usecases/creating_lambda_apigateway)
