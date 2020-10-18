# Prerequisites 

## 1. Telegram Token

Create a new bot by talking to [Bot Father](https://t.me/botfather) and remenber your authorization token. This is described in more detail [here](https://core.telegram.org/bots#6-botfather).

## 2. Create IAM
1. Login to your IAM dashboard, create a group with full access permission to "s3" and "transcribe".
2. Create a user and assign the the group

A official guide for both steps is given [here](https://docs.aws.amazon.com/medialive/latest/ug/setup-user-step-groups.html) and [here](https://docs.aws.amazon.com/medialive/latest/ug/setup-user-step-create-user.html).

## 3. Configure AWS
You need to configure the aws cli with following command.

```
[user@home] $ aws configure
AWS Access Key ID [None]: XXXXXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXX
Default region name [None]:  enter
Default output format [None]:  enter
```

## 4. Create a s3 bucket

Create a s3 buckets following the official AWS [instructions](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) and rememeber the name.

## 5. Complete config.json

Fill all required data into the `config.json`.
```
{
    "s3-bucket": "name-of-s3-bucket",
    "bot-token": "token-of-telegram-bot",
    "language": "en-US"
}
```

## 5. Make venv

```
$ python -m venv env
$ pip install -r requirements.txt
$ source ./env/bin/activate
```

## 6. Run bot
 ```
 $ python ./main.py
 ```