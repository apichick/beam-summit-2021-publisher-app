# Streaming tweets to Pub/Sub

This is an python application that streams tweets to Cloud Pub/Sub. 

## Pre-requisites

In order to be able to use this application follow the steps below:

**Twitter**

1. Create a Twitter developer account, if you don't have one already. You can apply for one [here](https://developer.twitter.com/en/apply/user.html)

2. Create a Twitter developer app. You can create one [here](https://developer.twitter.com/en/portal/apps/new)

3. Save the following for later:
        
    * API key and secret
    * Access token and secret

**Google Cloud**

1. [Select or create a Cloud Platform project.](https://console.cloud.google.com/project)

2. [Enable billing for your project.](https://support.google.com/cloud/answer/6293499#enable-billing)

3. [Enable the Google Cloud Pub/Sub API.](https://console.cloud.google.com/flows/enableapi?apiid=pubsub.googleapis.com)

4. [Create a Cloud Pub/Sub topic.](https://console.cloud.google.com/cloudpubsub/topicList)

5. [Create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts). Do not assign any role yet.

6. Create a service account key:

    a. [Go to the service account list](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts)

    b. Select a project.

    c. Click the email address of the service account that you want to create a key for.

    d. Click **Manage Keys** on the **Actions** menu.

    e. Click on the **Add Key** drop-down menu, then select **Create New Key**.

    f. Select JSON as the Key type and click **Create**. The key will be downloaded to your local file system.

6. Assign the Pub/Sub Publisher role (roles/pubsub/publisher) to the service account on the created Cloud Pub/Sub topic:

    a. [Go to the Cloud Pub/Sub topics list](https://console.cloud.google.com/cloudpubsub/topic/list)

    b. Click the name of the Cloud Pub/Sub topic that was created on step 4.

    c. On the **Permissions** tab to the left of the screen, click on the **Add Member** button. 

## Installation

1. Clone this repository.

        git clone git@github.com:apichick/beam-summit-2001-publisher-app.git

2. Change to the publisher-app directory.

        cd publisher-app

3. Create a configuration file named config.txt with the following contents:

        [twitter]
        api_key=<TWITTER APP API KEY>
        api_key_secret=<TWITTER APP API KEY>
        access_token=<TWITTER APP ACCESS TOKEN KEY>
        access_token_secret=<TWITTER APP ACCESS TOKEN SECRET>
        [pubsub]
        topic=projects/<PROJECT_ID>/topics/<TOPIC_NAME>
        key_file=<SERVICE ACCOUNT JSON KEY FILE PATH>
    
    Enter right values for all the properties.

4. Install dependencies

        pip install -r requirements.txt

5. Run the application

        python main.py --locations " -74,40,-73,41" --config-file config.txt

    The option ```--locations``` specifies a set of bounding boxes to track (In the example above, the coordinates correspond to New York City). More details [here](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/filter-realtime/guides/basic-stream-parameters#locations)