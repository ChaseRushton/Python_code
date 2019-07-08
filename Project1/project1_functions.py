from NeedlemanWunsch import NeedlemanWunsch

def Get_Sequences(file_1, file_2):
    """
	Reads sequences from the two input files

	Args:
		file_1: The name of the file containing the first sequence
		file_2: The name of the file containing the second sequence

	Returns:
		Returns the two sequences in a tuple of the form (str, str)

	"""

    file1 = open(file_1, "r")
    file2 = open(file_2, "r")

    # get only the sequence letters, initially this will be a list of different sets
    # of letters due to the line breaks in the .txt file
    with file1 as f:
        seq_1 = f.read().splitlines()

    with file2 as f:
        seq_2 = f.read().splitlines()

    file1.close()
    file2.close()

    # in case the .txt files has empty lines above the first ">" line
    seq_i = 0
    for x in range(len(seq_1)):
        if seq_1[x][0:1:] == ">":
            seq_i = x
    seq_i += 1
    seq_1 = seq_1[seq_i::]

    seq_2_i = 0
    for x in range(len(seq_2)):
        if seq_2[x][0:1:] == ">":
            seq_2_i = x
    seq_2_i += 1
    seq_2 = seq_2[seq_2_i::]

    # concatenate the strings of hemoglobin codes to one sequence
    sequence_1 = ""
    sequence_2 = ""

    for s in seq_1:
        sequence_1 += s

    for s in seq_2:
        sequence_2 += s

    # set the human and mouse sequences to a tuple called sequences
    sequences = (sequence_1, sequence_2)

    # return the tuple of sequences
    return sequences


def Build_Scoring_Matrix(file_1):
    """
	Builds the BLOSUM scoring matrix from the input file

	Args:
		file_1: The name of the file containing the BLOSUM matrix

	Returns:
		Returns a dictionary of the form BLOSUM_dict[(str, str)] = int

	"""
    """
    1. Create list of proteins in matrix in order
    2. Extract BLOSUM62 values in the matrix into an int array
    3. Assign a tuple to each value in the matrix in a dictionary
    4. Return the dictionary
    """
    # list of proteins used in the BLOSUM62 matrix
    protiens = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y',
                'V', 'B', 'Z', 'X', '*']

    file = open(file_1, "r")
    with file as f:
        m = f.read().splitlines()[7::]

    file.close()
    # reformat the matrix
    for x in range(len(m)):
        m[x] = m[x].split()[1::]

    # dimensions of blosum62 matrix
    dim = len(protiens)

    # create dictionary we're returning with appropriate key-value pairs
    blosum_dict = {}
    for row in range(dim):
        for column in range(dim):
            tup = (protiens[row], protiens[column])
            val = int(m[row][column])
            blosum_dict[tup] = val

    return blosum_dict


def Smith_Waterman(sequence_1, sequence_2, scoring_matrix):
    """
	Smith-Waterman algorithm

	Args:
		sequence_1: The first sequence
		sequence_2: The second sequence
		scoring_matrix: The matrix to determine the score of alignments

	Returns:
		Returns the two aligned sequences and the score in a tuple of the form (str, str, int)
	"""

    # initialize scoring matrix
    blosum_dict = scoring_matrix

    # Build the matrix
    h = len(sequence_1) + 1
    w = len(sequence_2) + 1

    def build_sw_matrix(w, h):
        """
        1. Initialize a matrix of size (len(sequence1) + 1) X (len(sequence2) + 1) with zeroes
        2. For each cell past the first column and row calculate the score of that position in the matrix
        using the blosum dictionary
        3. Set that cell position with the calculated score
        4. Return the matrix
        """
        # initialize matrix size with all zeroes
        matrix = [[0 for c in range(w)] for r in range(h)]

        # calculate and fill cell values
        for i in range(1, h):
            for j in range(1, w):
                dict_val = blosum_dict[(sequence_1[i - 1], sequence_2[j - 1])]
                l = matrix[i - 1][j] - 4  # left cell
                u = matrix[i][j - 1] - 4  # above cell
                u_l = matrix[i - 1][j - 1] + dict_val  # upper-left cell
                score = max(l, u, u_l, 0)  # return largest of values. if 0 is biggest, return that
                cell_val = score
                matrix[i][j] = cell_val
        return matrix

    def get_start_pos(sw_matrix):
        """
        Look through the Smith-Waterman matrix to find the largest value and return the
        position of the largest value
        """
        max = 0
        for i in range(h):
            for j in range(w):
                val = sw_matrix[i][j]
                if val > max:
                    start_x = i
                    start_y = j
                    max = val
        return start_x, start_y

    def backtrack(sw_matrix, start_pos):
        """
        Start the backtrack at the starting position, which is the cell in the Smith_Waterman matrix
        that contains the largest value in the matrix. From there, compare the upper-left, upper, and
        left cell values to determine the best possible path. Once the first 0 is hit in the backtracking
        process, we're done. Return the two aligned sequences.
        """
        # print_matrix(sw_matrix, h, sequence_1, sequence_2)
        i, j = start_pos
        align1 = ""
        align2 = ""
        gap = -4
        while sw_matrix[i][j] != 0:  # once a cell is 0, backtarck ends
            u_l = sw_matrix[i - 1][j - 1]  # upper-left cell
            u = sw_matrix[i-1][j]  # upper cell
            l = sw_matrix[i][j - 1]  # left cell
            if u_l >= u and u_l >= l:  # choose the largest of the three
                align1 += sequence_1[i - 1]  # append the character in the sequence to the aligned sequence
                align2 += sequence_2[j - 1]
                i -= 1  # decrement to move back up the matrix
                j -= 1
            elif u > u_l and u >= l:
                if (u_l - u) >= gap: # sometimes the largest number isn't always the direction we want to go and its better if we
                                    # go diagonal. If the difference between going diagonal is better than putting a gap in the alignment,
                                    # go diagonal instead.
                    align1 += sequence_1[i - 1]
                    align2 += sequence_2[j - 1]
                    i -= 1
                    j -= 1
                else:
                    align1 += sequence_1[i - 1]
                    align2 += "*"  # represents a space
                    i -= 1
            elif l > u_l and l >= u:
                if (u_l - l) >= gap:
                    align1 += sequence_1[i - 1]  # append the character in the sequence to the aligned sequence
                    align2 += sequence_2[j - 1]
                    i -= 1  # decrement to move back up the matrix
                    j -= 1
                else:
                    align1 += "*"
                    align2 += sequence_2[j - 1]
                    j -= 1
        align1 = align1[::-1]  # reverse the strings we made from backtracking. This will be our final alignment
        align2 = align2[::-1]
        result1 = ""
        result2 = ""
        front1, front2 = get_front_sequence((i,j))
        back1, back2 = get_back_sequence(start_pos)
        result1 += front1
        result1 += align1
        result1 += back1
        result2 += front2
        result2 += align2
        result2 += back2
        return result1, result2

    def get_front_sequence(end_of_backtrack_pos):
        """
        :param end_of_backtrack_pos: position at the end of the backtrack
        :return: strings containing the characters before the local alignment (if there are any)

        Starting at the end of backtrack process and going as up-left as we can and then filling the remainder
        with gaps if we need to either ups or lefts. Continue this until we reach point (0,0) in matrix.
        Adding each character along the way or gaps.
        """

        i, j = end_of_backtrack_pos
        front_1 = ""
        front_2 = ""
        while (i,j) != (0,0):
            if i > 0 and j > 0:
                front_1 += sequence_1[i-1]
                front_2 += sequence_2[j-1]
                i -= 1
                j -= 1
            elif i > 0:
                front_1 += sequence_1[i-1]
                front_2 += "*"
                i -= 1
            elif j > 0:
                front_1 += "*"
                front_2 += sequence_2[j - 1]
                j -= 1
        return front_1[::-1], front_2[::-1]

    def get_back_sequence(start_pos):
        """
        :param start_pos: position where local alignment start
        :return: strings containing the characters after local alignment (if there are any)

        Starting at the starting position of local alignment (or cell with largest value)
        and moving down-right until we reach the bottom-right corner of the matrix. Adding each character along the way
        or gaps.
        """
        i, j = start_pos
        back_1 = ""
        back_2 = ""
        end_h = h - 1
        end_w = w - 1
        while (i, j) != (end_h, end_w):
            if i < end_h and j < end_w:
                i += 1
                j += 1
                back_1 += sequence_1[i-1]
                back_2 += sequence_2[j-1]
            elif i < end_h:
                i += 1
                back_1 += sequence_1[i-1]
                back_2 += "*"
            elif j < end_w:
                j += 1
                back_1 += "*"
                back_2 += sequence_2[j-1]
        return back_1, back_2

    def calculate_alignment_score(seq1, seq2):
        """
        Take in the two alignment sequences and use the blosum62 dictionary to determine the score
        of the two sequences. Not entirely sure if the starting position is the score of
        our alignment or not...planning on asking DB.
        """
        score = 0
        for i in range(len(seq1)):
            score += blosum_dict[(seq1[i], seq2[i])]
        return score

    sw_matrix = build_sw_matrix(w, h) # build matrix
    start_pos = get_start_pos(sw_matrix)    # get start position, where the largest value in the Smith-Waterman matrix is located
    align1, align2 = backtrack(sw_matrix, start_pos)    # get alignments
    score = calculate_alignment_score(align1, align2)   # calculate score of the two alignments
    return align1, align2, score    #return alignments and score


def Needleman_Wunsch(sequence_1, sequence_2, scoring_matrix):
    """
	Needlman-Wunsch algorithm

	Args:
		sequence_1: The first sequence
		sequence_2: The second sequence
		scoring_matrix: The matrix to determine the score of alignments

	Returns:
		Returns the two aligned sequences and the score in a tuple of the form (str, str, int)
	"""
    nw = NeedlemanWunsch(sequence_1, sequence_2, (1, -1, -4), scoring_matrix)
    return nw.ss1, nw.ss2, nw.score()


def Output_Sequences(alignment_1, alignment_2, score, scoring_matrix):
    """
	Prints (or writes to a file?) the score and two aligned sequences in the format specifed by the project documentation

	Args:
		sequence_1: The first aligned sequence
		sequence_2: The second aligned sequence
		score: the score of the aligned sequences

	"""
    """
    Notes:

    Append the beginning and end of the local alignment with the remainder of sequence
    Largest value in the scoring matrix is the score that should be output from the immediate local alignment
    """

    blosum_dict = scoring_matrix

    # replace gaps in alignment with "-" characters to meet output requirements
    alignment_1 = alignment_1.replace("*", "-")
    alignment_2 = alignment_2.replace("*", "-")

    print "Score: %d" % score
    # generate the result string in between the two alignments
    result = ""
    for c in range(len(alignment_1)):
        tmp = blosum_dict[alignment_1[c], alignment_2[c]]
        if alignment_1[c] == alignment_2[c] or tmp > 0:
            result += "|"
        elif alignment_1[c] == "-" or alignment_2[c] == "-":
            result += " "
        else:
            result += "*"

    linebreak = 80
    align1_break = [alignment_1[i:i+linebreak:] for i in range(0, len(alignment_1), linebreak)]
    align2_break = [alignment_2[i:i+linebreak:] for i in range(0, len(alignment_2), linebreak)]
    result_break = [result[i:i+linebreak:] for i in range(0, len(result), linebreak)]

    for i in range(len(align1_break)):
        print align1_break[i]
        print result_break[i]
        print align2_break[i]
        print

