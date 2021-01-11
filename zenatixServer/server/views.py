from django.shortcuts import render
from django.http import HttpResponse
import os
from django.views.decorators.csrf import csrf_exempt
import json
import random
import os
from .utils import add_data

@csrf_exempt
def send_data(request):
    data = json.loads(request.body)
    rnd = random.randint(0,10)
    print("random variable is ", rnd)
    data_accepted = rnd <= 7

    if not data_accepted:
        error_message = {'message' : 'some error occured as act of god'}
        return HttpResponse(status=404, content=json.dumps(error_message))

    if not os.path.isfile('DataOutput.csv'):

        with open('DataOutput.csv', 'w+') as f:
            headers = ','.join(data.keys() if type(data) == dict else data[0].keys())
            headers += '\n'
            f.write(headers)

    with open('DataOutput.csv', 'r+') as f:

        data_sheet_headers = f.readline().strip().split(',')
        f.seek(0, os.SEEK_END)
        authentic_headers_set = set(data_sheet_headers)
        request_headers_set = set(data.keys() if type(data) == dict else data[0].keys())

        if authentic_headers_set != request_headers_set:

            return HttpResponse(status=400)

        if type(data) == dict:
            add_data(f, data, data_sheet_headers)
        else:
            for single_data_entry in data:
                add_data(f, single_data_entry, data_sheet_headers)

    return HttpResponse(status=201, content=json.dumps({"message":"success"}))






