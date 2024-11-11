import sys


def cnf2aag(cnf_path, aag_path=None):
    found_header = False
    cnf_vars = 0
    aag_vars = 0
    aag_opposite_clauses = [] # list of lists, each list represents clause that just need to put "not" on its last gate
    aag_opposite_clauses_last_and_var = []

    with open(cnf_path) as file:
        for line in file:
            splited = line.split(" ")
            if splited[0] == "c" or splited[0] == "c\n":
                continue
            elif splited[0] == "%\n":
                print("Ended because of %")
                break
            elif splited[0] == "p":
                assert splited[1] == "cnf"
                cnf_vars = int(splited[2])
                aag_vars += cnf_vars+1
                found_header = True
            else:
                assert found_header
                clause_ands = []
                literals = [int(literal_str) for literal_str in splited if literal_str!='']
                assert literals[len(literals)-1] == 0
                assert len(literals) > 2

                new_and = aag_vars
                aag_vars += 1
                clause_ands.append([new_and, -literals[0], -literals[1]])
                for i in range(2, len(literals)-1):
                    assert literals[i] != 0
                    old_and = new_and
                    new_and = aag_vars
                    aag_vars += 1
                    clause_ands.append([new_and, old_and, -literals[i]])
                aag_opposite_clauses.append(clause_ands)
                aag_opposite_clauses_last_and_var.append(new_and)

    aag_final_ands = []
    for clause in aag_opposite_clauses:
        for and_gate in clause:
            assert len(and_gate) == 3
            assert and_gate[0] > 0
            first_literal = str(and_gate[0] * 2)
            second_literal = str(and_gate[1] * 2) if and_gate[1] > 0 else str((-and_gate[1]) * 2 + 1)
            third_literal = str(and_gate[2] * 2) if and_gate[2] > 0 else str((-and_gate[2]) * 2 + 1)
            aag_final_ands.append(first_literal+" "+second_literal+" "+third_literal)

    new_and = aag_vars
    aag_vars += 1
    first_literal = str(new_and*2)
    second_literal = str(aag_opposite_clauses_last_and_var[0]*2+1)
    third_literal = str(aag_opposite_clauses_last_and_var[1]*2+1)
    aag_final_ands.append(first_literal+" "+second_literal+" "+third_literal)
    for i in range(2, len(aag_opposite_clauses_last_and_var)):
        old_and = new_and
        new_and = aag_vars
        aag_vars += 1
        first_literal = str(new_and * 2)
        second_literal = str(old_and * 2)
        third_literal = str(aag_opposite_clauses_last_and_var[i] * 2 + 1)
        aag_final_ands.append(first_literal + " " + second_literal + " " + third_literal)

    output_var = new_and

    if aag_path is None:
        aag_path = cnf_path.replace(".cnf", ".aag")

    # Write
    with open(aag_path, "w") as file:
        # Header
        file.write(f"aag {output_var} {cnf_vars} 0 1 {len(aag_final_ands)} \n")

        #Inputs
        for var in range(1, cnf_vars+1):
            file.write(f"{var*2}\n")

        #Outputs
        file.write(f"{output_var*2}\n")

        #Ands
        for and_gate in aag_final_ands:
            file.write(f"{and_gate}\n")

    print("Finished Successfully!")

if __name__ == "__main__":
    cnf2aag("../cnf/uf100-430/uf100-01.cnf")