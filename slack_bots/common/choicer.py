import os
import random


class RandomChoicer:

    def __init__(self, filename, base_dir='data', cache_dir='cache'):
        self.file = os.path.abspath(os.path.join(base_dir, filename))
        cache_file = os.path.abspath(os.path.join(cache_dir, filename))
        self.cache_file = os.path.join(os.path.dirname(cache_file), 'used.' + os.path.basename(cache_file))

    def select(self):
        # TODO: Make thread safe
        possible = set(read_all_lines(self.file))
        used = set(read_all_lines(self.cache_file))
        variants = possible - used
        if not variants:
            variants = possible
            used = set()
        selected = random.choice(tuple(variants))
        used.add(selected)
        write_all_lines(self.cache_file, used)
        return selected

    def save_cache(self, cached):
        write_all_lines(self.cache_file, cached)


def read_all_lines(file_name):
    with open(file_name) as f:
        all_lines = [x.strip() for x in f]
    return filter(None, all_lines)


def write_all_lines(filename, lines):
    with open(filename, 'w') as f:
        for l in lines:
            f.write(l)
