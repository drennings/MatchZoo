import shutil
import os
import csv
#import unicode

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
    backupfilepath = filepath[:-4] + "_old" + ".txt"
    if not os.path.exists(backupfilepath):
        print("Did not find a backupfile")
        shutil.copyfile(filepath, backupfilepath)
    else:
        print("Found a backupfile @ " + backupfilepath)

    with open(backupfilepath, "r") as txt_infile:
        with open(filepath, "w") as txt_outfile:
            #writer = csv.writer(tsv_outfile, delimiter=' ', lineterminator='\n')
            for line in txt_infile:
                # read line from backupfilepath
                #print(line)
                label, q_id, doc_id = line.strip().split(" ")
                new_doc_id = doc_id
                doc_id_u = unicode(doc_id, "utf-8")
                #print(label)
                #print(type(q_id))
                #print(doc_id)
                # adapt line if it has axiomatic rels
                if int(label) > 0:
                    #print("Label > 0")
                    #print(q_id)
                    if q_id in all_p_rels.keys():
                        #print(q_id)
                        #print("q_id in p_rels")
                        p_rels_for_q = all_p_rels[q_id]
                        print("Looking for ")
                        print(doc_id_u)
                        print(p_rels_for_q)
                        for doc_id_1,doc_id_2, delta in p_rels_for_q:
                            #print(doc_id_1, doc_id_2, delta)
                            #print(doc_id)
                            if doc_id_2 == doc_id_u:
                                print("Atleast I found a match")
                            if doc_id_1 == doc_id_u:
                                print("found line to add")
                                new_doc_id += ";" + doc_id_1 + ";" + delta
                line_to_write = label + " " + q_id + " " + new_doc_id + "\n"

                # write new line to filepath
                txt_outfile.write(line_to_write)

if __name__ == '__main__':
    path_to_p_rels = "./all_matchzoo_p_rels.tsv"
    infiles = ["./relation_train.txt", "./relation_dev.txt", "./relation_test.txt" ]
    infiles = ["./relation_train.txt"] #only use train file
    q_id = "s"
    all_p_rels = read_all_p_rels(path_to_p_rels)
    print("Found " + str(len(all_p_rels)) + " p_rels")
    for filepath in infiles:
        extend_rel_file_with_p_rels(filepath, all_p_rels)
    #for val in all_p_rels.keys():
    #    print(val)
        #break
    #print(q_id)
    print("Finished extending rel files with axiomatic rels")
