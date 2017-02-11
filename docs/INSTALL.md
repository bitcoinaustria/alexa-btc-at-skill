# Create an Alexa Skill

Go to to https://developer.amazon.com and create a new Alexa skill.
Fill out the Skill information as you wish. 
Add an interaction Model schema like this:
```
    {
      "intents": [
        {
          "intent": "Bitcoin",
          "slots": [
            {
              "name": "currency",
              "type": "currency"
            }
          ]
        }
      ]
    }
```

Create the type "currency" with the values: Dollar | Euro | Pound (depending on the language)

Create Sample Utterances like this:

```
    Bitcoin Austria how much is a bitcoin in {currency}
    Bitcoin Austria how is bitcoin doing
```

# Deploy a Lambda

Go to https://aws.amazon.com/console/ and login to your console. Go to the lambda services and add a new lambda. I recon to use the alexa skill python template and then choose to upload the lambda function.

For production environments you can use [Serverless](http://www.serverless.com) to deploy your lambda by installing the aws cli and the serverless client (npm install serverless -g) and entering ```serverless deploy```.

No matter how you deploy it you need to enter the lambda's ARN, which is printed out after entering ```serverless deploy``` or on the right top of the lambda AWS page.

