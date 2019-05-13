import os
from flask import Flask, request, render_template, g, redirect, Response, session, abort, flash
import pandas as pd
import io
import requests
import pandasql as ps
from joblib import dump, load
import numpy as np
# flask... magic
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



# read data from URL
url1 = "https://raw.githubusercontent.com/thuhlz/OpenDataSetNewsPop/master/train.csv"
s = requests.get(url1).content
data = pd.read_csv(io.StringIO(s.decode('utf-8')))



data['pop_level']=data[' shares']
data['pop_level'].loc[data[' shares'].between(0,1000)] = 0
data['pop_level'].loc[data[' shares'].between(1001,2000)] = 1
data['pop_level'].loc[data[' shares'].between(2000,3000,inclusive=False)] = 2
data['pop_level'].loc[data[' shares'].between(3000,4000)] = 3
data['pop_level'].loc[data[' shares'].between(4000,5000,inclusive=False)] = 4
data['pop_level'].loc[data[' shares']>=5000] = 5

# read text from URL
#url2 = ""
#t = requests.get(url2).content
#text = pd.read_csv(io.StringIO(t.decode('utf-8')))
# load model
moswl =  load('ModelRF.joblib')
data.rename(columns={ data.columns[0]: "idx" }, inplace=True)
# re-formate the data
#data.drop('Unnamed: 0',axis=1)
url2 = 'https://raw.githubusercontent.com/thuhlz/OpenDataSetNewsPop/master/news.csv'
t = requests.get(url2).content
textdata = pd.read_csv(io.StringIO(t.decode('utf-8')))





def getTable(index):
    query = "SELECT * FROM data WHERE idx = %s;" % (index)
    #text = gettext(url)
    result = ps.sqldf(query, globals())
    return result



def gettext(index):
    query = "SELECT * FROM textdata WHERE idx = %s;" % (index)
    result = ps.sqldf(query, globals())
    return result
@app.before_request
def before_request():
    return


@app.teardown_request
def teardown_request(exception):
    return

@app.route('/')
def index():
    return render_template("index.html")

def get_count(news_type):
    df = pd.DataFrame(data[data[news_type] == 1]['pop_level'].value_counts())
    dict = {}
    for i in range(6):
        dict[df.index[i]] =  df.iloc[i].values[0]
    l1, l2, l3, l4, l5, l6 = dict[0],dict[1],dict[2],dict[3],dict[4],dict[5]
    return l1,l2,l3,l4,l5,l6

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    typelist = [' data_channel_is_lifestyle', ' data_channel_is_entertainment',
                ' data_channel_is_bus', ' data_channel_is_socmed',
                ' data_channel_is_tech', ' data_channel_is_world']
    l1,l2,l3,l4,l5,l6 = get_count(typelist[0])
    e1, e2, e3, e4,e5, e6 = get_count(typelist[1])
    b1, b2, b3, b4, b5, b6 = get_count(typelist[2])
    s1, s2, s3, s4, s5, s6 = get_count(typelist[3])
    t1, t2, t3, t4, t5, t6 = get_count(typelist[4])
    w1, w2, w3, w4, w5, w6 = get_count(typelist[5])
    print(s1, s2, s3, s4, s5, s6,t1, t2, t3, t4, t5, t6,w1, w2, w3, w4, w5, w6)
    return render_template("dashboard.html",l1=l1,l2=l2,l3=l3,l4=l4,l5=l5,l6=l6,
                           e1=e1, e2=e2, e3=e3, e4=e4,e5=e5, e6=e6,
                           b1=b1, b2=b2, b3=b3, b4=b4, b5=b5, b6=b6,
                           s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6,
                           t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, t6=t6,
                           w1=w1, w2=w2, w3=w3, w4=w4, w5=w5, w6=w6)


@app.route('/list', methods=['POST','GET'])
def list():
    a = [i for i in range(1000)]
    np.random.shuffle(a)
    nums = a[:6]

    num1 = nums[0]
    T_sql = gettext(num1)
    title1 = T_sql['title'].values[0]
    pic1 = T_sql['pic'].values[0]

    num2 = nums[1]
    T_sql = gettext(num2)
    title2 = T_sql['title'].values[0]
    pic2 = T_sql['pic'].values[0]

    num3 = nums[2]
    T_sql = gettext(num3)
    title3 = T_sql['title'].values[0]
    pic3 = T_sql['pic'].values[0]

    num4 = nums[3]
    T_sql = gettext(num4)
    title4 = T_sql['title'].values[0]
    pic4 = T_sql['pic'].values[0]

    num5 = nums[4]
    T_sql = gettext(num5)
    title5 = T_sql['title'].values[0]
    pic5 = T_sql['pic'].values[0]

    num6 = nums[5]
    T_sql = gettext(num6)
    title6 = T_sql['title'].values[0]
    pic6 = T_sql['pic'].values[0]

    return render_template("selectNewsToPredict.html",num1 = num1, num2 = num2, num3 = num3, num4 = num4, num5 = num5, num6 = num6,
                           title1 = title1, title2 = title2, title3 = title3, title4 = title4, title5 = title5,title6 = title6, pic1=pic1,
                           pic2=pic2, pic3=pic3, pic4=pic4, pic5=pic5, pic6=pic6)



@app.route('/predict', methods=['POST'])
def predict():
    #if request.method != 'POST':
    #    return render_template("wrong.html")

    index = request.form['index']
    T_sql = gettext(index)
    url = T_sql['url'].values[0]
    text = T_sql['text'].values[0]
    title =T_sql['title'].values[0]
    results = getTable(index)
    results =results.iloc[:,2:-2]
    pop_dist=["very low","low", "below average", "above average", "high", "very high"]
    pop_value = pop_dist[moswl.predict(results)[0]]

    info = []
    dic = dict()
    for i in results.columns.tolist():
        dic[i] = results[i].values[0]
    info.append(dic)
    context = dict(NLP_values=info)

    return render_template("predict.html", pop_value=pop_value,text = text,title = title,url =url, **context)


if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

        HOST, PORT = host, port
        print ("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()