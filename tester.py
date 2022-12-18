import subprocess
import os
import json
import io
import __main__
path = os.path.join(os.getcwd(),"test")
dir_list = os.listdir(path)
test = []
stdout = []

PASSED = "dyk1"
FAILED = 'dxk1'

ignore = [ 
    "exp_res.json",
    ".browser",
    "tester.py"
]
print(ignore)

expected = json.load(open(os.path.join(path,"exp_res.json")))
DEBUG = True

class TextPipe:
        def __init__(self, *args, **kwds):
            self.args = args
            self.kwds = kwds
        def wrap_pipe(self, pipe):
            return io.TextIOWrapper(pipe, *self.args, **self.kwds)

def outcollect(stout: bytes):
    stdout.append(stout)
    
def dumpcollect():
    with open("dumps.txt", "w", encoding="UTF-8") as f:
        json.dump(stdout,f)

def def_print(status,output):
    if status:
        print(f"Test Run success at {output}")
        return PASSED
    else:
        print(f"Test returned Error at {output}")
        return FAILED
def tester():
    for file in dir_list:
        s = None
        if file in ignore:
            continue
        elif file in [expf.get("name") for expf in expected.get("tests")]:
            try:
                target = os.path.join(path,file)
                stat = subprocess.Popen(["python", target],stdout=subprocess.PIPE, encoding="utf-8")
                outcollect(stat.communicate()[0])
                if stat.returncode == 0:
                    s = def_print(True,file)
                else:
                    s = def_print(False,file)
            except subprocess.CalledProcessError as e:
                s = def_print(False,file)
            finally:
                for exp in expected.get("tests"):
                    if exp.get("name") == file:
                        print(exp.get("res"))
                        test.append(s == exp.get("res")) # expecting pass
                        assert s == exp.get("res") # expecting pass
                        break
                else:
                    assert False # Did you configure exp_res.json properly?
    else:
        for n, each_iter in enumerate(test):
            if each_iter:
                print(f"Test#{n+1} PASS")
            else:
                print(f"Test#{n+1} FAIL")
        if all(test):
            print("Test Success!")
        else:
            print(f"%s/%s succeeded"%(test.count(True),len(test)))
        assert all(test)  == True
if __name__ == "__main__":
    try:
        tester()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    finally:
        dumpcollect()
