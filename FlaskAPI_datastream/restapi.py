from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from datastreamlib import *
from Sabrewebservicelib import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

#cur = None

def checkPostedData(postedData, functionName):
    if (functionName == "getpnrcontactincludewebservice" or functionName == "subtract" or functionName == "multiply"):
        if "flightno" not in postedData or "date" not in postedData or "dep" not in postedData:
            return 301  # Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200


def getcontactpnrs(flightno, date):
    #global cur
    #if cur == None:
    #cur = connectdb()
    pnrsfromdatastream = getpnrsdatastream(
        flightno, date, cur)  # '6442', '03-mar-2021'
    returnlist = []
    for pnr in pnrsfromdatastream:
        paxphones = getpaxcontactandticket(pnr, cur)
        for paxphone in paxphones:
            returnlist.append(paxphone)
    return(returnlist)


def getcontactpnrhibird50webservice(flightno, date, dep, cur):

    pnrsformwebservice = getpnrwebservice(flightno, date, dep)
    print(len(pnrsformwebservice))
    pnrsformwebservice = set(pnrsformwebservice)
    returnlist = []
    for pnr in pnrsformwebservice:
        paxphones = getpaxcontactandticket(pnr, cur)
        for paxphone in paxphones:
            returnlist.append(paxphone)
    return(returnlist)

def getcontactpnrhibird50webserviceforcanceledflight(flightno, date, dep, cur):

    pnrsformwebservice = getpnrwebserviceforcancelflight(flightno, date, dep)
    print(len(pnrsformwebservice))
    pnrsformwebservice = set(pnrsformwebservice)
    returnlist = []
    for pnr in pnrsformwebservice:
        paxphones = getpaxcontactandticket(pnr, cur)
        for paxphone in paxphones:
            returnlist.append(paxphone)
    return(returnlist)


class GetPnrscontactincludewebservice(Resource):
    def post(self):

        #Step 1: Get posted data:

        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(
            postedData, "getpnrcontactincludewebservice")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        flightno = postedData["flightno"]
        date = postedData["date"]
        dep = postedData["dep"]

        #Step 2: Add the posted data
        #contacts = getcontactpnrs(flightno,date)
        cur = connectdb()
        contacts = getcontactpnrhibird50webservice(flightno, date, dep, cur)
        retMap = {
            'Message': contacts,
            'total': len(contacts),
            'Status Code': 200
        }
        response = jsonify(retMap)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


class GetPnrscontactincludewebserviceforcancelflight(Resource):
    def post(self):
        #Step 1: Get posted data:
        postedData = request.get_json()
        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(
            postedData, "getpnrcontactincludewebservice")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        flightno = postedData["flightno"]
        date = postedData["date"]
        dep = postedData["dep"]

        #Step 2: Add the posted data
        #contacts = getcontactpnrs(flightno,date)
        cur = connectdb()
        contacts = getcontactpnrhibird50webserviceforcanceledflight(flightno, date, dep, cur)
        retMap = {
            'Message': contacts,
            'total': len(contacts),
            'Status Code': 200
        }
        response = jsonify(retMap)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

api.add_resource(GetPnrscontactincludewebservice, "/getpnrscontacts")
api.add_resource(GetPnrscontactincludewebserviceforcancelflight, "/getpnrscontactsforcancelflight")


@app.route('/')
def hello_world():
    return "Wellcome to DatastreamAPI!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80) #0.0.0.0
   # app.run(debug=True, host='localhost', port=80)
