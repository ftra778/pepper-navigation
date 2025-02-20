import threading
import time
# from statistics import mean

up = True

def _t_1():
    global up
    time.sleep(9)
    x = 5
    while up:
        x = x + 1
        print(x)
        
def _t_2():
    global up
    time.sleep(9)
    x = 5
    while up:
        x = x + 1
        print(x)



if __name__ == "__main__":
    _1 = threading.Thread(target=_t_1)
    _2 = threading.Thread(target=_t_2)
    
    duration = 6
    
    start = time.time()
    test1 = []
    test2 = []
    while time.time() - start < duration:
        c1 = time.time()
        c2 = time.time()
        test1.append(c2 - c1)
        
    _1.start()
    _2.start()
    start = time.time()
    while time.time() - start < duration:
        c1 = time.time()
        c2 = time.time()
        test2.append(c2 - c1)
        
    print("No threading: {}".format(sum(test1)/(float(len(test1)))))
    print("Threading: {}".format(sum(test2)/(float(len(test2)))))
        
    up = False
    _1.join()
    _2.join()