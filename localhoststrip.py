def main():
    f = open('output.txt', 'w')
    for line in open('list.txt', 'r'):
        line2 = line.split()
        if len(line2) != 2:
            continue
        f.write(str(line2[1] + '\n'))
    f.close()
         
main()
