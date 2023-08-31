import json
from datetime import datetime
import requests
import os

urlDashboard = "https://console.cloud.google.com/home/dashboard?project=$projectID"
projectURL = "<a href='$urlDashboard'>$projectID</a>"

urlPolicy = "https://console.cloud.google.com/monitoring/alerting/policies/$policyID?project=$projectID"
policyLink = "<a href='$urlPolicy'>$policyName</a>"

def generate_alert(template_path,alert):
    global urlDashboard, projectURL, urlPolicy, policyLink
    
    with open(template_path, "r") as read_file:
        template = json.load(read_file)

    condition_name = alert["incident"]["condition_name"]
    template["summary"] = condition_name
    template["sections"][0]["activityTitle"] = condition_name

    summary = alert["incident"]["summary"]
    escaped_summary = summary.replace("{", "'").replace("}", "'")
    template["sections"][0]["activitySubtitle"] = escaped_summary

    timestamp = datetime.fromtimestamp(alert["incident"]["started_at"])
    started_at = json.dumps(timestamp, indent = 4, sort_keys = True, default = str)
    template["sections"][0]["facts"][0]["value"] = started_at

    projectID = alert["incident"]["resource"]["labels"]["project_id"]
    urlDashboard = urlDashboard.replace("$projectID", projectID)
    projectURL = projectURL.replace("$projectID", projectID)
    projectURL = projectURL.replace("$urlDashboard", urlDashboard)
    template["sections"][0]["facts"][1]["value"] = projectURL

    policyName = alert["incident"]["policy_name"]
    policyID = alert["incident"]["condition"]["name"]
    policyID = policyID.split('/')[3]
    urlPolicy = urlPolicy.replace("$policyID", policyID)
    urlPolicy = urlPolicy.replace("$projectID", projectID)
    policyLink = policyLink.replace("$urlPolicy", urlPolicy)
    policyLink = policyLink.replace("$policyName", policyName)
    template["sections"][0]["facts"][2]["value"] = policyLink

    template["sections"][0]["facts"][3]["value"] = condition_name

    metric = alert["incident"]["metric"]["type"]
    template["sections"][0]["facts"][4]["value"] = metric

    threshold = alert["incident"]["condition"]["conditionThreshold"]["thresholdValue"]
    template["sections"][0]["facts"][5]["value"] = threshold

    observed_value = alert["incident"]["observed_value"]
    template["sections"][0]["facts"][6]["value"] = observed_value

    incidentURL = alert["incident"]["url"]
    template["potentialAction"][0]["targets"][0]["uri"] = incidentURL

    return template

def send_alert(teams_alert):
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(os.environ.get('webhookURL'), headers=headers, json=teams_alert)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    print("Teams alert successfully sent")