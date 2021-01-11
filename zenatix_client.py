import requests
import time
from threading import Thread as thread
from queue import Queue
import json 

post_url="http://127.0.0.1:8000/send_data/"
csv_file="dataset.csv"

fail_queue=Queue()

def process_csv():
    data_dict={}

    with open(csv_file) as f:
        raw_line=f.readline()
        line = raw_line.strip()
        headers=line.split(",")
        while(raw_line):
            raw_line = f.readline()
            if (not raw_line):
                break
            line=raw_line.strip().split(",")
            for i in range(len(headers)):
                data_dict[headers[i]]=line[i]
            post_to_server(data_dict)
            time.sleep(60)
            
def post_to_server(data_dict):

    final_request = json.dumps(data_dict)   

    response = None

    try :
        response = requests.post(url = post_url, data = final_request)

    except Exception as E:
        print(E)

    if response is None or not check_status(response):
        if type(data_dict) == dict:
            fail_queue.put(data_dict)
        else:

            for data in data_dict:
                print("data is ", data, "\n\n")
                fail_queue.put(data)

def check_status(response):
    if response.status_code==201:
        return True
    else:
        return False

def post_failed_request():
    while True:
        if not fail_queue.empty():

            data_to_retry = [fail_queue.get() for _ in range(fail_queue.qsize())]

            data_to_retry = [item for index, item in enumerate(data_to_retry) if item not in data_to_retry[index + 1 : ]]
            post_to_server(data_to_retry)
            time.sleep(5)

if __name__ == '__main__':
    try:
       thread( target = process_csv ).start()
       thread( target = post_failed_request).start()
    except Exception as E:
        print(E)
        print("Error: unable to start thread")