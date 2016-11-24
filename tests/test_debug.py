import pydevd
pydevd.settrace('licho.iok.la', port=44957, stdoutToServer=True, stderrToServer=True)

if __name__ == '__main__':
    print("abcde")