import sys
import argparse
import pathlib
from enum import StrEnum

parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=pathlib.Path)

args = parser.parse_args()

class MODE(StrEnum):
    NONE = ""
    FIELD = "field"
    VIRTUAL = "virtual"

CLASS_KEY = "class"

def main():
    current_mode = MODE.NONE

    typedeffed = []
    HEADER_WARNING = "### THIS FILE IS GENERATED\n"

    with open(args.filepath, "r") as fd:
        data = fd.read()

        do = -1
        while True:
            class_offset = data.find(f"{CLASS_KEY} ", do+1)
            if class_offset == -1:
                break
            do = class_offset

            # Check if we are in a short comment
            line_start = data.rfind("\n", 0, class_offset) + 1
            line_end = data.find("\n", line_start)

            line = data[line_start:line_end].strip()
            if line.startswith("//"):
                continue

            # Check if we are in a long comment
            c_start = data.rfind("/*", 0, class_offset) + 1
            if c_start != -1:
                # Found a start, lets find the end and see if we match
                c_end = data.find("*/", c_start)
                if c_start < class_offset and class_offset < c_end:
                    # we are in a comment
                    continue


            class_offset_end = class_offset + len(CLASS_KEY)

            name_start = class_offset_end
            while data[name_start].isspace():
                name_start += 1

            name_end = name_start + 1
            while data[name_end].isalnum( ):
                name_end += 1

            class_name = data[name_start:name_end]

            b_start = name_end
            while data[b_start].isspace():
                b_start += 1

            if data[b_start] == ";":
                # Its a forward declaration
                r  = f"struct {class_name};"
                if class_name not in typedeffed:
                    r += f"\ntypedef struct {class_name} {class_name};"
                    typedeffed.append(class_name)

                data = \
                    data[0:class_offset] + \
                    r + \
                    data[b_start+1:]

                continue
            elif data[b_start] != "{":
                raise Exception(f"Found {data[b_start]} expected '{{'")

            b_end = b_start + 1
            b_depth = 1

            while b_depth > 0:
                if data[b_end] == '{':
                    b_depth += 1
                elif data[b_end] == "}":
                    b_depth -= 1

                b_end += 1

            body = data[b_start:b_end]

            for access_specifier in ("public", "protected", "private"):
                body = body.replace(access_specifier+":", "")

            attributes = []
            vmethods = []
            members = body[1:-1].split(";")
            for member in members.copy():
                smember = member.strip()
                if not smember:
                    continue

                if "(" in smember:
                    if "virtual" in smember:
                        vmethods.append(member)
                    continue

                attributes.append(member)

            if vmethods:
                for i, m in enumerate(vmethods):
                    a = m.index("(")
                    name_end = a
                    name_start = name_end
                    while m[name_start-1].isalnum():
                        name_start -= 1

                    tinfo = m[0:name_start].replace("virtual", "").strip()
                    name = m[name_start:name_end]
                    e = m.index(")")+1

                    vmethods[i] = \
                        tinfo + \
                        f"(*{name})" + \
                        m[name_end:e]

                vtable = \
                    "struct {\n" + \
                    "\n".join([x.strip()+";" for x in vmethods]) + \
                    "\n}* vtable\n"

                attributes.insert(0, vtable)

            newbody = \
                "{\n" + \
                "".join([x.strip()+"; " for x in attributes]) + \
                "\n}"

            r  = f"struct {class_name} {newbody};"
            if class_name not in typedeffed:
                r += f"\ntypedef struct {class_name} {class_name};"
                typedeffed.append(class_name)
            
            data = \
                data[0:class_offset] + \
                r + \
                data[b_end+1:]

        print(data)

if __name__ == "__main__":
    main()
