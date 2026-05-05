from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Photek detector mapping from header
def get_photek_mapping():
    J4_1 = [11, 9, 8, 6, 5, 3, 2, 0, 15, 14, 13, 12, 10, 7, 4, 1, 31, 30, 29, 28, 26, 23, 20, 17, 27, 25, 24, 22, 21, 19, 18, 16]
    J4_2 = [15, 13, 12, 10, 9, 7, 6, 4, 14, 11, 8, 5, 3, 2, 1, 0, 30, 27, 24, 21, 19, 18, 17, 16, 31, 29, 28, 26, 25, 23, 22, 20]
    
    J3_1 = [J4_2[31-i] for i in range(32)]
    J3_2 = [J4_1[31-i] for i in range(32)]
    J2_1 = J4_1[:]
    J2_2 = J4_2[:]
    J1_1 = J3_1[:]
    J1_2 = J3_2[:]
    
    blocks = [
        {'readout': 0, 'x0': 0, 'y0': 0, 'width': 8, 'height': 4, 'map': J4_1},
        {'readout': 1, 'x0': 8, 'y0': 0, 'width': 8, 'height': 4, 'map': J4_2},
        {'readout': 2, 'x0': 0, 'y0': 4, 'width': 8, 'height': 4, 'map': J3_1},
        {'readout': 3, 'x0': 8, 'y0': 4, 'width': 8, 'height': 4, 'map': J3_2},
        {'readout': 4, 'x0': 0, 'y0': 8, 'width': 8, 'height': 4, 'map': J2_1},
        {'readout': 5, 'x0': 8, 'y0': 8, 'width': 8, 'height': 4, 'map': J2_2},
        {'readout': 6, 'x0': 0, 'y0': 12, 'width': 8, 'height': 4, 'map': J1_1},
        {'readout': 7, 'x0': 8, 'y0': 12, 'width': 8, 'height': 4, 'map': J1_2},
    ]
    
    channels = {}
    for block in blocks:
        for i in range(block['width'] * block['height']):
            x = block['x0'] + (i % block['width'])
            y = block['y0'] + (i // block['width'])
            ch = block['map'][i]
            readout = block['readout']
            name = f"R{readout}_Ch{ch}"
            channels[name] = {'x': x, 'y': y, 'readout': readout, 'channel': ch}
    
    return channels

# Load detector mapping
channels = get_photek_mapping()
detector_offset = {'x': 0, 'y': 0}

# Detector specs
DETECTOR_SPECS = {
    'pixel_pitch_mm': 3.312,  # 0.8mm per pixel
    'offset_x_mm': 28.156, # Position of pixel (0,0) center in mm (laser position)
    'offset_y_mm': 65.562
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/channels', methods=['GET'])
def get_channels():
    return jsonify(channels)

@app.route('/api/offset', methods=['GET', 'POST'])
def detector_offset_endpoint():
    global detector_offset
    if request.method == 'POST':
        data = request.json
        detector_offset['x'] = data.get('x', 0)
        detector_offset['y'] = data.get('y', 0)
    return jsonify(detector_offset)

@app.route('/api/specs', methods=['GET'])
def get_specs():
    return jsonify(DETECTOR_SPECS)

if __name__ == '__main__':
    import json
    from app import get_photek_mapping, DETECTOR_SPECS
    
    data = {
        "channels": get_photek_mapping(),
        "specs": DETECTOR_SPECS
    }

    # create the file if it doesn't exist, otherwise overwrite
    import os
    os.makedirs('static', exist_ok=True)
    with open('static/detector-data.json', 'w') as f:
        json.dump(data, f, indent=2)
        

    app.run(debug=True, host='localhost', port=5000)
