import datetime as dt
action_date = dt.date.today()
a=['1','2']



with open('./select_result/' + str(action_date), 'w') as f:
    for i in a:
        f.write(i + '\n')