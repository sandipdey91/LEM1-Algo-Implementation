import copy


class Partition:
    def __init__(self, aset={}, length=0):
        # Initialization
        self.length = length
        self.matrix = {}
        if len(aset) != 0:    # Intial with a set
            for ii in range(1, length):
                self.matrix[ii] = {}
                for jj in range(ii+1, length+1):
                    self.matrix[ii][jj] = True

            # Calculate partition matrix
            for brace in aset.values():
                for i in range(len(brace)):
                    item = brace[i]
                    for j in range(i+1, len(brace)):
                            self.matrix[item][brace[j]] = False
        else:   # Inital without data
            for ii in range(1, length):
                self.matrix[ii] = {}
                for jj in range(ii+1, length+1):
                    self.matrix[ii][jj] = False

    def print_matrix(self):
        print(self.matrix)

    def merge(self, one):
        if self.length == one.length:
            newone = Partition({}, self.length)
            for i in range(1,self.length):
                for j in range(i+1, self.length+1):
                    if self.matrix[i][j] or one.matrix[i][j] :
                        newone.matrix[i][j] = True
            return newone
        else:
            print("Trying to merging to sets with different length.")
            return None

    def is_smaller(self, one):
        for i in range(1, self.length):
            for j in range(i + 1, self.length + 1):
                if (not self.matrix[i][j]) and one.matrix[i][j]:
                    return False
        # self is smaller than one
        return True


def merging_part(sets={}, length=0):
    if len(sets.values()) == 0:
        print("No partitions to  merge.")
        return None
    else:
        merging = Partition({}, length)
        for par_i in sets.values():
            merging = merging.merge(par_i)
            if merging is None:
                break
        return merging


def global_cov_finding(a_list=[], a_par={}, d_par={}, length=0):
    cover = copy.copy(a_list)
    Q_par = copy.copy(a_par)
    P_par = copy.copy(a_par)

    for attri in a_list:
        Q_par.pop(attri)
        if len(Q_par) == 0:
            break
        # print("Q", Q_par.keys())
        Q_merge = merging_part(Q_par, length)
        if Q_merge.is_smaller(d_par):
            # print("remove", attri)
            cover.remove(attri)
            P_par = copy.copy(Q_par)
        else:
            Q_par = copy.copy(P_par)

    return cover



