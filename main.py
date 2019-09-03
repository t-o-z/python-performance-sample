import threading
import queue
import time

commonList=set()
q=queue.Queue()

def worker():
    """
    スレッド
    """
    global q
    global commonList
    
    while True:
        item = q.get()
        if item is None:            
            time.sleep(0.1) #Ctrl+Cで終了させるおまじない。
            break
        
        commonList.add((item.ID,sum(item.values)))
        q.task_done()

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
    スレッドを立てる
    """
    threads=set()
    thread_start = time.time()
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.add(t)
    
    thread_start_elapsed_time = time.time() - thread_start
    print (f'Thread start elapsed_time:{format(thread_start_elapsed_time)} [sec]')    

    """
    Queueへテストデータを詰める(Workerにて順次処理している)
    """
    process_start = time.time()
    queueing_start = time.time()
    [q.put(item) for item in threadItem]

    queueing_time = time.time() - queueing_start
    print (f'Queueing elapsed_time:{format(queueing_time)} [sec]')
    
    """
    Queueが空になるまで待機する
    """
    q.join()
    process_time = time.time() - process_start
    print (f'Process all data elapsed_time:{format(process_time)} [sec]')

    #スレッド停止命令(None)の投入
    for i in range(num_worker_threads):
        q.put(None)
    
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