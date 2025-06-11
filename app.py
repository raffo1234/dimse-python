from flask import Flask, request, jsonify
from pynetdicom import AE
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
port = int(os.environ.get('PORT', 5000))

@app.route('/ping', methods=['POST'])
def ping_dicom():
    data = request.get_json()
    if not data or 'ip' not in data or 'port' not in data or 'aet_server' not in data:
        return jsonify({'ok': False, 'error': 'Missing required fields (ip, port, aet_server)'}), 400

    ip = data['ip']
    port_number = int(data['port'])
    aet_server = data['aet_server']
    aet_client = data.get('aet_client', 'MY_ECHO_SCU')

    # Create AE and add Verification context
    ae = AE(ae_title=aet_client)
    ae.add_requested_context('1.2.840.10008.1.1')

    # Associate
    assoc = ae.associate(ip, port_number, ae_title=aet_server)

    if assoc.is_established:
        status = assoc.send_c_echo()
        assoc.release()

        if status:
            return jsonify({
                'ok': True,
                'status': True,
                'message': f'Successfully Echoed to {aet_server}@{ip}:{port_number}'
            })
        else:
            return jsonify({'ok': False, 'error': 'Echo failed'}), 500
    else:
        return jsonify({
            'ok': False,
            'error': 'Association failed: could not connect to peer'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
