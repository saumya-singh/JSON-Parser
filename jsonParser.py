#!/usr/bin/env python3
import re, pprint
from sys import argv

def nullParser(data):
    if data[0 : 4] == "null":
        return (None, data[4 : ])

def booleanParser(data):
    if data[0 : 4] == "true":
        return (True, data[4 : ])
    elif data[0 : 5] == "false":
        return (False, data[5 : ])

def spaceParser(data):
    if data:
        space_regex = re.match('\s+', data)
        if space_regex:
            return (' ', data[space_regex.end() : ])

def commaParser(data):
    if data[0] == ",":
        return(data[0], data[1 : ])

def colonParser(data):
    if data[0] == ":":
        return(data[0], data[1 : ])

def stringParser(data):
    if data[0] == '"':
        data = data[1 : ]
        next_quote_index = data.index('"')
        while data[next_quote_index - 1] == '\\':
            next_quote_index += data[next_quote_index + 1 : ].index('"') + 1
        return_string = data[ : next_quote_index].replace('\\\\', '\\')
        return (return_string, data[next_quote_index + 1 : ])

def numberParser(data):
    if data:
        num_regex = re.findall("^(-?(?:[0-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)", data)
        if not num_regex:
            return None
        index = len(num_regex[0])
        try:
            return (int(num_regex[0]), data[index : ])
        except:
            return (float(num_regex[0]), data[index : ])

def arrayParser(data):
    if data[0] == "[" :
        data = data[1 : ]
        parsed_list = []
        if data[0] == "]":
            return (parsed_list, data[1 : ])
        while (len(data) > 1):
            result = valueParser(data)
            if result and result[0] == ' ':
                data = result[1]
                try:
                    if data[0] == "]":
                        return (parsed_list, data[1 : ])
                    continue
                except:
                    return "not a valid JSON"
            parsed_list.append(result[0])
            data = result[1]
            res = spaceParser(data)
            if res:
                data = res[1]
            if data[0] == "]":
                return (parsed_list, data[1 : ])
            result = commaParser(data)
            if not result:
                return "not a valid JSON"
            data = result[1]
    return

def objectParser(data):
    if data[0] == "{":
        data = data[1 : ]
        parsed_dict = {}
        if data[0] == '}':
            return (parsed_dict, data[1 : ])
        while len(data):
            result = spaceParser(data)
            if result:
                data = result[1]
            result = stringParser(data)
            if not result:
                return "not a valid parser"
            key = result[0]
            data = result[1]
            result = spaceParser(data)
            if result:
                data = result[1]
            result = colonParser(result[1])
            if not result:
                return "not a valid parser"
            data = result[1]
            result = spaceParser(data)
            if result:
                data = result[1]
            result = valueParser(data)
            if not result:
                return "not a valid parser"
            parsed_dict[key] = result[0]
            data = result[1]
            result = spaceParser(data)
            if result:
                data = result[1]
            if data[0] == '}':
                return (parsed_dict, data[1 : ])
            result = commaParser(data)
            if not result:
                return "not a valid parser"
            data = result[1]
    return

def parser(*args):
    def parserData(data):
        for one_parser in args:
            res = one_parser(data)
            if res:
                return res
    return parserData

valueParser = parser(stringParser, spaceParser, nullParser, booleanParser, numberParser, arrayParser, objectParser)

def main():
    data = ""
    file_name = argv[1]
    with open(file_name, "r") as file_obj:
        data = file_obj.read()
    if len(data) == 0:
        print("Empty File")
        return
        
    result = spaceParser(data)
    if result:
        starting_spaces = result[0]
        data = result[1]
    result = valueParser(data)
    if isinstance(result, tuple):
        if len(result[1]) > 0:
            last_spaces_parsed = spaceParser(result[1]) 
            last_spaces = last_spaces_parsed[0]
            result = (result[0], last_spaces_parsed[1])
    try:
        if result[1] == '':
            if result[0] == ' ':
                print ("Value Error: expecting value...")
                return
            pprint.pprint(result[0])
        else:
            print("not a valid JSON")
    except:
        print("not a valid JSON")
    return

if __name__ == '__main__':
    main()
