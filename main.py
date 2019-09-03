import threading
import time
from collections import deque

commonList=set()
q=deque()

def worker():
    """
    スレッド
    """
    global q
    global commonList
    
    while True:
        try:
            item = q.popleft()
        except IndexError as ie:
            #print(ie)
            time.sleep(0.1) #Ctrl+Cで終了させるおまじない。
            break
        
        commonList.add((item.ID,sum(item.values)))

def main():
    global q
    global commonList
    num_worker_threads = 10
    test_data_num = 5000000
    print(f'Data set: {test_data_num}')
    print(f'Worker thread: {num_worker_threads}')

    """
    テストデータをセットする
    """
    set_data_start = time.time()
    threadItem = set()
    threadItem = [Job([1,2,3],0) for i in range(test_data_num)]

    set_data_time = time.time() - set_data_start
    print (f'Set test data elapsed_time:{format(set_data_time)} [sec]')

    """
    Queueへテストデータを詰める
    """
    queueing_start = time.time()
    [q.append(item) for item in threadItem]

    queueing_time = time.time() - queueing_start
    print (f'Queueing elapsed_time:{format(queueing_time)} [sec]')


    """
    スレッドを立てる
    """
    process_start = time.time()
    threads=set()
    thread_start = time.time()
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.add(t)
    
    thread_start_elapsed_time = time.time() - thread_start
    print (f'Thread start elapsed_time:{format(thread_start_elapsed_time)} [sec]')    
    
    """
    Queueが空になるまで待機する
    """
    while True:
        #print(len(q)) ちゃんとさばいてるか確認用
        if len(q) == 0:
            break;
        else:
            time.sleep(0.1)

    process_time = time.time() - process_start
    print (f'Process all data elapsed_time:{format(process_time)} [sec]')

    #スレッド停止命令(None)の投入
    for i in range(num_worker_threads):
        q.append(None)
    
    #スレッドの終了まち
    for t in threads:
        t.join()
    
class Job():
    #xはリスト,yは書き込み先のリストのインデックス
    def __init__(self,x,y):
        self.values=x.copy()
        self.ID=y

if __name__ == '__main__':
    main()