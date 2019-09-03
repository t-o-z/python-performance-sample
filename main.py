import threading
import queue
import time

commonList=[]
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
        
        commonList.append((item.ID,sum(item.values)))
        q.task_done()

def main():
    global q
    global commonList
    num_worker_threads = 5
    test_data_num = 100000
    print(f'Data set: {test_data_num}')

    """
    テストデータをセットする
    """
    threadItem = []
    set_data_start = time.time()
    for i in range(test_data_num):
        threadItem.append(Job([1,2,3],0))

    set_data_time = time.time() - set_data_start
    print (f'Set test data elapsed_time:{format(set_data_time)} [sec]')

    """
    スレッドを立てる
    """
    threads=[]
    thread_start = time.time()
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    thread_start_elapsed_time = time.time() - thread_start
    print (f'Thread start elapsed_time:{format(thread_start_elapsed_time)} [sec]')    

    """
    Queueへテストデータを詰める(Workerにて順次処理している)
    """
    process_start = time.time()
    queueing_start = time.time()
    for item in threadItem:
        q.put(item)
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