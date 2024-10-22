from django.shortcuts import render
from .models import ScanResult
import requests
import socket
from django.utils import timezone
import json

required_headers = ['content-security-policy','permissions-policy','X-Content-Type-Options','X-Frame-Options','Strict-Transport-Security','Referrer-Policy']

def scan_site(request):
    if request.method == 'POST':
        url = request.POST.get('website_url')
        try:
            response = requests.get(url)
            headers = response.headers
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'error': str(e)})
        missing_headers = []
        valid_headers = {}
        for header in required_headers:
            if header not in headers:
                missing_headers.append(f'{header}: Missing')
                valid_headers[header] = 'Missing'
            else:
                valid_headers[header] = 'Enabled'

        grade = assign_grade(missing_headers)
        time = timezone.now()
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            ip_address = "IP resolution failed"

        scan_result = {
            "url": url,
            "ip_address": ip_address,
            "time": time,
            "grade": grade,
            "headers": valid_headers
        }
        if not ScanResult.objects.filter(url=url).exists():
            insert_data = ScanResult(
                url=url,
                ip_address=ip_address,
                grade=grade,
                headers=json.dumps(valid_headers),
                scan_time=time
            )
            insert_data.save()
        return render(request, 'scan_result.html', {'scan_result': scan_result})
    grand_totals = {
        'A+': ScanResult.objects.filter(grade='A+').count(),
        'A': ScanResult.objects.filter(grade='A').count(),
        'B': ScanResult.objects.filter(grade='B').count(),
        'C': ScanResult.objects.filter(grade='C').count(),
        'D': ScanResult.objects.filter(grade='D').count(),
        'E': ScanResult.objects.filter(grade='E').count(),
        'F': ScanResult.objects.filter(grade='F').count(),
    }
    total_scans = sum(grand_totals.values())
    grand_totals['Total'] = total_scans

    recent_scans = ScanResult.objects.all().order_by('-scan_time')[:10]  
    hall_of_fame = ScanResult.objects.filter(grade__in=['A+', 'A']).order_by('-scan_time')[:10]
    hall_of_shame = ScanResult.objects.filter(grade='F').order_by('-scan_time')[:10]

    context = {
        'grand_totals': grand_totals,
        'recent_scans': recent_scans,
        'hall_of_fame': hall_of_fame,
        'hall_of_shame': hall_of_shame
    }

    return render(request, 'index.html', context)

def assign_grade(missing_headers):
    missing_count = len(missing_headers)

    if missing_count == 0:
        return 'A+'
    elif missing_count == 1:
        return 'A'
    elif missing_count == 2:
        return 'B'
    elif missing_count == 3:
        return 'C'
    elif missing_count == 4:
        return 'D'
    elif missing_count == 5:
        return 'E'
    else:
        return 'F'

def about_page(request):
    return render(request, 'about.html')
