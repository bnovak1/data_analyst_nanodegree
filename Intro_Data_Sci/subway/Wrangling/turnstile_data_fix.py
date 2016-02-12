import csv

def fix_turnstile_data(filenames):
    '''
    Filenames is a list of MTA Subway turnstile text files. A link to an example
    MTA Subway turnstile text file can be seen at the URL below:
    http://web.mta.info/developers/data/nyct/turnstile/turnstile_110507.txt
    
    As you can see, there are numerous data points included in each row of the
    a MTA Subway turnstile text file. 

    You want to write a function that will update each row in the text
    file so there is only one entry per row. A few examples below:
    A002,R051,02-00-00,05-28-11,00:00:00,REGULAR,003178521,001100739
    A002,R051,02-00-00,05-28-11,04:00:00,REGULAR,003178541,001100746
    A002,R051,02-00-00,05-28-11,08:00:00,REGULAR,003178559,001100775
    
    Write the updates to a different text file in the format of "updated_" + filename.
    For example:
        1) if you read in a text file called "turnstile_110521.txt"
        2) you should write the updated data to "updated_turnstile_110521.txt"

    The order of the fields should be preserved. 
    
    You can see a sample of the turnstile text file that's passed into this function
    and the the corresponding updated file in the links below:
    
    Sample input file:
    https://www.dropbox.com/s/mpin5zv4hgrx244/turnstile_110528.txt
    Sample updated file:
    https://www.dropbox.com/s/074xbgio4c39b7h/solution_turnstile_110528.txt
    '''
    print filenames
    
    for name in filenames:
        
        # read in data
        fid_in = open(name,'r')
        data = csv.reader(fid_in)

        # output file
        name_out = "updated_" + name
        fid_out = open(name_out,'w')
        writer = csv.writer(fid_out)
        
        # loop over rows of input data
        for row in data:
            
            # length of row
            lrow = len(row)
            
            # number of records per row is (lrow - 3)/5 since there are 8 entries per record, but the first 3 occur only once
            lrow_new = (len(row) - 3)/5
            
            # loop over records in row and write to output file
            for irec in range(lrow_new):
                writer.writerow(row[0:3] + row[5*irec+3:5*irec+8])            
            
