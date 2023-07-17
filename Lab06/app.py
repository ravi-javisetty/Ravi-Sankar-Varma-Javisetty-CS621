from flask import Flask, render_template,request,redirect,url_for
app=Flask(__name__)
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/report',methods=['POST'])
def report():
    password=request.form["pass"]
    lc=False
    uc=False
    len_pass=False
    dig_check=False
    check_status=False
    for i in password:
        if(i.islower()):
            lc=True
    for i in password:
        if(i.isupper()):
            uc=True
    if (len(password)>=8):
        len_pass=True
    if(password[len(password)-1].isdigit()):
        dig_check=True
    check_status= lc and uc and len_pass and dig_check
    return render_template('report.html',check_status=check_status,lc=lc,uc=uc,len_pass=len_pass,dig_check=dig_check)
if __name__=='__main__':
    app.run(debug=True)
