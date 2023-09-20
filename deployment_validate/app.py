from flask import Flask, request, jsonify
import ssl

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_deployment():
    try:
        admission_request = request.json
        admission_response = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": admission_request['request']['uid'],
                "allowed": False,
                "status": {
                    "reason": "ValidationWebhookError",
                    "message": "Resource requests must be specified for Deployment."
                }
            }
        }
        print(admission_request)
        if admission_request['request']['kind']['kind'] == 'Deployment':
            deployment_spec = admission_request['request']['object']['spec']['template']['spec']
            if 'containers' in deployment_spec:
                for container in deployment_spec['containers']:
                    if 'resources' not in container or 'requests' not in container['resources']:
                        return jsonify(admission_response)

        admission_response['response']['allowed'] = True
        return jsonify(admission_response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=443,ssl_context=('/etc/certs/tls.crt', '/etc/certs/tls.key'))