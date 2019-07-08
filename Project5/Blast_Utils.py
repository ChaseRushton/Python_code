import subprocess
import os
import sys
from multiprocessing import Pool
import External_Feature_Extraction as efe

def Blast_Directory_Parallel(fasta_dir, blast_dir, nr_dir):
    p = Pool(4)
    args = [blast_dir, "-d", nr_dir, "-j", "3", "-b", "1", 
             "-a", "4", "-i", "test.fa", "-Q", "test.pssm"]
    all_args = []
    for file in os.listdir(fasta_dir):
        if ".fa" in file:
            fa_filename = fasta_dir + file
            pssm_filename = fasta_dir + file[:-6] + ".pssm"
            args[10] = fa_filename
            args[12] = pssm_filename
            all_args.append(args[:])
    p.map(_Blast_Directory, all_args)

def _Blast_Directory(args):
    print "Blasting: '{}' ...".format(args[12])
    FNULL = open(os.devnull, 'w')
    subprocess.call(args, stdout=FNULL)

def Extract_Features(pssm_dir):
    """
    Helper function for generating the dataset file
    :param sequences: list of proten sequences
    :return: return the extracted features from the sequences
    """
    for file in os.listdir(pssm_dir):
        if ".pssm" not in file:
            continue
        if os.path.exists(pssm_dir + file[:-5] + ".features"):
            continue
        feature_vectors = []
        gnb_pssm, lin_reg_vals = Get_PSSM(pssm_dir + file)
        feature_vectors.append(lin_reg_vals)
        with open(pssm_dir + file[:-5] + ".features", "w") as feature_file:
            pass
            # for i in range(sequence_length-6):
            #     for j in range(i + 5, sequence_length):
            #         if (i,j) in contact_points:
            #             label = 1
            #         else:
            #             label = 0
            #         index_i = i + 2
            #         index_j = j + 2
            #         i_features = gnb_pssm[index_i-2:index_i+3]
            #         j_features = gnb_pssm[index_j-2:index_j+3]
            #         i_flat = [item for sublist in i_features for item in sublist]
            #         j_flat = [item for sublist in j_features for item in sublist]
            #         i_str = ",".join(i_flat)
            #         j_str = ",".join(j_flat)
            #         if len(i_str) == 0 or len(j_str) == 0:
            #             import pdb
            #             pdb.set_trace()
            #             print file[:-5]
            #         feature_file.write("{},{},{}\n".format(label, i_str, j_str))


def Get_PSSM(blast_output):

    lin_reg_matrix = []
    
    all_gnb_features = []
    amino_acid_features = []
    amino_acid_features.extend([-1.0 for _ in range(20)])
    amino_acid_features.extend([-1.0 for _ in range(20)])
    
    with open(blast_output, 'r') as pssm_file:
        start_read = False
        for line in pssm_file:
            if "Lambda" in line:
                break
            line = line.strip()
            if line == "":
                continue
            line = line.split()
            if line[0] == "1":
                start_read = True
            if start_read:
                scores = [float(x) for x in line[2:22]]
                amino_acid_features.extend(scores)
                if len(amino_acid_features) == 100:
                    all_gnb_features.append(amino_acid_features)
                    amino_acid_features = amino_acid_features[20:]

                lin_reg_vals = line[22:42]
                lin_reg_matrix.append(lin_reg_vals)
        amino_acid_features.extend([-1.0 for _ in range(20)])
        all_gnb_features.append(amino_acid_features)
        amino_acid_features = amino_acid_features[20:]
        amino_acid_features.extend([-1.0 for _ in range(20)])
        all_gnb_features.append(amino_acid_features)

        lin_reg_matrix = average_PSSM_Weights(lin_reg_matrix)    
    return [all_gnb_features], lin_reg_matrix



def Get_Contact_Points(rr_filename):
    contact_points = set()
    with open(rr_filename, "r") as rr_file:
        start_read = False
        for line in rr_file:
            if not start_read:
                start_read = True
                sequence_length = len(line.strip())
                continue
            line = line.strip().split(" ")
            i = int(line[0]) - 1
            j = int(line[1]) - 1
            contact_points.add((i,j))
    return contact_points, sequence_length

def average_PSSM_Weights(matrix):

    average_weights = []

    row_length = len(matrix[0])
    matrix_length = len(matrix)

    for column in range(row_length):
        vals = []
        for row in range(matrix_length):
            val = matrix[row][column]
            vals.append(int(val))
        avg = sum(vals) / len(vals)
        avg = avg / float(100)
        average_weights.append(avg)

    return average_weights

if __name__ == "__main__":
    blast_dir = "../../blast/bin/blastpgp"
    nr_dir = "../../nr/nr"
    #Blast_Directory_Parallel("data/", blast_dir, nr_dir)
    Extract_Features("data/")        
