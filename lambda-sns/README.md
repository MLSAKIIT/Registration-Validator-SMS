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
      --attribute-definitions AttributeName=Name,AttributeType=S AttributeName=phoneNumber,AttributeType=S \
      --key-schema AttributeName=Name,KeyType=HASH  AttributeName=phoneNumber,KeyType=RANGE \
      --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
      --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES
     ```
     This creates a DynamoDB table called Users with `Name` as Partition Key & `phoneNumber` as Sort Key accepting String Datatypes. This also enables DynamoDB Streams.
     
  2. Go to AWS DynamoDB from the AWS Console Homepage and search DynamoDB. Select `Tables` in the left pane of the DynamoDB page to access your table.
     
     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/67b935ff-eca3-4e74-92ae-17820260e635)

</details>
<details>
  <summary><h3>Step 2. AWS Lambda Handler Function</h3></summary>

  ### AWS Lambda Configuration
  
  1. Go to Services > Lambda > Functions > `Create function`
  2. Provide a name for the function and select the following configuration

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/cc4b09ef-4808-4e5f-8d7d-0e18b931dbea)

  3. Under the Code Source window copy the contents of the lambda_function.py from the repository files.
  4. Go to Configuration > Permissions > Execution Role. Click the role name assigned to the Lambda function which will redirect to the **IAM console**.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/78a0ce93-dcce-4aca-9f6b-add713b26931)
   
  5. Go to Permission Policies > Add permissions > Attach Policies

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/85c69bcd-b863-4a1d-b118-34861115eee7)

  6. Search and Select `Amazon SNS Full Access` under Other permissions Policies and click Add permissions.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/ecb3b6f7-13c6-490b-9148-5a2eec857762)

</details>
<details>
  <summary><h3>Step 3. AWS EventBrige Pipeline</h3></summary>

  ### Creating the EventBridge Pipeline
  
  1. Go to Services > Amazon EventBridge > Pipes > `Create Pipe`
  2. In the below window, name your pipeline. Under Source, select Source and click on DynamoDB Stream.
     
     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/379516a2-0770-45b6-8918-052b53f06547)
     
  3. Under DynamoDB steam, select the DynamoDB database from the last step.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/05ffa7b3-86cf-41ad-a1be-061261c336bd)

  4. Click on Filtering. From the sample events, select Sample event 1 for DynamoDB Stream.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/fb0748c4-54ba-406f-a76a-cdec31246f7c)

  5. In the `Event pattern`, paste the following pattern.

     ```json
     {
       "dynamodb": {
         "NewImage": {
           "phoneNumber": {
             "S": [{
               "prefix": "+91"
             }]
           }
         }
       }
     }
     ```
     The EventBridge Pipeline will trigger Lambda function only if new records from DynamoDB have a prefix <kbd>+91</kbd> in the `phoneNumber` column. This filters user records having the country code [+91] for valid Indian phone numbers which will be used for sending the SMS.

  6. Under Target, select *AWS Lambda* for Target Service. Select the Lambda function created in [Step 2](#step-2-aws-lambda-handler-function) under Function. Click `Next`.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/f5eb2a4d-4d6f-4ce2-b31a-d6a7be844d31)

  7. In your Pipeline window go to Settings > Permissions > Execution Role ID.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/d7928ebc-5d0d-4323-adcb-17d0f39e09fb)

  8. Go to Permission Policies > Add permissions > Attach Policies

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/02d4c113-195b-466d-b357-e7520f231561)

  9. Search and Select `Amazon Lambda Full Access` under Other permissions Policies and click Add permissions.

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/8a84043a-9d71-4a34-8e7e-cfe0d58c88e0)

</details>
<details>
  <summary><h3>Step 4. SNS Setup</h3></summary>

  ### Configuring AWS SNS
  
  1. Go to Services > Simple Notification Service > Text Messaging(SMS) > Sandbox destination phone numbers > `Add phone number`

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/4e0d15a7-ac69-4b0b-a57b-457ea7bacda3)

  2. Add a phone number that may be used for testing purposes for verification by Amazon. Follow the steps until the phone number appears under the sandbox showing Status:
      |:white_check_mark:|Verified|
      |------------------|:-------|

     ![image](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/883a3b27-1a05-4a57-af60-32402cd4983f)
</details>

> [!IMPORTANT]  
> Failing to configure the **IAM Roles** properly might cause the functions & services to not work properly.

### Usage

![Screenshot 2023-11-20 223916](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/af297c73-58a9-4e59-b350-9b1e656f5c41)

## Resources

- AWS EventBridge Documentation: https://docs.aws.amazon.com/eventbridge
- AWS Lambda Documentation: https://docs.aws.amazon.com/lambda
- AWS SNS Documentation: https://docs.aws.amazon.com/sns
- AWS DynamoDB Documentation: https://docs.aws.amazon.com/dynamodb