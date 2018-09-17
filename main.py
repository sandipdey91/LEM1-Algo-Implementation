import Ip_Datproc as inpda
import Gen_rules as rulgen
import Inconst_deter as inconst
from Cutpnt_deter import generate_cutpoint
import Partn_cal as parcal

import time

attribute_data = {}
decision_datas = {}
decision_lists = []
attribute_count = len(inpda.attr_nm)

for item in inpda.attr_nm:
    attribute_data[item] = {}


num = 1
for line in inpda.data:
    # In case there is line is just a '\n'
    if len(line) < attribute_count:
        break
    for i in range(len(inpda.attr_nm)):
        if line[i] in attribute_data[inpda.attr_nm[i]].keys():
            attribute_data[inpda.attr_nm[i]][line[i]].append(num)
        else:
            attribute_data[inpda.attr_nm[i]][line[i]] = [num]
    if line[i+1] in decision_datas:
        decision_datas[line[i+1]].append(num)
    else:
        decision_datas[line[i+1]] = [num]
    decision_lists.append(line[-1])
    num += 1
num_data = num-1
generate_cutpoint(attribute_data)

dec_part_set = parcal.Partition(decision_datas, num_data)

attr_part_set = {}
for attribute in attribute_data.keys():
    attr_part_set[attribute] = parcal.Partition(attribute_data[attribute], num_data)

print("Number of cases:", num_data)

start = time.time()

partition_A = parcal.merging_part(attr_part_set, num_data)

if partition_A.is_smaller(dec_part_set):
# If consistent
    print("! Possible rule set is not shown since it is identical with the certain rule set")
    # single global convering
    covering = parcal.global_cov_finding(inpda.attr_nm, attr_part_set, dec_part_set, num_data)
    # a ruleset
    ruleset = rulgen.Rule(attribute_data, decision_lists, covering, num_data).Gen_rules()
    # Output 
    output_file = open(inpda.out_name+".certain.r", 'w')
    output_file.write(inpda.print_ruleset(ruleset))
    output_file.close()

    print("The Global covering is:", covering)
   
    print("Saved file",inpda.out_name+".certain.r")

# Not consistent
else:
    print("Inconsistent.")

    # Get different decision and covering sets of concepts
    possible_dict, certain_dict, possible_list, certain_list =\
       inconst.deal_inconsistency(attribute_data, decision_datas, decision_lists, inpda.attr_nm, num_data)

    # Possible
    output_file = open(inpda.out_name + ".possible.r", 'w')
    for dp_dict_key in possible_dict.keys():
        dp_dict = possible_dict[dp_dict_key]
        dp_list = possible_list[dp_dict_key]
        dp_parset = parcal.Partition(dp_dict, num_data)

        # get a single global convering
        covering = parcal.global_cov_finding(inpda.attr_nm, attr_part_set, dp_parset, num_data)

        # get ruleset
        ruleset = rulgen.Rule(attribute_data, dp_list, covering, num_data).Gen_rules()

        output_file.write(inpda.print_ruleset(ruleset))
        # Printing
        print("Possible:", dp_dict_key, "\tA single global covering:",covering)
        
    output_file.close()

    # Certain
    output_file = open(inpda.out_name + ".certain.r", 'w')
    for dc_dict_key in certain_dict.keys():
        dc_dict = certain_dict[dc_dict_key]
        dc_list = certain_list[dc_dict_key]
        dc_parset = parcal.Partition(dc_dict, num_data)

        # get a single global conering
        covering = parcal.global_cov_finding(inpda.attr_nm, attr_part_set, dc_parset, num_data)

        # get ruleset
        ruleset = rulgen.Rule(attribute_data, dc_list, covering, num_data).Gen_rules()

        output_file.write(inpda.print_ruleset(ruleset))
        # Printing
        print("Certain :", dc_dict_key, "\tA single global covering:", covering)
      
    output_file.close()
    print("Saved file", inpda.out_name + ".certain.r and",inpda.out_name + ".possible.r")

end = time.time()
timer = end - start
print("Time taken", timer, "seconds.")

