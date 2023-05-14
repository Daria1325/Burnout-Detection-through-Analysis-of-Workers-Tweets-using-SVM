import pickle
import numpy as np
import analizer.Tweets as tw
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from personal.models import Employee, State, Result
import re
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) 


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
    state = State.objects.get(state_id=new_status_id)
   
    emp.state_id = state
    emp.save()
    return

def save_results(worker, date, probs, count):
    employee = Employee.objects.get(employee_id=worker['employee_id_id'])
    result = {"percent_N" : probs[0], "percent_S": probs[1], "percent_L" : probs[2],
    "count_N" : count[0], "count_S" : count[1], "count_L" : count[2]}
    result['status'], _ = analize_results(result)
    Result.objects.update_or_create(
    employee_id=employee, scan_date = date,
    defaults=result,
    )

def get_average_count(results):
    count = 0
    number = 0
    for result in results:
        if result['count_N']+result['count_S']+result['count_L'] !=0:
            count+= result['count_N']+result['count_S']+result['count_L']
            number+=1
    if number==0:
        return 0.
    return count/number

def analize_results(results):
    if (results['count_N']+results['count_S']+results['count_L']==0):
        return "N",results['count_N']+results['count_S']+results['count_L']
    elif results['percent_N']>=0.75:
        return "L",results['count_N']+results['count_S']+results['count_L']
    elif (results['percent_S'] + results['percent_L']>=0.35):
        return "H",results['count_N']+results['count_S']+results['count_L']
    else:
        return "M",results['count_N']+results['count_S']+results['count_L']


def find_new_status_id(new_res, new_count, prev_res=None, avr_count=None):
    if prev_res is None:
        new_status_id = State.objects.filter(status=new_res[0]).filter(progress__exact='').values_list('state_id', flat=True)[0]
        return new_status_id
    elif prev_res=='N' and new_res=='N':
        new_status_id = State.objects.filter(status=new_res).filter(progress__exact='').values_list('state_id', flat=True)[0]
        return new_status_id

    if avr_count is not None and avr_count!=0:
        change = (abs(new_count- avr_count)) * 100 / avr_count
        if change >70 and new_count>15 and avr_count>=15 and new_res !='H':
            new_status_id = State.objects.filter(status='M').filter(note = "Big change in number of posted tweets").values_list('state_id', flat=True)[0]
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
    last_result_status, last_count = analize_results(last_results[0])
    if last_results.count() > 1:
        prev_result_status,_ = analize_results(last_results[1])
        avr_count = get_average_count(last_results[1:3])
        new_status_id=find_new_status_id(last_result_status,last_count, prev_result_status, avr_count)
    else:
        new_status_id=find_new_status_id(last_result_status, last_count)
    
    change_status(worker,new_status_id)



@shared_task(bind=True)
def analize_tweets(self,workers,date):
    progress_recorder = ProgressRecorder(self)
    textData,model=openFiles()
    i=0
    twitter = tw.Twitter()
    date = datetime.strptime(str(date), "%Y-%m-%d").date()
    for worker in workers:
       # tweets = twitter.get_tweets(worker['username'],date)
        tweets = twitter.get_tweets_snc(worker['username'],date)
        results = []
        for tweet in tweets:
            to_predict = [tweet]
            vectorizer = TfidfVectorizer(sublinear_tf=True,norm='l2')
            vectorizer.fit_transform(textData).toarray()
            to_predict_vec = vectorizer.transform(to_predict)
            probs = np.round(model.predict_proba(to_predict_vec)[0],decimals=2)
            results.append(probs)
            print(probs)

        average = getAverage(results)
        save_results(worker,date,average[0], average[1])
        form_new_status(worker)      
        i+=1
        progress_recorder.set_progress(i,len(workers))
    return ''  

def clean_text(text):
        text = text.lower().strip()
        text = re.sub('@[^\s]+','',text)
        text = re.sub('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])','',text)
        text = re.sub('[^\x00-\x7F]+','',text)
        text =  re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub(' +', ' ', text)
        clean_text=""
        for x in text.split():
            if x not in set(stopwords.words('english')):
                clean_text=" ".join([clean_text, x])
        return clean_text

def analize_text(text):
    text = clean_text(text)
    doc = nlp(text)
    text=" ".join([token.lemma_ for token in doc])
    
    textData,model=openFiles()
    vectorizer = TfidfVectorizer(sublinear_tf=True,norm='l2')
    vectorizer.fit_transform(textData).toarray()
    to_predict_vec = vectorizer.transform([text])
    probs = np.round(model.predict_proba(to_predict_vec)[0],decimals=2)
    return probs