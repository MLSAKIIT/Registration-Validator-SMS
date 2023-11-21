import json
import boto3

def lambda_handler(event, context):
    boto3_version = boto3.__version__

# data from dynamodb data stream
    print(event) 
  
# parsing for user details
    cust_number = event[0]["dynamodb"]["NewImage"]["phoneNumber"]["S"] 
    name = event[0]["dynamodb"]["NewImage"]["Name"]["S"]

    print(name, cust_number)

# creating a json of user details
    return_statement = {
        'name': name,
        'cust_number': cust_number
    } 

# Publishing formatted message to number via SNS
    print ("sending message...") 
    client = boto3.client("sns")
    response = client.publish(
        PhoneNumber=cust_number,
        Message=f"Thank you {name} for registering for MLSA EVENT_NAME using phone number:{cust_number}"
    )
    print (response)

# Details to be printed to CloudWatch logs upon execution
    return {
        'statusCode': 200,
        'body': json.dumps(return_statement)
    }