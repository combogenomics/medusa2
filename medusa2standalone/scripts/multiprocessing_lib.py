from multiprocessing import Pool
import time
from time import sleep
from IPython import embed
import logging,functools

"""
def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    pool = Pool(processes=4)

        # print "[0, 1, 4,..., 81]"
    print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
    for i in pool.imap_unordered(f, range(10)):
        print(i)

    # evaluate "f(10)" asynchronously
    res = pool.apply_async(f, [10])
    print(res.get(timeout=1))
             # prints "100"

    # make worker sleep for 10 secs
    res = pool.apply_async(sleep, [10])
    embed()
    print(res.get(timeout=1))             # raises multiprocessing.TimeoutError
    # exiting the 'with'-block has stopped the pool
"""

def fxn_wrapper(args_):
    args__,kwargs__ = args_
    fxn = kwargs__['fxn']
    if 'logging_info' in kwargs__: logging.info(kwargs__['logging_info'])
    return fxn(*args__,**kwargs__)

def poolWrapper(n_threads,iterable_args):
    pool = Pool(processes=n_threads)
    logging.debug("Spawning a pool of %s workers to do the job..." %n_threads)
    res = [i for i in pool.map(fxn_wrapper,iterable_args)]
    return res

def poolWrapperGen(n_threads,iterable_args):
    pool = Pool(processes=n_threads)
    logging.debug("Spawning a pool of %s workers to do the job..." %n_threads)
    for res in  pool.imap(fxn_wrapper,iterable_args): yield res

def provaFun(inp,**kwargs):
    sleep(1)

def check(inputs = range(100)):
    inputs = range(100)
    print("prova senza multiprocessing...")
    start = time.time()
    map(provaFun,inputs)
    print("tempo senza multiprocessing: %s" %(time.time() - start))

def check2(inputs = range(100)):
    print("prova con multiprocessing...")
    start2 = time.time()
    iterable_mummer_args = [(            ([i]),
                        {'fxn':provaFun}
                    ) for i,c in enumerate(inputs)]


    poolWrapper(5,iterable_mummer_args)
    print( "tempo con multiprocessing: %s" %(time.time() - start2))
