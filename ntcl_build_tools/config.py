import os.path

class Config (object):
    @classmethod
    def from_file(cls, filename):
        if not os.path.isfile(filename): return {}
        return {key.strip():value.split() for key, value in (cls.normalize(line).split('=') for line in open(filename, 'r') if cls.is_valid(line))}

    @staticmethod
    def normalize(line):
        return line.split('#')[0].strip()

    @classmethod
    def is_valid(cls, line):
        return len(cls.normalize(line).split('=')) == 2
