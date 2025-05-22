from django.http import JsonResponse
from django.shortcuts import render
from urllib.parse import urlparse
import subprocess
import re
import time
from datetime import datetime
from collections import defaultdict
import threading
import json

captured_data = defaultdict(list)
capture_thread = None
is_capturing = False


def index(request):
    return render(request, 'phone_capture_index.html')


def extract_domain(text):
    match = re.search(r'https?://[\w.-]+(:\d+)?', text)
    if match:
        try:
            return urlparse(match.group()).netloc or "unknown"
        except:
            return "parse-error"
    return "no-url"


def check_devices(request):
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip() and 'device' in line:
                devices.append(line.split('\t')[0])
        return JsonResponse({'success': True, 'devices': devices})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def capture_logcat(device_id, duration):
    global captured_data, is_capturing

    captured_data.clear()
    is_capturing = True
    cmd = ['adb', '-s', device_id, 'logcat', '-v', 'time']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    start_time = time.time()
    while time.time() - start_time < duration and is_capturing:
        try:
            line = process.stdout.readline()
            if not line:
                break
            decoded = line.decode('utf-8', errors='replace').strip()
            if 'http' in decoded:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                domain = extract_domain(decoded)
                captured_data[domain].append({
                    'timestamp': timestamp,
                    'data': decoded,
                    'domain': domain
                })
        except Exception as e:
            continue

    process.terminate()
    is_capturing = False


def capture_traffic(request):
    global capture_thread, is_capturing

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            device_id = body.get('device_id')
            duration = int(body.get('duration', 10))

            if is_capturing:
                return JsonResponse({'success': False, 'error': '已有任务进行中'})

            capture_thread = threading.Thread(target=capture_logcat, args=(device_id, duration))
            capture_thread.start()

            return JsonResponse({'success': True, 'message': '开始捕获'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '请求方法错误'})


def stop_capture(request):
    global is_capturing
    is_capturing = False
    return JsonResponse({'success': True, 'message': '已停止'})


def get_captured_data(request):
    return JsonResponse({
        'success': True,
        'data': dict(captured_data),
    })