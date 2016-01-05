from os import listdir, mkdir

HEADER_START = "705000001001011707001   5323 #0001    N                               "
HEADER_MID = "0      0"
DATA_HEAD_END = 40
DATA_GAP = 50
DATA_TAIL_START = 90
LINE_LEN = 291

def get_term():
    return raw_input("Input term code: ")

def build_header(term, filename):
    if len(filename) == 8:
        courseNum = "0" + filename[0:4]
    else:
        courseNum = filename[0:5]
    numQ = guess_num_questions(term, filename)
    # Convert numQ to string with leadng zeroes (len == 3)
    numQ = "{0:03d}".format(numQ)
    assert int(courseNum) > 999 #sanity check
    print "Guessing {} questions for course {}".format(numQ, filename[:-4])
    return HEADER_START + term + numQ + HEADER_MID + courseNum + "\n"

def clean_data(term, filename):
    cleanData = ""
    with open(term + "/" + filename) as datfile:
        for line in datfile.readlines():
            if len(line) == LINE_LEN:
                cleanData += clean_line(line)
    return cleanData

def clean_line(line):
    return line[:DATA_HEAD_END] + DATA_GAP*" " + line[DATA_TAIL_START:]

def write_cleaned_file(targetDir, filename, header, data):
    with open(targetDir + filename, "w") as datfile:
        datfile.write(header + data + chr(26))

def guess_num_questions(term, filename):
    counts = []
    with open(term + "/" + filename) as datfile:
        for line in datfile.readlines():
            current_count = 0
            for i in range(DATA_TAIL_START, LINE_LEN+1):
                if line[i] != " ":
                    current_count += 1
                else:
                    counts.append(current_count)
                    break
    return get_mode(counts)

def get_mode(counts):
    count_dict = {}
    max_freq = 0
    max_count = None
    for c in counts:
        try: count_dict[c] += 1
        except KeyError: count_dict[c] = 1
        if count_dict[c] > max_freq:
            max_count = c
            max_freq = count_dict[c]
    return max_count
    
if __name__ == '__main__':
    term = get_term()
    targetDir = term + "/cleaned/"
    mkdir(targetDir)
    for f in listdir(term):
        if f.upper() == "QS.DAT" or f[-4:].upper() != ".DAT":
            continue
        else:
            header = build_header(term, f)
            cleanedData = clean_data(term, f)
            write_cleaned_file(targetDir, f, header, cleanedData)
    raw_input("Press ENTER to exit.")
