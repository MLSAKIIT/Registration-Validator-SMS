# Event Registration Confirmation through SMS via AWS

> Demo of serverless application to send instant verification SMS based on form response submission

## Table of Contents
- [Problem Statement](#problem-statement)
- [Architecture](#high-level-architecture-overview)
- [Setup and Instructions](#setup)
- [Conclusion](#conclusion)
- [Credits](#contributors)

# Introduction

### Problem Statement

Every year MLSA conducts 3-4 events with a registration period of a week. Upto 2000 registrations take place through a contact form hosted on a subdomain on our official website. However upon registering, participants don't receive a confirmation message potentially causing confusion.

# High Level Architecture Overview

## AWS Services In Use

1. API Gateway can directly communicate with AWS services using their low-level APIs. This includes AWS services such as DynamoDB.

2. DynamoDB is a NoSQL database stores relevant user details along with contact details such as phone numbers in JSON format.

3. DynamoDB Streams captures a time-ordered sequence of item-level modifications in a DynamoDB table [INSERT, MODIFY, DELETE], enabling real-time data processing via pipelines or Lambda functions.

4. AWS EventBridge acts as a pipeline service by providing a streamlined way for events to flow between different components of our applications or other AWS services. It allows you to define event sources, set rules and filters, and seamlessly deliver them to targets for processing. 

5. AWS Lambda is a serverless compute service that lets us run code without provisioning or managing servers.

6. AWS SNS is a fully managed topic based publish/subscribe messaging service that will be used to send SMS messages to users.

##

### Architecture Diagram & Overview

![Blank diagram](https://github.com/SourasishBasu/SMS-Verifier-AWS/assets/89185962/0135d68a-5c00-42a2-9c07-6fed994a6035)

A static site is hosted with a contact form. We use *API Gateway* to create an API which makes a `PUT` request to our *DynamoDB* database after the user clicks <kbd>Register</kbd> on the form.

The API sends user records to *DynamoDB* which then pushes the record into the *DynamoDB Data Stream*.

*AWS EventBrige Pipeline* is configured to use *DynamoDB Data Streams* as the Event **Source**, **Filter** for `INSERT` records in the stream to pick up only new entries. The record data is then pushed to the **Target** *Lambda* function.

*AWS Lambda* performs the processing on the input `JSON` data using Python to parse the user data and extract the Phone Number, name and other relevant details to send to *SNS*.

*AWS SNS* publishes a formatted string with user details as an SMS to the provided number, confirming their registration.

# Prerequisites

- **A Free-Tier eligible AWS account**
- **Python 3.11**

# Setup
<details>
  <summary><h2>Step 1. DynamoDB and Data Streams</h2></summary>

  ### Creating a Linux EC2 instance
  
  1. Choose a name for your EC2 server.
  2. Under `Application and OS Images
</details>

<details>
  <summary><h2>EventBrige Pipeline</h2></summary>

  ### Creating a Linux EC2 instance
  
  1. Choose a name for your EC2 server.
  2. Under `Application and OS Images
</details>

<details>
  <summary><h2>Lambda Handler Function</h2></summary>

  ### Creating a Linux EC2 instance
  
  1. Choose a name for your EC2 server.
  2. Under `Application and OS Images
</details>

<details>
  <summary><h2>SNS</h2></summary>

  ### Creating a Linux EC2 instance
  
  1. Choose a name for your EC2 server.
  2. Under `Application and OS Images
</details>


## Improvements

- For implementing in production, user may exit the `SMS Sandbox` in **AWS SNS** to publish messages to any phone number for standard rates
- Email functionality may be implemented parallely along with SMS.
- 

## Conclusion

We demonstrated an end-to-end solution to using AWS and serverless infrastructure to send users instantaneous confirmation messages via SMS upon registering for an event on a website contact form.

## Contributors ##

| Authors                                |
| ---------------------------------------|
| Sourasish Basu @Sasquatch				 |
| Swapnil Dutta @rycerzes				 |


## Version history ##

| Version | Date          		| Comments        |
| ------- | ------------------- | --------------- |
| 1.0     | Nov 16th, 2023   | Initial release |

## Disclaimer ##
**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**
