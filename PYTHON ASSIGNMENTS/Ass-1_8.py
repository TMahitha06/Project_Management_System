def process_scores(scores):
    first,*middle,last=scores
    avg=sum(middle)/ len(middle)if middle else 0
    return (first,last,avg)
print(process_scores([98, 85, 88, 92, 78]))