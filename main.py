import time
import concurrent.futures
from collections import deque

commonList = set()
q = deque()

def task(item):
    """
    タスク
    """
    global commonList    
    commonList.add((item.ID,sum(item.values)))

def main():
    global q
    global commonList
    num_workers = None # os.cpu_count()
    test_data_num = 5000000
    print(f'Data set: {test_data_num}')
    print(f'Max worker num: {num_workers}')

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
    処理開始
    """
    process_start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.map(task) for x in range(test_data_num)]

        for future in concurrent.futures.as_completed(futures):
            print(future.result()) 

    process_time = time.time() - process_start
    print (f'Process all data elapsed_time:{format(process_time)} [sec]')
    
class Job():
    #xはリスト,yは書き込み先のリストのインデックス
    def __init__(self,x,y):
        self.values=x.copy()
        self.ID=y

if __name__ == '__main__':
    main()