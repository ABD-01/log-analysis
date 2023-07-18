import numlines
from timeit import default_timer as timer
import perfplot

class benchmark(object):

    def __init__(self, msg, fmt="%0.3g"):
        self.msg = msg
        self.fmt = fmt

    def __enter__(self):
        self.start = timer()
        return self

    def __exit__(self, *args):
        t = timer() - self.start
        print(("%s : " + self.fmt + " seconds") % (self.msg, t))
        self.time = t


file_name = "OVERNIGHT_MASTER_5JUL7.40"

def setup(n):    
    fname = "t.txt"
    with open(fname, 'w') as f:
        for i in range(n):
            f.write(f'{i+1: 6d} [2023-07-05 20:37:07.294] INFO:  [NET] GSM_TX(119): |vltdata=NRM86433705967909301L1050723203655018.465788N073.782837E4040661BB40012D0400001.22329.4010011111S0587.38BSNL 3\n')
    return fname

with benchmark("buf_count_newlines"):
    a = numlines.buf_count_newlines(file_name)


with benchmark("read_count"):
    b = numlines.read_count(file_name) 

with benchmark("sum1"):
    c = numlines.sum1(file_name)

with benchmark("for_open"):
    d = numlines.for_open(file_name)

print(a,b,c,d)

e = perfplot.bench(
    setup=setup,
    kernels=[
        numlines.buf_count_newlines,
        numlines.read_count,
        numlines.sum1,
        numlines.for_open
    ],
    n_range=[2 ** k for k in range(21)],
    xlabel="num lines",
)
e.save("out.png")
e.show()