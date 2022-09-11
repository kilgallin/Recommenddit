import sys
import csv
import errno
import apriori

def compute_list(records):
    item_list = []
    #print "test apriori"
    for data in records:
        if data is not None:
            item_list.append(data)
    return item_list

def query_subreddit(subreddit, records):
    subreddit_set = set()
    for x in records:
        subreddit_set.add(x)
    if subreddit in map(str.lower, subreddit_set):
        return True
    else:
        return False

def write_tempfile(data,temp_filename):
    #print author
    #print subreddit_list
    streddit = ""
    f = open(temp_filename,"a") #opens file with name of "test.txt"
    for x in data:
        streddit += x + ","
    #print streddit
    f.write(streddit+"\n")
    f.close()

def delete_tempfile(temp_filename):
    f = open(temp_filename, "w")
    f.truncate()
    f.close()

def main():
    """ start calling function """
    # file path specification
    print "Please input your interest subreddit: /r/", 
    subreddit = raw_input().lower()
    filename = 'transaction.csv'
    items_data = []
    try:
        # create temporary file for user
        temp_filename = 'transaction_temp.csv'

        with open(filename, 'rb') as content:
            reader = csv.reader(content)
            content_list = list(reader)
            count = 0
            found_count = 0
            # create csv file here
            for records in content_list:
                count+=1
                if query_subreddit(subreddit, records):
                    temp = compute_list(records)
                    items_data.append(temp)
                    found_count+=1
            # writing temporary file for calculation
            for data in items_data:
                write_tempfile(data,temp_filename)
        content.close()

        # test on priori
        """ SET THE SUPPORT AND CONFIDENCE HERE! 
            DEFAULT: support = 0.15 confidence = 0.6 
            runApriori(temp_filename, support, confidence)
        """
        items, rules = apriori.runApriori(apriori.dataFromFile(temp_filename), 0.05, 0.05)
        apriori.printResults(items, rules)
        print "\n------------------------ RECOMMENDIT RESULT:"
        index = 1
        for subr in apriori.recommendation_set:
            print index,":",subr
            index+=1
        print "----------------------------------------------"
        print "Query over ", count," records in transaction"
        print "Found: ",found_count, " records in transaction"
        # delete csv file here
        delete_tempfile(temp_filename)

    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            print filename," not found"
            raise # Propagate other kinds of IOError.

if __name__ == '__main__':
    main()