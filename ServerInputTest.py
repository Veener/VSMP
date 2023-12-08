from threading import Thread
import time


def inputFun():
    while True:
        data=input()
        returnData(data)

def outputFun():
    while True:
        print("OUT")
        time.sleep(5)

def returnData(data):
    print(f"Data: {data}")

inp=Thread(target=inputFun)
inp.start()
outputFun()