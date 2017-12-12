#!/usr/bin/env python3

import re, pprint
    from sys import argv

def nullParser(data):
    if data[0 : 4] == "null":
        return (None, data[4 : ].strip())


def booleanParser(data):
    if data[0 : 4] == "true":
        return (True, data[4 : ])
    elif data[0 : 5] == "false":
        return (False, data[5 : ].strip())


def commaParser(data):
    if data[0] == ",":
        return(data[0], data[1 : ].strip())


def colonParser(data):
    if data[0] == ":":
        return(data[0], data[1 : ].strip())


def stringParser(data):
    if data[0] == '"':
        data = data[1 : ]
        next_quote_index = data.index('"')
        while data[next_quote_index - 1] == '\\':
            next_quote_index += data[next_quote_index + 1 : ].index('"') + 1
        return (data[ : next_quote_index], data[next_quote_index + 1 : ].strip())


def numberParser(data):
    if data:
        num_regex = re.findall("^(-?(?:[0-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)", data)
        if not num_regex:
            return None
        index = len(num_regex[0])
        try:
            return (int(num_regex[0]), data[index : ].strip())
        except:
            return (float(num_regex[0]), data[index : ].strip())


def arrayParser(data):
    if data[0] == "[" :
        data = data[1 : ].strip()
        parsed_list = []
        if data[0] == "]":
            return (parsed_list, data[1 : ].strip())
        while len(data):
            result = parser(stringParser, nullParser, booleanParser, numberParser, arrayParser, objectParser, input_data = data)
            if not result:
                return None
            parsed_list.append(result[0])
            data = result[1].strip()
            if data[0] == "]":
                return (parsed_list, data[1 : ].strip())
            result = commaParser(data)
            if not result:
                return None
            data = result[1].strip()


def objectParser(data):
    if data[0] == "{":
        data = data[1 : ].strip()
        parsed_dict = {}
        if data[0] == '}':
            return (parsed_dict, data[1 : ].strip())
        while len(data):
            result = stringParser(data)
            if not result:
                return None
            key = result[0]
            result = colonParser(result[1].strip())
            if not result:
                return None
            data = result[1].strip()
            result = parser(stringParser, nullParser, booleanParser, numberParser, arrayParser, objectParser, input_data = data)
            if not result:
                return None
            parsed_dict[key] = result[0]
            data = result[1].strip()
            if data[0] == '}':
                return (parsed_dict, data[1 : ].strip())
            result = commaParser(data)
            if not result:
                return None
            data = result[1].strip()


def parser(*args, input_data):
    for one_parser in args:
        res = one_parser(input_data)
        if res:
            return res
    return None


def main():
    data = ""
    file_name = argv[1]

    with open(file_name, "r") as file_obj:
        for line in file_obj:
            data += line.strip()

    result = ()
    result = parser(stringParser, nullParser, booleanParser, numberParser, arrayParser, objectParser, input_data = data)
    try:
        if result[1] == '':
            try:
                pprint.pprint(result[0])
            except:
                print(None)
        else:
            print(None)
    except:
        print(None)


if __name__ == '__main__':
    main()