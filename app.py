from flask import Flask, request, jsonify
from pynetdicom import AE, build_context
from pynetdicom.sop_class import Verification
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://cadia.pe", "http://localhost:3000"])
port = os.environ.get('PORT', 5000)

@app.route('/ping', methods=['POST'])
def ping_dicom():
    data = request.get_json()
    if not data or 'ip' not in data or 'port' not in data or 'aet_server' not in data:
        return jsonify({'ok': False, 'error': 'Missing required fields (ip, port, aet_server)'}), 400

    ip = data['ip']
    port_number = int(data['port'])
    aet_server = data['aet_server']
    aet_client = data.get('aet_client', 'MY_CLIENT_AE')

    # Create application entity
    ae = AE(ae_title=aet_client)

    # Create a Verification presentation context
    context = build_context(Verification)

    # Add the presentation context to the AE's requested contexts
    ae.requested_contexts.append(context)

    # Associate with peer AE
    assoc = ae.associate(ip, port_number, aet_server, ae_title=aet_server)

    if assoc.is_established:
        status = assoc.send_c_echo()
        if status:
            return jsonify({'ok': True, 'status': True, 'message': f'Successfully Echoed to {aet_server}@{ip}:{port_number}'})
        else:
            return jsonify({'ok': False, 'error': 'Echo failed'}), 500
        assoc.release()
    else:
        return jsonify({'ok': False, 'error': f'Association failed: {assoc.reason_str}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)