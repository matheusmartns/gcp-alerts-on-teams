import json_operations
import base64
import json

def main(event, context):
    template_path = "template.json"
    alert = base64.b64decode(event['data']).decode('utf-8')
    alert_json = json.loads(alert)

    teams_alert = json_operations.generate_alert(template_path, alert_json)
    json_operations.send_alert(teams_alert)