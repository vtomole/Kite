import sys
import requests

url ='http://127.0.0.1:5000/api/add_message/1234'

def run(path):    
    with open(path, 'r') as myfile:
        data=myfile.read() 
        res = requests.post(url, json={"mytext":data})
    
        if res.ok:
            j = res.json()
            print (j["results"])


if __name__ == "__main__":    
    run(sys.argv[1])
