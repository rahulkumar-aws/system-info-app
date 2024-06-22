from flask import Flask, jsonify, render_template
import socket
import psutil
import time

app = Flask(__name__)

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def format_bytes(size):
    # Convert bytes to human-readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_disk_space():
    disk_usage = psutil.disk_usage('/')
    return {
        'total': format_bytes(disk_usage.total),
        'used': format_bytes(disk_usage.used),
        'free': format_bytes(disk_usage.free),
        'percent': disk_usage.percent
    }

def get_cpu_info():
    return {
        'count': psutil.cpu_count(),
        'percent': psutil.cpu_percent(interval=1)
    }

def get_ram_info():
    virtual_memory = psutil.virtual_memory()
    return {
        'total': format_bytes(virtual_memory.total),
        'available': format_bytes(virtual_memory.available),
        'percent': virtual_memory.percent,
        'used': format_bytes(virtual_memory.used),
        'free': format_bytes(virtual_memory.free)
    }

def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': format_bytes(net_io.bytes_sent),
        'bytes_recv': format_bytes(net_io.bytes_recv)
    }

@app.route('/system_info', methods=['GET'])
def system_info():
    return jsonify({
        'ip_address': get_ip_address(),
        'disk_space': get_disk_space(),
        'cpu_info': get_cpu_info(),
        'ram_info': get_ram_info(),
        'network_info': get_network_info()
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/graph_data', methods=['GET'])
def graph_data():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent
    net_recv = net_io.bytes_recv
    return jsonify({
        'cpu_percent': cpu_percent,
        'ram_percent': ram_percent,
        'disk_percent': disk_percent,
        'net_sent': net_sent,
        'net_recv': net_recv,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
