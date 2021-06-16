#  python 3
import tracemalloc
import time
start_time = time.time()
tracemalloc.start()

frenchDictionary = {}
with open('french_dictionary.csv', encoding='utf-8') as reader:
    for i in reader.readlines():
        line = i.split(",");
        frenchDictionary[line[0]] = line[1][:len(line[1])-1]; 

wordFrequency = {}
with open('find_words.txt') as reader:
    for line in reader:
        for word in line.split():
            if frenchDictionary.get(word,False):
                wordFrequency[word] = 0

punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
def removepunc(word):
    punctations = []
    for i,ele in enumerate(word): 
        if ele in punc:
            if ele.find("'") and i>0:
                ele = word[i:]
            punctations.append([ele,i])
            word = word.replace(ele, "")
    return [word,punctations]
def ReplaceWord(word):
    tempword = removepunc(word);
    tempCnt = wordFrequency.get(tempword[0].lower(),-1)
    if tempCnt>=0:
        wordFrequency[tempword[0].lower()] += 1
        replaceword = frenchDictionary[tempword[0].lower()] 
        if tempword[0][0].isupper():
            replaceword = replaceword[0].upper()+replaceword[1:]
        if tempword[0].isupper():
            replaceword = replaceword.upper()
        for i in tempword[1]:
            if i[1] == 0:
                replaceword = i[0]+replaceword
            else:
                replaceword = replaceword+i[0]
        return replaceword
    return word
with open('t8.shakespeare.txt',encoding='utf-8') as infile, open('t8.shakespeare.translated.txt', 'w',encoding='utf-8') as outfile:
    for line in infile:
        for word in line.split():
            
            if word.find("-")==-1:
                replaceword = ReplaceWord(word)
            else:
                treplaceword = []
                for tword in word.split("-"):
                    treplaceword.append(ReplaceWord(tword))
                replaceword = "-".join(treplaceword)        

            line = line.replace(word,replaceword)
        outfile.write(line)
with open('frequency.csv', 'w',encoding='utf-8') as file:
    for key,val in wordFrequency.items():
        line = key+","+frenchDictionary[key]+","+str(val)+"\n"
        file.write(line)

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
tracemalloc.stop()
with open('performance.txt','w') as file:
    file.write(time.strftime("Time to process: %M minutes %S seconds",time.gmtime(end_time-start_time)))
    file.write(f"\nMemeory used: {peak / 10**6} MB")    