from . import main
from ..utils import *
from flask import jsonify, render_template,redirect,flash, request,url_for,session

''' errors '''
@main.app_errorhandler(404)
def error404(error):
    return render_template("errorpage/error_404.html"),404

@main.app_errorhandler(500)
def error500(error):
    return render_template("errorpage/error_500.html"),500


'''pages'''

#查看地图
@main.route('/',methods=['GET','POST'])
def index():
    return render_template('mainpage/view.html')

#上传温度
@main.route('/uploadtemp',methods=['GET','POST'])
def uploadtemp():
    return render_template('mainpage/uploadtemp.html')

#修改温度
@main.route('/edittemp',methods=['GET','POST'])
def edittemp():
    return render_template('mainpage/edittemp.html')

#删除温度
@main.route('/deletetemp',methods=['GET','POST'])
def deletetemp():
    return render_template('mainpage/deletetemp.html')

#预测温度
@main.route('/predtemp',methods=['GET','POST'])
def predtemp():
    return render_template('mainpage/predtemp.html')

'''api'''
# 增（上传文件）
@main.route("/action/uploadtemp",methods=['GET','POST'])
def action_uploadtemp():
    if request.method=='POST':
        files=request.files.getlist("files")
        success_files=[]
        fail_files=[]
        duplicated_files=[]
        print(files)
        for file in tqdm(files):
            fp=f"{FILE_DIRS}/{file.filename}"
            file.save(fp)
            upload_result = upload_sst(fp)
            if upload_result == "success":
                success_files.append(file.filename)
            elif upload_result == "duplicated":
                duplicated_files.append(file.filename)
            else:
                fail_files.append(file.filename)
            os.remove(fp)
        return jsonify({
            "success_files":success_files,
            "fail_files":fail_files,
            "duplicated_files":duplicated_files
        })
    
    return jsonify({})

# 查（范围查询）
@main.route("/action/query_range",methods=['GET','POST'])
def action_query_by_range():
    if request.method=='POST':
        data=request.get_json()
        query_result=query_sst_byrange(
            time=data["time"],
            lat_range=data["lat"],
            lon_range=data["lon"]
        )
        return jsonify(query_result)
    return jsonify({})

# 改
@main.route("/action/update",methods=['GET','POST'])
def action_update_sst():
    if request.method=='POST':
        data=request.get_json()
        success,message=update_sst(
            time=data[0],
            lon=data[1],
            lat=data[2],
            sst=data[3],
            ssta=data[4]
        )
        return jsonify({
            "success":success,
            "message":message
        })
    return jsonify({})

# 删（删除一个月的数据）
@main.route("/action/delete_sst",methods=['GET','POST'])
def action_delete_sst():
    if request.method=='POST':
        data=request.get_json()
        del_num=delete_sst(data["time"])
        return jsonify({
            "message":f"成功删除{del_num}条数据。"
        })
    return jsonify({})

# 查（查某个位置）
@main.route("/action/query_position",methods=['GET','POST'])
def action_query_position():
    if request.method=='POST':
        data=request.get_json()
        result=query_sst(data["time"],data["lat"],data["lon"])
        if result is None:
            sst=ssta="N/A"
        else:
            sst=result.sst if result.sst is not None else "N/A"
            ssta=result.ssta if result.ssta is not None else "N/A"
        return jsonify({
            "sst":sst,
            "ssta":ssta
        })
    return jsonify({})

# 预测（预测某个位置）
@main.route("/action/pred_sst",methods=['GET','POST'])
def action_pred_sst():
    if request.method=='POST':
        data=request.get_json()
        sst,ssta=pred_sst(data["lat"],data["lon"],data["month"])
        sst=sst if sst is not None else "N/A"
        ssta=ssta if ssta is not None else "N/A"
        return jsonify({
            "sst":sst,
            "ssta":ssta,
        })
    return jsonify({})