#import app as mk
from flask import Flask, jsonify, request, render_template
from datetime import datetime


#make a flask app
app = Flask(__name__)

# function to divide the user_id in 2's like if the codedata = 0123  then 
# codelist =  ['01','12','23']
# and codecounter to divide every 2 numbers
def divideUsercode(codeData, codelist, codecounter):
    for i in codeData:

        #codecounter to divide every 2 number
        if codecounter//2:

            #add every 2 numbers to codelist
            codelist.append(codeData[codecounter-2:codecounter])
        codecounter += 1
    return codelist

# function to get current timestamp
def getDateandTime():
    now = datetime.now()
    #print('time now is',now)
    result = int(datetime.timestamp(now))
    result = str(result)
    return result

# Function we send to it user_id and get it's corresonding OTP  
def generateOTP(codeData):

    # check if the length is 1 add 0 on the left cause we divide into 2 numbers
    if len(codeData) == 1:
        u = '0'+codeData

    codelist = []
    codecounter = 1

    # store the listed user_id after being divided  
    codeToBehex = divideUsercode(codeData, codelist, codecounter)

    #to store the summation of the user_id after being listed  
    codeStore = 0

    for x in range(len(codeToBehex)):

        codeStore += int(codeToBehex[x])

    #now code store has the summation of the listed user_id 
    # if user_id = 0123 then codestore now is = 01+12+23 = 36     

    

    #convert the summation of the listed user_id into hexadecimal
    hexCode = hex(codeStore)

    # neglict the first 2 digits which are = 0x , beacause the conversion to hexa
    hexCode = hexCode[2:]
    
    
    # now hexCode contain the summation of every 2's in user_id into hexadecimal 
    # hexCode length will never be more than 3 digits or characters 



    # get timestamp of the current date and time
    dt = getDateandTime()
    
    #subtract current timestamp from (1609452000) which is the timestamp of (1/1/2021)
    dt = int(dt) - 1609452000
    dt = str(dt)

    #neglict the last 2 numbers after subtraction from (1609452000) 
    #and convert the result to hexa
    dt = int(dt[:6])
    OTP = hex(dt)

    #neglict 0x which are the first 2 digits after converting the resulting date to hexa 
    # concatenate it to hexCode which contains the summation of every 2's in user_id into 
    # hexadecimal 
    OTP = OTP[2:]+hexCode

    # the OTP length won't be more than 8 digits or characters
    return OTP


# home route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')



# success route if
@app.route('/success', methods=['GET', 'POST'])
def success():

    if request.method == 'POST':

        #get the user_id from the request data 
        user = request.form['usercode']
        if user != '':

            #generate the otp using the user_id entered from the textBox
            otp = generateOTP(user)


            # add user_id and it's corresponding otp to an obj
            data = {
                'user_id': user,
                'OTP': otp
            }

            return data
        else:
            return 'Error'


# Run the application
if __name__ == '__main__':
    app.debug = True
    app.run()