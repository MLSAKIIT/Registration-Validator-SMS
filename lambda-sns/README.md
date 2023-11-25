# Getting Started with `AWS Configuration`
Initial commit from [@SourasishBasu](https://github.com/Sourasishbasu).
### AWS Infrastructure in use
- `API Gateway` can directly communicate with AWS services using their low-level APIs. This includes AWS services such as `DynamoDB`.
- `DynamoDB` is a NoSQL database stores relevant user details along with contact details such as phone numbers in JSON format.
- `DynamoDB Streams` captures a time-ordered sequence of item-level modifications in a DynamoDB table `[INSERT, MODIFY, DELETE]`, enabling real-time data processing via pipelines or `Lambda` functions.
- `EventBridge` acts as a pipeline service by providing a streamlined way for events to flow between different components of our applications or other AWS services. It allows you to define event sources, set rules and filters, and seamlessly deliver them to targets for processing.
- `Lambda` is a serverless compute service that lets us run code without provisioning or managing servers.
- `SNS` is a fully managed topic based publish/subscribe messaging service that will be used to send SMS messages to users.

## Setup
<details>
  <summary><h3>Step 1. DynamoDB and Data Streams</h3></summary>

  ### Creating the DynamoDB table

  1. Open AWS CloudShell and execute the following commands.
     
     ```bash
      aws dynamodb create-table \
      --table-name Users \
      --attribute-definitions AttributeName=id,AttributeType=S AttributeName=roll,AttributeType=S \
      --key-schema AttributeName=id,KeyType=HASH  AttributeName=roll,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
      --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES
     ```
     This creates a DynamoDB table called Users with `id` as Partition Key & `roll` as Sort Key accepting String datatypes. This also enables DynamoDB Streams.
     
  2. Go to AWS DynamoDB from the AWS Console Homepage and search DynamoDB. Select `Tables` in the left pane of the DynamoDB page to access your table.
     
     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/DynamodbTable.png)

</details>
<details>
  <summary><h3>Step 2. AWS Lambda Handler Function</h3></summary>

  ### AWS Lambda Configuration
  
  1. Go to Services > Lambda > Functions > `Create function`.
  2. Provide a name for the function and select the following configuration

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/FunctionCreation.png)

  3. Under the Code Source window copy the contents of the `app.py` from the repository files.
  4. Go to Configuration > Permissions > Execution Role. Click the role name assigned to the Lambda function which will redirect to the **IAM console**.

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/ExecutionRole.png)
   
  5. Go to Permission Policies > Add permissions > Attach Policies.

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/AttachPolicies.png)

  6. Search and Select `Amazon SNS Full Access` under Other permissions Policies and click Add permissions.

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/SNSpermission.png)

</details>
<details>
  <summary><h3>Step 3. AWS EventBrige Pipeline</h3></summary>

  ### Creating the EventBridge Pipeline
  
  1. Go to Services > Amazon EventBridge > Pipes > `Create Pipe`.
  2. In the below window, name the pipeline. Under Source, select Source and click on DynamoDB Streams.     
  3. Under DynamoDB Stream, select the DynamoDB database from [Step 1](#step-1-dynamodb-and-data-streams).

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/EBSource.png)

  4. Click on Filtering. From the sample events, select Sample event 1 for DynamoDB Stream.

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/SampleEvents.png)

  5. In the `Event pattern`, paste the following pattern.

     ```json
     {
       "dynamodb": {
         "NewImage": {
           "phone": {
             "S": [{
               "prefix": "+91"
             }]
           }
         }
       }
     }
     ```
     The EventBridge Pipeline will trigger Lambda function only if new records from DynamoDB have a prefix <kbd>+91</kbd> in the `phone` column. This filters user records having the country code [+91] for valid Indian phone numbers which will be used for sending the SMS.

  6. Under Target, select *AWS Lambda* for Target Service. Select the Lambda function created in [Step 2](#step-2-aws-lambda-handler-function) under Function. Click `Create Pipe` below.

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/TargetPipeline.png)

</details>
<details>
  <summary><h3>Step 4. SNS Setup</h3></summary>

  ### Configuring AWS SNS
  
  1. Go to Services > Simple Notification Service > Text Messaging(SMS) > Sandbox destination phone numbers > `Add phone number`.

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/SNSsandbox.png)

  2. Add a phone number that may be used for testing purposes for verification by Amazon. Follow the steps until the phone number appears under the sandbox showing Status:
      |:white_check_mark:|Verified|
      |------------------|:-------|

     ![image](https://github.com/MLSAKIIT/Registration-Validator-SMS/blob/e2453e8c85ac79fe6e796400f854157c2efc70aa/assets/NumberVerified.png)
</details>

## Resources

- AWS EventBridge Documentation: https://docs.aws.amazon.com/eventbridge
- AWS Lambda Documentation: https://docs.aws.amazon.com/lambda
- AWS SNS Documentation: https://docs.aws.amazon.com/sns
- AWS DynamoDB Documentation: https://docs.aws.amazon.com/dynamodb
