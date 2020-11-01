import os


class File:
    file = ""

    def __init__(self, file_name):
        self.file_name = file_name

    def isFile(self, file_name):
        if os.path.isfile(file_name):
            return True
        else:
            return False

    def openOrCreate(self):
        if self.isFile(self.file_name):
            with open(self.file_name, "r") as file:
                return file
        else:
            with open(self.file_name, "w+") as file:
                return file

    def readFile(self):
        with open(self.file_name, "r") as reader:
            return reader.read()

    def readLine(self):
        with open(self.file_name, "r") as reader:
            return reader.readline()

    def readLnsFile(self):
        with open(self.file_name, "r") as reader:
            return reader.readlines()

    def writeFile(self, line):
        with open(self.file_name, "a") as wr:
            wr.write(line + "\n")

    def rename(self, old_name, new_name):
        os.rename(old_name, new_name)
