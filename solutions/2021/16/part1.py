def solve(data: str) -> str:
    bits = bin(int(data.strip(), 16))[2:].zfill(len(data.strip()) * 4)

    class Reader:
        def __init__(self, s: str) -> None:
            self.s = s
            self.pos = 0

        def read(self, n: int) -> int:
            val = int(self.s[self.pos : self.pos + n], 2)
            self.pos += n
            return val

    def parse(reader: Reader) -> int:
        version = reader.read(3)
        type_id = reader.read(3)
        total = version

        if type_id == 4:
            while reader.read(1):
                reader.read(4)
            reader.read(4)
        else:
            if reader.read(1) == 0:
                sub_len = reader.read(15)
                end = reader.pos + sub_len
                while reader.pos < end:
                    total += parse(reader)
            else:
                for _ in range(reader.read(11)):
                    total += parse(reader)

        return total

    return str(parse(Reader(bits)))
