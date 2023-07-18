def buf_count_newlines(fname):
    lines = 0
    buf_size = 2 ** 16
    with open(fname) as f:
        buf = f.read(buf_size)
        while buf:
            lines += buf.count("\n")
            buf = f.read(buf_size)
    return lines

def read_count(fname):
    return open(fname).read().count("\n")

def sum1(fname):
    return sum(1 for _ in open(fname))

def for_open(fname):
    lines = 0
    for _ in open(fname):
        lines += 1
    return lines

# ref: https://stackoverflow.com/a/68385697