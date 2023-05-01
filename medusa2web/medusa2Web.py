from fileinput import filename
import gzip
import subprocess,os
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask, flash,request,render_template, redirect, url_for, jsonify,send_file,session
from threading import Thread

from utils import check_sequence, checkId

app = Flask(__name__)
a = Thread()
finished = False
target_filename=""
run=0
skipmap= False
references_filename=""
minimap2 = False
process=1
output_folder=""


def runScript(target_filename,output_folder,run,skipmap,process,minimap2,random,weight):
#print(target_filename)
    global finished
    
    if(skipmap == 'on'):
        skipmap='True'
    else:
        skipmap='False'
        
    if(minimap2 == 'on'):
        minimap2 ='True'
    else:
        minimap2 ='False'   

        
    result = subprocess.run(['./launcher.sh', target_filename, output_folder, run, skipmap, minimap2, process ,random,weight], stdout=subprocess.PIPE)
    t = result.stdout.decode('utf-8');
    finished= True
    #return render_template('index.html')
    
@app.route('/download')
def downloadFile():    
    global output_folder
    path="./results/"+output_folder+"/Scaffolds_"+output_folder+".tar.gz"
    return send_file(path, as_attachment=True, cache_timeout=0)
    
    
@app.route('/result')
def result():
    """ Just give back the result of your heavy work """
    return render_template('index_done.html', target_filename=target_filename, references_filename=references_filename, run=run, skipmap=skipmap, output_folder=output_folder, process=process, minimap2=minimap2, random=random, weight=weight)  


@app.route('/status')
def thread_status():
    """ Return the status of the worker thread """
    return jsonify(dict(status=('finished' if finished else 'running')))    
    


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/', methods = ['POST'])
def upload_file():
    global a
    global finished
    global target_filename 
    global run
    global skipmap
    global references_filename
    global output_folder
    global minimap2
    global process 
    global random
    global weight
    #blank all variables
    finished = False
    target_filename=""
    run=0
    skipmap= False
    references_filename=""
    minimap2 = False
    process=1
    output_folder=""
    
    
    finished = False
    target_file = request.files['target']
    references_files= request.files.getlist('references')
    output_folder = request.form['outputfolder']
    run = request.form['run']
    skipmap = request.form.get('skipmap')
    #minimap2 = request.form.get('minimap2')
    process = request.form['process']
    random =  request.form.get('graph_path_rd')
    weight = request.form.get('graph_path_wh')

    if request.form.get('aligning_algorithm') == 'option2':
        minimap2 = 'on'

    
    if random:
        random = "True"
    else:
        random ="False"
    
    if weight:
        weight = "True"
    else:
        weight ="False"	

    
    list_id=[]
        
    if output_folder!= '':
        os.mkdir("./results/"+output_folder)
        os.mkdir("./results/"+output_folder+"/target/")
        os.mkdir("./results/"+output_folder+"/references/")
    
    if target_file.filename != '':
        target = "./results/"+output_folder+"/target/"+target_file.filename
       # target_file.save("./results/"+output_folder+"/target/"+target_file.filename)
        target_file.save(target)
        target_filename = target_file.filename
        sequence=0
        found_new_line = 0
        list_id.clear()
        count_line = 0
        if(target_filename.find('.gz')>-1):
            with gzip.open(target,"rt") as file:
                for line in file.readlines():
                        count_line=count_line+1
                        if  found_new_line ==1:
                            if line[0]== ">":
                                flash(u'Something went wrong with your target genome: empty sequence found',
                                        'danger')
                                return redirect(url_for('index'))
                        if line[0]== ">":
                            found_new_line =1
                            id = checkId(line)
                            try:
                                if(list_id.index(id)>=0):
                                    flash(u'Something went wrong with your target genome: duplicate id found',
                                            'danger')
                                    return redirect(url_for('index'))
                                else:
                                    list_id.append(id)
                            except Exception as e:
                                list_id.append(id)

                        else:
                            found_new_line =0
                            sequence = check_sequence(line)
                            if sequence == 1:
                                    flash(u'Something went wrong with your target genome::one or more sequences contain non DNA characters',
                                            'danger')
                                    return redirect(url_for('index'))
                if count_line == 1:
                        flash(u'Something went wrong with your target genome: file empty',
                                'danger')
        else:
            try:
                with open(target,"r") as file:
                    for line in file.readlines():
                        count_line=count_line+1
                        if  found_new_line ==1:
                            if line[0]== ">":
                                flash(u'Something went wrong with your target genome: empty sequence found',
                                        'danger')
                                return redirect(url_for('index'))
                        if line[0]== ">":
                            found_new_line =1
                            id = checkId(line)
                            try:
                                if(list_id.index(id)>=0):
                                    flash(u'Something went wrong with your target genome: duplicate id found',
                                            'danger')
                                    return redirect(url_for('index'))
                                else:
                                    list_id.append(id)
                            except Exception as e:
                                list_id.append(id)

                        else:
                            found_new_line =0
                            sequence = check_sequence(line)
                            if sequence == 1:
                                    flash(u'Something went wrong with your target genome:one or more sequences contain non DNA characters',
                                            'danger')
                                    return redirect(url_for('index'))
                    if count_line == 1:
                        flash(u'Something went wrong with your target genome: file empty',
                                'danger')
                        return redirect(url_for('index'))
            except Exception as e:
                print(e)
                flash(u'unrecognized compression type, please use GZIP for deflating your files',
                    'danger')
                return redirect(url_for('index'))
                        
    else:
        flash(u'Something went wrong with your target genome',
                'danger ')
        return redirect(url_for('index'))
        
    i=1
    for currentRef in references_files:
        if currentRef.filename != '':
            #currentRef.save("./results/"+output_folder+"/references/"+currentRef.filename)
            current_reference =  "./results/"+output_folder+"/references/"+currentRef.filename
            currentRef.save(current_reference)
            sequence=0
            found_new_line = 0
            list_id.clear()
            count_line=0
            if(currentRef.filename.find('.gz')>-1):
                with gzip.open(current_reference,"rt") as file:
                    for line in file.readlines():
                            count_line=count_line+1
                            if  found_new_line ==1:
                                if line[0]== ">":
                                    flash(u'Something went wrong with your reference genome: empty sequence found',
                                            'danger')
                                    return redirect(url_for('index'))
                            if line[0]== ">":
                                found_new_line =1
                                id = checkId(line)
                                try:
                                    if(list_id.index(id)>=0):
                                        flash(u'Something went wrong with your reference genome: duplicate id found',
                                                'danger')
                                        return redirect(url_for('index'))
                                    else:
                                        list_id.append(id)
                                except Exception as e:
                                    list_id.append(id)

                            else:
                                found_new_line =0
                                sequence = check_sequence(line)
                                if sequence == 1:
                                        flash(u'Something went wrong with your reference genome: one or more sequences contain non DNA characters',
                                                'danger')
                                        return redirect(url_for('index'))
                    if count_line == 1:
                        flash(u'Something went wrong with your reference genome: file empty',
                                'danger')
                        return redirect(url_for('index'))
            else:
                try:
                    with open(current_reference,"r") as file:
                        for line in file.readlines():
                            if  found_new_line ==1:
                                count_line=count_line+1
                                if line[0]== ">" :
                                    flash(u'Something went wrong with your reference genome: empty sequence found',
                                            'danger')
                                    return redirect(url_for('index'))
                            if line[0]== ">":
                                found_new_line =1
                                id = checkId(line)
                                try:
                                    if(list_id.index(id)>=0):
                                        flash(u'Something went wrong with your reference genome: duplicate id found',
                                                'danger')
                                        return redirect(url_for('index'))
                                    else:
                                        list_id.append(id)
                                except Exception as e:
                                    list_id.append(id)

                            else:
                                found_new_line =0
                                sequence = check_sequence(line)
                                if sequence == 1:
                                        flash(u'Something went wrong with your reference genome: one or more sequences contain non DNA characters',
                                                'danger')
                                        return redirect(url_for('index'))
                        if count_line == 1:
                            flash(u'Something went wrong with your reference genome: file empty',
                                    'danger')
                            return redirect(url_for('index'))
                    
                except Exception as e:
                    flash(u'unrecognized compression type, please use GZIP for deflating your files',
                        'danger')
                    return redirect(url_for('index'))
        if i==1:
            references_filename= references_filename + currentRef.filename
        else:
            references_filename= references_filename + ", " + currentRef.filename
        i=i+1

    a = Thread(target=runScript, args=(target_filename,output_folder,run,skipmap,process,minimap2,random,weight))
    a.start()
    return render_template('index_loading.html', target_filename=target_filename, references_filename=references_filename, run=run, skipmap=skipmap, output_folder=output_folder, process=process, minimap2=minimap2, random=random,weight=weight)       

  
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'super secret key'
    app.run(debug=True)


