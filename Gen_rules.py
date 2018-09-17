from Ip_Datproc import ordering_cond
import copy


class Rule:

    def __init__(self, attributes_dict={}, decision_list=[], covering=[], num_data=0):
        self.num_data = num_data
        self.covering = covering
        self.attributes_dict = attributes_dict
        self.decision_list = decision_list


    def getting_decision(self, case):             # use list
        return self.decision_list[case-1]

    def getting_cond(self, case):           # use dict
        conditions = {}
        for attri in self.covering:
            for value in self.attributes_dict[attri]:
                if case in self.attributes_dict[attri][value]:
                    conditions[attri] = value
        return conditions

  

    def getting_case(self, conditions={}):   # use dict
        data_list = [0] * (self.num_data+1)
        cases = []
        for attri in conditions.keys():
            for case in self.attributes_dict[attri][conditions[attri]]:
                data_list[case] += 1
        for i in range(1, len(data_list)):
            if data_list[i] == len(conditions):
                cases.append(i)
        return cases

    

    def Gen_rules(self):
        ruleset = []
        data_list = [0] * (self.num_data+1)

        for case in range(1, self.num_data+1):
            if data_list[case] == 1:
                continue
            else:
                case_decision = self.getting_decision(case)
                if case_decision == "special":
                    continue
                case_conditions = self.getting_cond(case)
                # Drop conditions
                Q_con = copy.copy(case_conditions)

                # Drop in order
                for attri in ordering_cond(case_conditions.keys()):
                    Q_con.pop(attri)
                    if self.check_consistent(self.getting_case(Q_con), case_decision):
                        case_conditions = copy.copy(Q_con)
                    else:
                        Q_con = copy.copy(case_conditions)
                ruleset.append((case_conditions, case_decision))

                for one in self.getting_case(case_conditions):
                    data_list[one] = 1
        # print(ruleset)
        return ruleset

    def check_consistent(self, cases=[], decision = ""):
        for case in cases:
            if self.getting_decision(case) != decision:
                return False
        return True

