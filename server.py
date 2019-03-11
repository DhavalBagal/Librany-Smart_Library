# main.py
import cv2
from flask import Flask, render_template, Response, request,abort, jsonify
import os
import json
import qrcode
import subprocess

app = Flask(__name__)

@app.route('/issuebook', methods=['POST'])
def issuebook():

    if not request.json:
        abort(400)
        
    req = request.get_json(force=True)
    print(req['command'])
    if req['command']=="ISSUE":
        
        try:
            os.system("python3 issuebook.py")
        except:
            return jsonify(response='FAILED')
        
        return jsonify(response='OK')
    
    return jsonify(response='FAILED')

@app.route('/returnbook', methods=['GET','POST'])
def returnbook():

    if not request.json:
        abort(400)
        
    req = request.get_json(force=True)
    print(req['command'])
    if req['command']=="RETURN":

        try:
            os.system("python3 returnbook.py")
        except:
            return jsonify(response='FAILED')
            
        return jsonify(response='OK')
    
    return jsonify(response='FAILED')

@app.route('/cataloguebook', methods=['GET','POST'])
def cataloguebook():
    req = request.get_json(force=True)
    print(req['command'])
    if req['command']=="CATALOGUE":

        data = req['data']

        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=50, border=2)

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qrcodes/"+data+".png")

        return jsonify(response='OK')

    return jsonify(response='FAILED')
    
@app.route('/searchbook',methods=['GET','POST'])
def searchbook():

    if not request.json:
        abort(400)
        
    req = request.get_json(force=True)
    print(req['command'])
    if req['command']=="SEARCH":

        try:
            os.system("python3 searchbook.py")
        except:
            return jsonify(response='FAILED')
            
        return jsonify(response='OK')
    
    return jsonify(response='FAILED')

    """
    req = request.get_json(force=True)
    print(req['command'])
    if req['command']=="SEARCH":
        p = subprocess.check_output('python3 searchbook.py '+req['bookid'], shell=True)
        p = p.decode("utf-8")
        print(p)
        if 'NOT_FOUND' in p:
            return jsonify(response='NOT_FOUND')
        else :
            return jsonify(response=p)  
        
    
    return jsonify(response='FAILED')"""
        

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True, threaded=True)
