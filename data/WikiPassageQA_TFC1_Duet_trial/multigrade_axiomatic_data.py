import shutil
import os

def read_all_p_rels(path_to_prels):
    all_p_rels = {}

    with open(path_to_prels, "r") as tsv_file:
        for line in tsv_file:
            line = line.strip().split("\t")
            if len(line) < 2:
                continue
            q_id = line[0]
            p_rels_string = line[1]

            p_rels_for_q = []
            for p_rel in p_rels_string.split(";"):
                #print(p_rel)
                p_rels_for_q.append(tuple(p_rel[1:-1].replace("'", "").split(", ")))

            all_p_rels[q_id] = p_rels_for_q

    return all_p_rels

def extend_rel_file_with_p_rels(filepath, all_p_rels):
    # create a backup if we don't have one yet
    backupfilepath = filepath[-4] + "_old" + ".txt"
    if not os.path.exists(backupfilepath):
        shutil.copyfile(filepath, backupfilepath)

    with open(backupfilepath, "r") as tsv_infile:
        with open(filepath, "w") as as tsv_outfile:

            for line in tsv_file:
                # read line from backupfilepath
                label, q_id, doc_id = line.strip().split("\t")
                new_doc_id = doc_id

                # adapt line if it has axiomatic rels
                if doc_id > 0:
                    if q_id in all_p_rels:
                        p_rels_for_q = all_p_rels[q_id]
                        for doc_id_1,doc_id_2, delta in p_rels_for_q:
                            if doc_id_1 == doc_id:
                                new_doc_id += ";" + doc_id_1 + ";" + delta
                line_to_write = [label, q_id, new_doc_id]

                # write new line to filepath
                writer.writerow(line_to_write)

if __name__ == '__main__':
    path_to_p_rels = "./all_p_rels_matchzoo"
    infiles = ["./relation_train.txt", "./relation_dev.txt", "./relation_test.txt" ]
    infiles = ["./relation_train.txt"] #only use train file

    all_p_rels = read_all_p_rels(path_to_p_rels)

    for filepath in infiles:
        extend_rel_file_with_p_rels(filepath, all_p_rels)

    print("Finished extending rel files with axiomatic rels")
