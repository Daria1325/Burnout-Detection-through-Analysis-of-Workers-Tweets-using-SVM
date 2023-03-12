import pickle
import numpy as np
import analizer.Tweets as tw
from sklearn.feature_extraction.text import TfidfVectorizer

from personal.models import Employee, State, Result

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


def change_status(worker, new_status_id):
    emp = Employee.objects.get(employee_id=worker['employee_id_id'])
    print(new_status_id)
    state = State.objects.get(state_id=new_status_id)
   
    emp.state_id = state
    emp.save()
    return

def save_results(worker, date, probs, count):
    employee = Employee.objects.get(employee_id=worker['employee_id_id'])
    prev_res = Result.objects.filter(employee_id=employee).order_by('-scan_date').values_list('scan_date', flat=True)[0]
    result = {"percent_N" : probs[0], "percent_S": probs[1], "percent_L" : probs[2],
    "count_N" : count[0], "count_S" : count[1], "count_L" : count[2]}
    result['status'] = analize_results(result)
    Result.objects.update_or_create(
    employee_id=employee, scan_date = date,
    defaults=result,
    )
    if prev_res<date:
        return 'change'
    else:
        return 'no_change'


def analize_results(results):
    if (results['count_N']+results['count_S']+results['count_L']==0):
        return "N"
    elif results['percent_N']>0.85:
        return "L"
    elif (results['percent_S']+ results['percent_L']>30):
        return "H"
    else:
        return "M"


def find_new_status_id(new_res,prev_res=None):
    if prev_res is None:
        new_status_id = State.objects.filter(status=new_res).filter(progress__exact='').values_list('state_id', flat=True)[0]
        return new_status_id

    
    if (new_res=='N'):
        new_status_id = State.objects.filter(status=new_res).filter(progress__exact='').values_list('state_id', flat=True)[0]
    elif (prev_res == new_res):
        new_status_id = State.objects.filter(status=new_res).filter(progress='S').values_list('state_id', flat=True)[0]
    elif(new_res=='L'):
        new_status_id = State.objects.filter(status=new_res).filter(progress='I').values_list('state_id', flat=True)[0]
    elif(new_res=='H'):
        new_status_id = State.objects.filter(status=new_res).filter(progress='W').values_list('state_id', flat=True)[0]
    elif(new_res=='M' and prev_res=='L'):
        new_status_id = State.objects.filter(status=new_res).filter(progress='W').values_list('state_id', flat=True)[0]
    else:
        new_status_id = State.objects.filter(status='M').filter(progress='I').values_list('state_id', flat=True)[0]
    return new_status_id

def form_new_status(worker):
    employee = Employee.objects.get(employee_id=worker['employee_id_id'])
    last_results = Result.objects.filter(employee_id=employee).order_by('-scan_date').values()
    last_result_status = analize_results(last_results[0])
    if last_results.count() >1:
        prev_result_status = analize_results(last_results[1])
        new_status_id=find_new_status_id(last_result_status,prev_result_status)
        
    else:
        new_status_id=find_new_status_id(last_result_status)
    
    change_status(worker,new_status_id)



def analize_tweets(workers,date):
    textData,model=openFiles()
    i=0
    twitter = tw.Twitter()
    for worker in workers:
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
        save_results(worker,date,average[0], average[1])
        form_new_status(worker)      
       
        i+=1

    return     
