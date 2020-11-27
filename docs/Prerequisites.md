# Prerequisites 

You will need `docker` in order to run the bot.
## 1. Telegram Token

Create a new bot by talking to [Bot Father](https://t.me/botfather) and remenber your authorization token. This is described in more detail [here](https://core.telegram.org/bots#6-botfather).

## 2. Create IAM
1. Login to your IAM dashboard, create a group with full access permission to "s3" and "transcribe".
2. Create a user and assign the the group

A official guide for both steps is given [here](https://docs.aws.amazon.com/medialive/latest/ug/setup-user-step-groups.html) and [here](https://docs.aws.amazon.com/medialive/latest/ug/setup-user-step-create-user.html).

## 4. Create a s3 bucket

Create a s3 buckets following the official AWS [instructions](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) and rememeber the name.

## 5. Complete Dockerfile

Fill all required keys into the `Dockerfile`

## 6. Run Container

```
make run
```