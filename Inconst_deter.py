import copy
import Gen_rules as ru


def deal_inconsistency(attributes_dict, decision_dict, decision_list, attributes_name, num_data):
    possible_dict = {}
    certain_dict = {}
    possible_list = {}
    certain_list = {}
    rule = ru.Rule(attributes_dict, decision_list, attributes_name, num_data)

    # Generate different decision_parset for each concept
    for concept_name in decision_dict.keys():
        concept_case = decision_dict[concept_name]
        possible_cases = copy.copy(concept_case)
        certain_cases = copy.copy(concept_case)
        checklist = [0]*(num_data+1)
        for case in concept_case:
            if checklist[case] == 1:
                continue
            conditions = rule.get_conditions(case)
            cases = rule.get_cases(conditions)
            flag = False
            for item in cases:
                checklist[item] = 1
                if item not in concept_case:
                    flag = True
                    if item not in possible_cases:
                        possible_cases.append(item)
            if flag:
                certain_cases.remove(case)

        dp_dict = {concept_name: [], "special": []}
        dc_dict = {concept_name: [], "special": []}
        dp_list = []
        dc_list = []
        # get decision set of concepts
        for i in range(1, num_data+1):
            if i in possible_cases:
                dp_dict[concept_name].append(i)
                dp_list.append(concept_name)
            else:
                dp_dict["special"].append(i)
                dp_list.append("special")
            if i in certain_cases:
                dc_dict[concept_name].append(i)
                dc_list.append(concept_name)
            else:
                dc_dict["special"].append(i)
                dc_list.append("special")

        possible_dict[concept_name] = dp_dict
        certain_dict[concept_name] = dc_dict
        possible_list[concept_name] = dp_list
        certain_list[concept_name] = dc_list

    return possible_dict, certain_dict, possible_list, certain_list
