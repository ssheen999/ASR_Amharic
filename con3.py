# usr/env/python3

def convert(file):
    output = open("text_unicode", "w")
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            for i in line.split():
                U=''
                for j in i:
                    if j not in '<UNK>':
                        U += 'x%04x' % ord(j)
                    
                    else:
                        U += j

                output.write(U+ ' ')
            
            output.write("\n")
        
        output.close()

    return output


convert('text2')



