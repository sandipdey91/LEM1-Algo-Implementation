
data = []
attr_nm = []
decision_name = ""


def read_data(inputfile=None):
    datas = []
    attributesname = []
    decisionname = ""
    try:
        inputfile.readline()
        lines = inputfile.readline().split()
        if lines[0] == "[":
            attributesname = lines[1:len(lines) - 2]
            decisionname = lines[-2]
        for line in input_file.readlines():
            if line[0] == '!':  # Comment 
                break
            datas.append(line.split()[0:])
        return datas, attributesname, decisionname
    except:
        print("Error in reading data")
        exit()

flag = True
while flag:
    try:
        input_name = input("Give i/p file name, eg:\"data.txt\"\n")
        input_file = open(input_name, 'r')
        data, attr_nm, decision_name = read_data(input_file)
        flag = False
        input_file.close()
    except:
        print("Input file could not be opened")

out_name = input("Give o/p file name, eg:\"rule.d\"\n")


# sort the conditions
def ordering_cond(attributes = []):
    # Order the conditions
    order = {}
    orderlist = []
    for attri in attributes:
        order[attr_nm.index(attri)] = attri
    for i in sorted(order.keys()):
        orderlist.append(order[i])
    return orderlist


# generate the output string
def print_ruleset(ruleset=[]):
    string = ""
    for rule in ruleset:
        # Condition
        flag = False

        # Generate the string
        catstr = ""
        for attri in ordering_cond(rule[0].keys()):
            if flag:
                catstr += " & "
            flag = True
            catstr += "(" + attri +", "+ rule[0][attri] + ")"
        catstr += " -> " +"("+ decision_name +", "+rule[1]+")\n"
            
        string += catstr
    return string
