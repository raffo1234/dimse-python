# app.py
from flask import Flask, request, jsonify
from pydicom import dcmnet
import os

app = Flask(__name__)
port = os.environ.get('PORT', 5000)  # Default port for Render.com

@app.route('/ping', methods=['POST'])
def ping_dicom():
    data = request.get_json()
    if not data or 'ip' not in data or 'port' not in data or 'aet_server' not in data:
        return jsonify({'ok': False, 'error': 'Missing required fields (ip, port, aet_server)'}), 400

    ip = data['ip']
    port_number = int(data['port'])
    aet_server = data['aet_server']
    aet_client = data.get('aet_client', 'MY_CLIENT_AE')

    ae = dcmnet.AE(ae_title=aet_client)
    assoc = None
    try:
        assoc = ae.associate(ip, port_number, aet_server)
        if assoc.is_established:
            status = assoc.send_c_echo()
            if status:
                return jsonify({'ok': True, 'status': True, 'message': f'Successfully Echoed to {aet_server}@{ip}:{port_number}'})
            else:
                return jsonify({'ok': False, 'error': 'Echo failed'}), 500
        else:
            return jsonify({'ok': False, 'error': 'Association failed'}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        if assoc and assoc.is_established:
            assoc.release()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)