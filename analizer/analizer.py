import pickle
import numpy as np
import analizer.Tweets as tw
from sklearn.feature_extraction.text import TfidfVectorizer
# from copy import deepcopy as copy


from personal.models import Employee, State, Result

# class Result(object):
#     def __init__(self,date,probs,count):
#         self.date = date    
#         self.probs = probs
#         self.count = count
#         self.status = self.calculateStatus()
#     def calculateStatus(self):
#         status = Status()
#         status.analizeResults([self],type = "oneResult")

#         return status.status

# class Status(object):
#     def __init__(self):
#         self.note = None
#         self.progress = None
#         self.status = None
#     def analizeResults(self,results,type=None):
#         if type == "oneResult":
#             if (results[0].count[0]+results[0].count[1]+results[0].count[2]==0):
#                 self.status = "No data"
#             elif results[0].probs[0]>0.85:
#                 self.status = "Low"
#             elif (results[0].probs[1]+ results[0].probs[2]>30):
#                 self.status = "High"
#             else:
#                 self.status = "Moderate"
#         elif len(results)==1:
#             self.progress = "Not enough data"
#             if results[-1].status == "High":
#                 self.status = "High"
#                 self.note = "HIGH risk. Needs attention."
#             elif results[-1].status == "Low":
#                 self.status = "Low"
#                 self.note = "No need to worry. Employee is fine."
#             elif results[-1].status == "Moderate":
#                  self.note = "MODERATE risk. Employee may expirience some minor problems."
#             else:
#                 self.status = "No data"
#                 self.note = "Not enoufh data for defining state."
        
#         elif len(results)>1:
#             if results[-1].status == "High":
#                 self.status = "High"
#                 if results[-2].status == "High":
#                     self.note = "Two scanings in HIGH rick. Needs attention."
#                     self.progress = "Stable"
#                 elif results[-2].status == "Low":
#                     self.note = "Last scaning was in LOW rick.  Needs attention."
#                     self.progress = "Worsened"
#                 elif results[-2].status == "Moderate":
#                     self.note = "Last scaning was in MODERATE rick. Worsened."
#                     self.progress = "Worsened"
#                 else:
#                     self.note = "HIGH risk. Needs attention."
#                     self.progress = "Not enough data"
           
#             elif results[-1].status == "Low":
#                 self.status = "Low"
#                 self.note = "No need to worry. Employee is fine."
#                 if results[-2].status == "High":
#                     self.progress = "Improved"
#                 elif results[-2].status == "Low":
#                     self.progress = "Stable"
#                 elif results[-2].status == "Moderate":
#                     self.progress = "Improved"
#                 else:
#                     self.progress = "Not enough data"
            
#             elif results[-1].status == "Moderate":
#                 self.status = "Moderate"
#                 if results[-2].status == "High":
#                     self.note = "Last scaning was in HIGH rick. Improved."
#                     self.progress = "Improved"
#                 elif results[-2].status == "Low":
#                     self.note = "Last scaning was in LOW rick. Worsened."
#                     self.progress = "Worsened"
#                 elif results[-2].status == "Moderate":
#                     self.note = "Last scaning was in MODERATE rick. Stable."
#                     self.progress = "Stable"
#                 else:
#                     self.note = "MODERATE risk. Employee may expirience some minor problems."
#                     self.progress = "Not enough data"

    
    
# class Person(object):
#     def __init__(self,id):
#         self.id = id    
#         self.results = []
#         self.state = Status()

#     def addResult(self,result):
#         self.results.append(copy(result))
#         self.state.analizeResults(self.results)
        

#     def __str__(self):
#         return self.id + " "+ self.results[0].status




def openFiles():
    f = open("analizer\data\\alldata.txt", "r")
    
    textData =f.read()
    textData = textData.split('\n')

    with open('analizer\Model\model.pkl', 'rb') as f:
        model = pickle.load(f)
    return textData, model


def getAverage(arr):
    probs = [0., 0., 0.]
    counts= [0,0,0]
    if len(arr)!=0:
        for item in arr:
            probs+=item
            max_val = np.max(item)
            counts[np.where(item == max_val)[0][0]]+=1
        probs =[round(x/len(arr),2) for x in probs]
    return (probs,counts)


def getPrevStatus(worker):
    employee = Employee.objects.filter(employee_id=worker['employee_id_id']).values_list('state_id', flat=True)
    return employee[0]

def analize_results(probs, counts):
    if (counts[0]+counts[1]+counts[2]==0):
        return "N"
    elif probs[0]>0.85:
        return "L"
    elif (probs[1]+ probs[2]>30):
        return "H"
    else:
        return "M"


def find_new_status_id(prev_status_id, new_status):
    if prev_status_id is None:
        new_status_id = State.objects.filter(status=new_status).filter(progress__exact='').values_list('state_id', flat=True)[0]
        return new_status_id
    prev_status = State.objects.filter(state_id=prev_status_id).values_list('status', flat=True)[0]
    
    if (new_status=='N'):
        new_status_id = State.objects.filter(status=new_status).filter(progress__exact='').values_list('state_id', flat=True)[0]
    elif (prev_status == new_status):
        new_status_id = State.objects.filter(status=new_status).filter(progress='S').values_list('state_id', flat=True)[0]
    elif(new_status=='L'):
        new_status_id = State.objects.filter(status=new_status).filter(progress='I').values_list('state_id', flat=True)[0]
    elif(new_status=='H'):
        new_status_id = State.objects.filter(status=new_status).filter(progress='W').values_list('state_id', flat=True)[0]
    elif(new_status=='M' and prev_status=='L'):
        new_status_id = State.objects.filter(status=new_status).filter(progress='W').values_list('state_id', flat=True)[0]
    else:
        new_status_id = State.objects.filter(status='M').filter(progress='I').values_list('state_id', flat=True)[0]
    return new_status_id

def change_status(worker, new_status_id):
    emp = Employee.objects.get(employee_id=worker['employee_id_id'])
    print(new_status_id)
    state = State.objects.get(state_id=new_status_id)
   
    emp.state_id = state
    emp.save()
    return

def save_results(worker, date, probs, count):
    employee = Employee.objects.get(employee_id=worker['employee_id_id'])
    Result.objects.update_or_create(
    employee_id=employee, scan_date = date,
    defaults={"percent_N" : probs[0], "percent_S": probs[1], "percent_L" : probs[2],
    "count_N" : count[0], "count_S" : count[1], "count_L" : count[2]},
)
    return


def analize_tweets(workers,date):
    textData,model=openFiles()
    i=0
    twitter = tw.Twitter()
    for worker in workers:

        prev_status = getPrevStatus(worker)


        tweets = twitter.get_tweets(worker['username'],date)
        results = []
        for tweet in tweets:
            to_predict = [tweet]
            vectorizer = TfidfVectorizer(sublinear_tf=True,norm='l2')
            vectorizer.fit_transform(textData).toarray()
            to_predict_vec = vectorizer.transform(to_predict)
            probs = np.round(model.predict_proba(to_predict_vec)[0],decimals=2)
            results.append(probs)

        average = getAverage(results)
        new_status=analize_results(average[0],average[1])
        new_status_id =find_new_status_id(prev_status,new_status)
        change_status(worker,new_status_id)

        save_results(worker,date,average[0], average[1])
       
        i+=1

    return     
