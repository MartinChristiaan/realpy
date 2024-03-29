from flask import Flask,Response
from flask import render_template
import os
from os import path,system
from flask import request
import json
from flask_cors import CORS
import shutil
# Model Definition
import math
import serialization
import numpy as np
import types
from enum import Enum
import video_capture
#pathToPython = "C:\\Users\\marti\\Source\\Repos\\VideoHeartbeatInterface\\src\\pythonTypes.fs"

def create_type_provider(classlibrary,pathToPython):
    lines = ["module PythonTypes \n"]
    lines +=["type ClassName = string \n"]
    lines +=["type FieldName = string \n"]
    lines +=["type EnumName = FieldName \n"]
    lines +=["type EnumOptions = string list \n"]
    lines +=["type MethodName = FieldName \n"]
    
    for c in classlibrary:
        classname = type(c).__name__
        for field in dir(c):
            attr = getattr(c,field)
            if type(attr)== types.MethodType:
               lines+=["let " + classname + "_"+ str(field) + " : ClassName*MethodName = \"" + classname+"\",\"" + str(field)+"\" \n"]
            elif isinstance(attr, Enum):
                choices = "\";\"".join(dir(type(attr))[:-4])
                print(choices)
                lines+=["let " + classname + "_"+ str(field) + " : ClassName*EnumName = \"" + classname+"\",\"" + str(field)+"\" \n"]
                lines+=["let " + classname + "_"+ str(field) + "_options  : EnumOptions = [\"" + choices + "\"] \n"]
                
            else:
                 lines+=["let " + classname + "_"+ str(field) + " : ClassName*FieldName = \"" + classname+"\",\"" + str(field)+"\" \n"]
    f = open(pathToPython,"w")
    f.writelines(lines)
def setup_template(pathToClient,use_camera):
    
    if os.path.exists(pathToClient):
        pass
    else:
        print("copying")
        shutil.copytree("PyTypeClient",pathToClient)
        if not use_camera:
            htmlfile = pathToClient + "/public/index.html"
            f = open(htmlfile,'r')
            lines = f.readlines()
            f.close()
    
            f = open(htmlfile,'w')
            del lines[25]
            f.writelines(lines)
            f.close()

def create_server(classlibrary,main,pathToClient,use_camera=True):
    """Receives list of uiElements that handle interaction with their specified classes"""
    # Check if a path can be found,otherwize create the app
    if use_camera:
        video_capture.main = main
    else:
        # repeat within loop
        pass
    setup_template(pathToClient,use_camera)
    app = Flask(__name__)
    CORS(app)
    uiElements = []
    classnames = [type(c).__name__ for c in classlibrary]
    classlookup = dict(zip(classnames, classlibrary))
    create_type_provider(classlibrary,pathToClient + "/src/pythonTypes.fs")
    
    @app.route("/")
    @app.route('/getTargets',methods=['PUT'])
    def get_targets(): 
        classnamescol = request.form['classname'].split('/')
        fieldnamescol = request.form['fieldname'].split('/')
        
        data = []
        for (classnames,fieldnames) in zip(classnamescol,fieldnamescol):
            subclassnames = classnames.split()
            subfieldnames = fieldnames.split()
            subdata = []
            for (classname,fieldname) in zip(subclassnames,subfieldnames):
                item = classlookup[classname].__dict__[fieldname]
                if isinstance(item, list) or isinstance(item,np.ndarray):
                    liststring = [str(el) for el in item]
                    subdata.append("@".join(liststring))
                else:
                    subdata.append(str(item))
            data.append(",".join(subdata))
        #print(data)
        return "/".join(data)
    @app.route('/updateTarget',methods=['PUT'])
    def update_target():
        classname = request.form['classname']
        fieldname = request.form['fieldname']
        valuetype = request.form['valuetype']
        value = request.form['value']
        
        if valuetype == "float":
            classlookup[classname].__dict__[fieldname] = float(value)
        if valuetype == "bool":
            value = classlookup[classname].__dict__[fieldname]
            classlookup[classname].__dict__[fieldname] = not value
        if valuetype == "string":
            classlookup[classname].__dict__[fieldname] = value
        if valuetype == "enum":
            enum = classlookup[classname].__dict__[fieldname]
            classlookup[classname].__dict__[fieldname] = type(enum)[value]  
          
        return ""
    
    @app.route('/invokeMethod',methods=['PUT'])
    def invoke_method():
        classname = request.form['classname']
        method = request.form['method']    
        getattr(classlookup[classname], method)()
        return ""
 
    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    @app.route('/video_feed')
    def video_feed():
        return Response(gen(video_capture.Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
   
    return app




