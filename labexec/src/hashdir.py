import os
import hashlib

def hash_directory(path):
    hash_ = hashlib.md5()

    for root, dirs, files in os.walk(path):
        for f in files:
            file = open(os.path.join(root, f), "r")
            while 1:
                buf = file.read(4096)
                if not buf:
                    break
                hash_.update(hashlib.md5(buf).hexdigest())
            file.close()

    return hash_.hexdigest()


if __name__ == '__main__':
    print hash_directory("/Users/luke/programming/labtools/")