class Person():
    userId = 0
    answers = {}
    timestamp = ''
    age = 0
    gender = 'F'
    address = ''

    def __init__(self, row):
        global questions
        #self.answers = {}
        self.userId = setId()
        self.timestamp = row[0]
        self.age = row[1]
        self.gender = row[2]
        self.address = row[3]
        for i, a in enumerate(row[4:-1]):
            if a.find(';') > -1:
                self.answers[questions[i]] = a.split(';')
            else:
                self.answers[questions[i]] = a

class Question():
    answers = {}
    text = ''

    def __init__(self, q):
        self.text = q
        self.answers = {}
        
    def add(self, answer, user):
        if answer.find(';') > -1:
            values = answer.split(';')
        else:
            values = [answer]
        for a in values:
            if a not in self.answers:
                self.answers[a] = []
            self.answers[a] += [user]

def setId():
    global users
    currentIds = list(users.keys())
    currentIds.sort()
    if len(currentIds) == 0:
        return 1
    else:
        lastId = currentIds.pop()
        newId = int(lastId) + 1
        return newId


root = 'D:/Python Projects/Music Data/Raw Data.csv'
f = open(root)
csv = f.read()
f.close()

questions = []
headers = csv.replace('ï»¿', '').split('\n')[0].split(',')
demographics = headers[:4]
demoDict = dict.fromkeys(demographics)
for d in demoDict:
    demoDict[d] = {}

for q in headers[4:]:
    newQuestion = Question(q)
    questions += [newQuestion]

print(questions)

userRows = [row.split(',') for row in csv.strip().split('\n')[1:]]
users= {}

for row in userRows:
    person = Person(row)
    users[person.userId] = person

    #[Timestamp, Age, Gender, Home]
    demographicVals = row[:4]
    for i, col in enumerate(demographicVals):
        #If answer not already in the dictionary of answers
        if col not in demoDict[demographics[i]]:
            demoDict[demographics[i]][col] = []     #add answer and empty list to dictionary
        demoDict[demographics[i]][col] += [person]  #add user to the list of users that answered this way

    #For the questions    
    for i, col in enumerate(row[4:]):
        #print(col)
        questions[i].add(col, person)

print('Questions?', len(questions))
blankDemoDict = {}
for cat in demoDict:
    blankDemoDict[cat] = {}
    for val in demoDict[cat]:
        blankDemoDict[cat][val] = 0
print(blankDemoDict)
        
for i, q in enumerate([questions[-4]]):
    csv = ''
        
    for v in q.answers:
        theseDemos = blankDemoDict
        csvHeader = v + ','
        csvRow = ''
        for user in q.answers[v]:
            theseDemos['Timestamp'][user.timestamp] += 1
            theseDemos['Age?'][user.age] += 1
            theseDemos['Gender?'][user.gender] += 1
            #theseDemos['Home?'][user.address] += 1

        #Combine demos like address    
        catsSorted = list(theseDemos.keys())
        catsSorted.sort()
        for cat in catsSorted:
            answersSorted = list(theseDemos[cat].keys())
            answersSorted.sort()
            
            for answer in answersSorted:
                csvRow += str(theseDemos[cat][answer]) + ','
                if i == 0:
                    csvHeader += answer + ','
        csv += csvRow+ '\n'

    f = open('D:/Python Projects/Music Data/Question ' + str(i) + '.csv', 'w')
    f.write(csvHeader + '\n' + csv)
    f.close()
