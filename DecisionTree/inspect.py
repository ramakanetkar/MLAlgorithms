import math
import sys
def main():
    positive_value =["democrat", "A", "y", "before1950", "yes", "morethan3min", "fast", "expensive",
	            "high", "Two", "large",'+']
    #f1 = open("example1.csv",'r')
    f1 = open(sys.argv[1],'r')
    line_count = 0
    plus_count = 0
    next(f1)
    for f in f1:
        line_count = line_count + 1
        if (f[f.rfind(',')+1:]).strip() in positive_value:
            plus_count = plus_count +1
    print('entrophy: ' + str(calculate_entrophy(plus_count,line_count)))
    error = (line_count-plus_count)/line_count
    print('error: ' + str(error))

def calculate_entrophy(plus, total):
    xp = (plus/total) * math.log((total/plus),2)
    minus = total - plus
    xm = (minus/total) * math.log((total/minus),2)
    return xp+xm

if __name__=="__main__":
    main()