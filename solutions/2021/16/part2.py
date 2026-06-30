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
        reader.read(3)  # version
        type_id = reader.read(3)

        if type_id == 4:
            value = 0
            while True:
                if not reader.read(1):
                    value = (value << 4) | reader.read(4)
                    break
                value = (value << 4) | reader.read(4)
            return value

        sub_values: list[int] = []
        if reader.read(1) == 0:
            sub_len = reader.read(15)
            end = reader.pos + sub_len
            while reader.pos < end:
                sub_values.append(parse(reader))
        else:
            for _ in range(reader.read(11)):
                sub_values.append(parse(reader))

        if type_id == 0:
            return sum(sub_values)
        if type_id == 1:
            result = 1
            for v in sub_values:
                result *= v
            return result
        if type_id == 2:
            return min(sub_values)
        if type_id == 3:
            return max(sub_values)
        if type_id == 5:
            return int(sub_values[0] > sub_values[1])
        if type_id == 6:
            return int(sub_values[0] < sub_values[1])
        if type_id == 7:
            return int(sub_values[0] == sub_values[1])
        raise ValueError(f"unknown type {type_id}")

    return str(parse(Reader(bits)))
