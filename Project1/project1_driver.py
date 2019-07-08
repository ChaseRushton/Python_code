import project1_functions as p1f

sequence1, sequence2 = p1f.Get_Sequences("human_hemoglobin_alpha.fasta.txt", "mouse_hemoglobin_alpha.fasta.txt")
BLOSUM_matrix = p1f.Build_Scoring_Matrix("BLOSUM62.txt")

SW_sequence1, SW_sequence2, SW_score = p1f.Smith_Waterman(sequence1, sequence2, BLOSUM_matrix)
NW_sequence1, NW_sequence2, NW_score = p1f.Needleman_Wunsch(sequence1, sequence2, BLOSUM_matrix)

print
print "SMITH-WATERMAN:"
p1f.Output_Sequences(SW_sequence1, SW_sequence2, SW_score, BLOSUM_matrix)
print "NEEDLEMAN-WUNSCH:"
p1f.Output_Sequences(NW_sequence1, NW_sequence2, NW_score, BLOSUM_matrix)