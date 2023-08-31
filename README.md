# teams-alerts
Cloud Function to send GCP alerts to MS Teams

![image](https://github.com/matheusmartns/teams-alerts/assets/9992922/9d13df52-36e8-4ca9-be53-3546ddde0ce1)

Medium Article: https://medium.com/@mathmartns/gcp-alerts-on-microsoft-teams-309f7bd8bd0a

## Getting Started

### Prerequisites

- Webhook for the MS Teams channel, for that, visit this well-covered [guide](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=dotnet) by Microsoft;
- Pub/Sub Topic and subscription to receive the Alert;
- The [Policy](https://console.cloud.google.com/monitoring/alerting) that will trigger the alert;
- Create the Cloud Function using the provided files, you **NEED** to create a runtime environment variable named **webhookURL** that contains the webhook URL that the MS Teams generated for you (or you can hardcode it, use a variable inside your code, here it's your choice).

### Files
#### <ins>main.py</ins>
As the name says, this is the main file of our function, Our main function receives event and context, both come from the pub/sub and are mandatory, but the info that we need is inside the event on its data section.

#### <ins>json_operations.py</ins>
Here is where the magic happens, we get the required info from the Pub/Sub original Alert and insert them on the fields of the JSON alert that will be sent to the MS Teams.

A lot of transformation is going on there and I won’t be able to cover it here, but the strategy is basically the same, We assign to a variable the value we want from the original alert message (if necessary perform modifications, for example, the Timestamp we need to adjust it to a human-readable format) and “paste” it on the respective field of the new alert JSON template.

#### <ins>template.json</ins>
This is the template file that will be filled with the information that will come from the Pub/Sub and this format is readable by the MS Teams, you can find more about it [here](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL).
