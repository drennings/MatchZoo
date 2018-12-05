print("Multigrading data")
path1 = "./all_p_rels_matchzoo"
path2 = "./WikiPassageQA/"
prepare.save_relation(dstdir + 'relation_train.txt', rel_train)
    prepare.save_relation(dstdir + 'relation_valid.txt', rel_valid)
    prepare.save_relation(dstdir + 'relation_test.txt', rel_test)

