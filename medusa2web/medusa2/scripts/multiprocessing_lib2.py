## multi_nuovo


def do_something(data):
    return data * 2

def consumer(inQ, outQ):
    while True:
        try:
            # get a new message
            val = inQ.get()

            # this is the 'TERM' signal
            if val is None:
                break;

            # unpack the message
            pos = val[0]  # its helpful to pass in/out the pos in the array
            data = val[1]

            # process the data
            ret = do_something(data)

            # send the response / results
            outQ.put( (pos, ret) )


        except Exception as e:
            print("error!", e)
            break

def process_data(data_list, inQ, outQ):
    # send pos/data to workers
    for i,dat in enumerate(data_list):
        inQ.put( (i,dat) )

    # process results
    for i in range(len(data_list)):
        ret = outQ.get()
        pos = ret[0]
        dat = ret[1]
        data_list[pos] = dat


def main():
    import multiprocessing as mp
    # initialize things
    n_workers = 4
    inQ = mp.Queue()
    outQ = mp.Queue()
    # instantiate workers
    workers = [mp.Process(target=consumer, args=(inQ,outQ))
               for i in range(n_workers)]

    # start the workers
    for w in workers:
        w.start()

    # gather some data
    data_list = [ d for d in range(1000)]

    # lets process the data a few times
    for i in range(4):
        process_data(data_list)

    # tell all workers, no more data (one msg for each)
    for i in range(n_workers):
        inQ.put(None)
    # join on the workers
    for w in workers:
        w.join()

    # print out final results  (i*16)
    for i,dat in enumerate(data_list):
        print(i, dat)

###############################

def process_data(data_list, inQ, outQ,nworker):
    # send pos/data to workers
    for i,dat in enumerate(data_list):
        inQ.put( (i,dat) )


    # process results
    for i in range(len(data_list)):
        ret = outQ.get()
        pos = ret[0]
        dat = ret[1]
        data_list[pos] = dat



def main2():
    import multiprocessing as mp
    # initialize things
    n_workers = 4
    inQ = mp.Queue()
    outQ = mp.Queue()

    # instantiate workers
    workers = [mp.Process(target=consumer, args=(inQ,outQ))
               for i in range(n_workers)]

    # start the workers
    for w in workers:
        w.start()

    # gather some data
    data_list = [ d for d in range(1000)]

    # lets process the data a few times
    process_data(data_list,inQ,outQ)

    # tell all workers, no more data (one msg for each)
    for i in range(n_worker): inQ.put(None)

    # join on the workers
    for w in workers: w.join()

    # print out final results  (i*16)
    for i,dat in enumerate(data_list):
        print(i, dat)





def wrapper(fxn,args,dataGen,threads=1):
    """ wrap fxn with a Process-paradigm multithread """


