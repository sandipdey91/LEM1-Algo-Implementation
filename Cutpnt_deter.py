# Judge if it is a numerical attribute
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# String of symbolic attributes
def concat (lower, upper):
    lower = round(float(lower),4)
    upper = round(float(upper),4)
    return str(lower) + ".."+str(upper)


def generate_cutpoint(attributes_dict={}):
    list_attri = list(attributes_dict.keys())
    for attribute in list_attri:
        if is_number(list(attributes_dict[attribute].keys())[0]):
            if len(attributes_dict[attribute].keys()) == 1:
                value = list(attributes_dict[attribute].keys())[0]
                num_string = concat(value,value)
                attributes_dict[attribute][num_string] = attributes_dict[attribute][value]
                attributes_dict[attribute].pop(value)
            else:
                list_value = sorted(list(attributes_dict[attribute].keys()), key=lambda x: float(x))

                # First one
                num_string = concat(list_value[0], (float(list_value[0])+float(list_value[1]))/2)
                attributes_dict[attribute][num_string] = attributes_dict[attribute][list_value[0]]
                attributes_dict[attribute].pop(list_value[0])

                # Ones in middle
                for i in range(1,len(list_value)-1):
                    num_string = concat(list_value[i], (float(list_value[i]) + float(list_value[i+1])) / 2)
                    attributes_dict[attribute][num_string] = attributes_dict[attribute][list_value[i]]
                    attributes_dict[attribute].pop(list_value[i])

                # Last one
                last = len(list_value)-1
                num_string = concat((float(list_value[last-1]) + float(list_value[last])) / 2, list_value[last])
                attributes_dict[attribute][num_string] = attributes_dict[attribute][list_value[last]]
                attributes_dict[attribute].pop(list_value[last])
