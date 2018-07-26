
class LabeledString(object):
    def __init__(self, label, str):
        self.label = label
        self.str = str

    def __str__(self):
        return self.str


class LineWithSourceMap(object):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return ''.join(map(lambda x: x.str, self.line))

    def __getitem__(self, i):
        curIndex = 0
        curChar = 0
        while curIndex < len(self.line):
            elem = self.line[curIndex]
            curChar += len(elem.str)
            if i < curChar:
                return elem.label
            curIndex += 1
        # If it is past the end of the line, just blame the last element
        if self.line:
            return self.line[-1].label


class StringWithSourceMap(object):
    def __init__(self, lines, lastData):
        self.lines = []
        for l in lines:
            self.lines.append(LineWithSourceMap(l))
        self.lines.append(LineWithSourceMap(lastData))

    def __str__(self):
        return '\n'.join(map(str, self.lines))

    def __getitem__(self, i):
        return self.lines[i]


class LabeledRope(object):
    def __init__(self, strings=[]):
        self.lines = []
        self.lastLine = []
        self.lastLine.extend(strings)

    def append(self, x):
        self.lastLine.append(x)

    def extend(self, x):
        self.lastLine.extend(x)

    def __iadd__(self, x):
        self.append(x)
        return self

    def newline(self):
        self.lines.append(self.lastLine)
        self.lastLine = []

    def result(self):
        return StringWithSourceMap(self.lines, self.lastLine)

    def __str__(self):
        return str(self.result())
