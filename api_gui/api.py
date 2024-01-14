from flask import stream_with_context, Response, Flask, jsonify,\
                Markup, request, render_template, send_from_directory,\
                make_response, redirect, escape
import json
import time
import json
from multiprocessing import Process
import subprocess
import argparse
import io
import sys
import glob
from kwic import kwic_gen
from freqs import get_freqs 
import os
from collections import defaultdict
import hashlib
from werkzeug.utils import secure_filename#, escape
import uuid
from dep_search import redone_expr
dd = defaultdict(dict)
from re import finditer, compile
from copy import deepcopy
from functools import partial
import markdown
import threading
from time import sleep


main_page_called = 0
unsaved_query_logs = ""
main_page_timer = time.time()
query_log_timer = time.time()
main_page_call_lock = threading.Lock()
query_log_lock = threading.Lock()
config_folder = os.getenv('CONFIG_FOLDER', '/configs/')
if not config_folder.endswith('/'):
    config_folder += '/'
log_folder = os.getenv('LOG_FOLDER', '/api_gui/logs/')
if not log_folder.endswith('/'):
    log_folder += '/'
index_folder = os.getenv('INDEX_FOLDER', '/indexes/')
if not index_folder.endswith('/'):
    index_folder += '/'


def update_main_page_called_file(main_page_calls):
    global log_folder
    if os.path.exists(log_folder + "main_page_called.txt"):
        with open(log_folder + "main_page_called.txt", "r") as file:
            try:
                saved_number_of_calls = int(file.read().strip())
            except:
                saved_number_of_calls = 0
    else:
        saved_number_of_calls = 0
    with open(log_folder + "main_page_called.txt", "w") as file:
        file.write(str(saved_number_of_calls + main_page_calls))
    
  
def update_query_logs(new_query_logs):
    global log_folder
    with open(log_folder + "queries.txt", "a") as file:
        file.write(new_query_logs)


with open(index_folder + "xpos_tags.json", "r") as xpos_tags_file:
    xpos_tags = json.load(xpos_tags_file)


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(THIS_DIR, "res")

def match_xpos_tags(xpos_tag, prev_found_xpos_tags, query):
    if xpos_tag[:-1] in prev_found_xpos_tags:
        prev_found_xpos_tags.add(xpos_tag)
        return False
    if query.search(xpos_tag):
        prev_found_xpos_tags.add(xpos_tag)
        return True
    return False    
    

def get_all_xpos_roots(xpos_query, xpos_tags_from_db): 
    xpos_query = xpos_query.replace(".", "[A-Za-z]")
    print("query:", xpos_query)
    query = compile(xpos_query)
    prev_found_xpos_tags = set()
    found_xpos_tags = filter(partial(match_xpos_tags, prev_found_xpos_tags=prev_found_xpos_tags, query=query), xpos_tags_from_db)
    queries = ["X=" + tag[:-1] for tag in found_xpos_tags]
    if len(queries) > 1:
        return "( " + " | ".join(queries)  + " ) "
    return " | ".join(queries)


def process_xpos_regex(query, dbs):
    global xpos_tags
    xpos_tags_from_db = []
    for db in dbs.strip().split(","):
        if db in xpos_tags:
            xpos_tags_from_db += xpos_tags[db]
    
    xpos_tags_from_db = list(set(xpos_tags_from_db))
    iter = finditer(r"X=[\s\S]*?[ \|\&]", query + " ")
    cur_position = 0
    processed_string = ""
    for xpos_query_start, xpos_query_end in [(m.start(0), m.end(0)) for m in iter]:
        processed_string += query[cur_position:xpos_query_start] + get_all_xpos_roots(query[xpos_query_start+2:xpos_query_end-1] + ">", xpos_tags_from_db)
        cur_position = xpos_query_end - 1
    processed_string += query[cur_position:]
    return processed_string


def get_uuid():
    uu = uuid.uuid4()
    return str(uu)


def res_file(basename):
    return os.path.join(RES_DIR, basename)


def query_process(dbs, query, langs, ticket, limit=10000, case=False, rand=False, save_to_logs=True):
    global unsaved_query_logs
    global query_log_timer
    global config_folder
    if save_to_logs:
        query_log_lock.acquire()
        
        unsaved_query_logs += json.dumps({"query": query, "dbs": dbs, "limit": limit, "case": case, "random": rand}) + "\n"
        if time.time() - query_log_timer > 20:
            query_log_timer = time.time()
            update_query_logs(unsaved_query_logs)
            unsaved_query_logs = ""
     
        query_log_lock.release()

    print ('!!!', str(langs))
    print(dbs, "|", query, "|", langs, "|", ticket)
    query = process_xpos_regex(query, dbs)
    print("xpos processed query", query)
    limit = int(limit)
    try:


        inf = open(config_folder + 'config.json','r')
        xx = json.load(inf)
        inf.close()
        print(xx)

        allow_unlimited_limit = xx['allow_unlimited_limit']
        max_result_limit = xx['max_result_limit']
        
        print(allow_unlimited_limit, max_result_limit)

        if limit==0 and not allow_unlimited_limit:
            limit = max_result_limit 

        if limit > max_result_limit:
            limit = max_result_limit
    except:
        pass

    xdbs = get_db_locations()
    print(xdbs)

    #Replace with call
    #open res file
    outf_err = open(res_file(ticket+'.err'),'w')


    xdb_string = []
    langs = langs.split(',')
    for x in dbs.split(','):
        if len(langs) > 0 and len(langs[0]) > 0:
            langs_in_db = get_db_langs([x])
            if len(set(langs).intersection(set(langs_in_db))) > 0:
                xdb_string.append(xdbs[x])
        else:
            xdb_string.append(xdbs[x])
            
    db_string = ','.join(xdb_string)
    if len(db_string) < 1:
        db_string = xdbs[dbs]
    
    os.system('python3 res_cleaner.py &')
    langs = ','.join(langs)
    
    if rand:
        rand = "1"
    else:
        rand = "0"
    
    if len(langs) > 0:
        if case == 'true':
            p = subprocess.Popen(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--langs', langs, '--chop_dir', RES_DIR, '--chop_ticket', ticket, '--case', query, '--rand', rand], cwd='/api_gui')
            print (' '.join(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--langs', langs, '--chop_dir', RES_DIR, '--chop_ticket', ticket, '--case', query, '--rand', rand]))
        else:
            p = subprocess.Popen(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--langs', langs, '--chop_dir', RES_DIR, '--chop_ticket', ticket,  query, '--rand', rand], cwd='/api_gui')
            print (' '.join(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--langs', langs, '--chop_dir', RES_DIR, '--chop_ticket', ticket,  query, '--rand', rand]))
    else:
        if case == 'true':
            p = subprocess.Popen(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--chop_dir', RES_DIR, '--chop_ticket', ticket, '--case', query, '--rand', rand], cwd='/api_gui')
            print (' '.join(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--chop_dir', RES_DIR, '--chop_ticket', ticket, '--case', query, '--rand', rand]))
        else:
            p = subprocess.Popen(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--chop_dir', RES_DIR, '--chop_ticket', ticket,  query, '--rand', rand], cwd='/api_gui')
            print (' '.join(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '2', '--chop_dir', RES_DIR, '--chop_ticket', ticket,  query, '--rand', rand]))

    #oug = open(res_file("ticket.res"), 'wb')
    #p = subprocess.Popen(['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '4', '--chop_dir', RES_DIR, '--chop_ticket', ticket , query], cwd='../')
    
    #print ('!!!!!', ['python3', 'query.py', '-d', db_string, '-m', str(limit), '--context', '4', '--chop_dir', RES_DIR, '--chop_ticket', ticket , query])
    xoutf = open(res_file(ticket + '.json'),'wt')
    xoutf.write(json.dumps({'query':query, 'dbs':dbs, 'langs':langs, 'ticket':ticket, 'limit': limit}))
    xoutf.close()

    outf_files = {}
    from collections import defaultdict
    counts = defaultdict(int)
    step = 10
    buffer = bytes()
    langs = set()
    lang = '-'

    outfs = {}

    err_out = open(res_file(ticket + '_err'), 'wb')
    '''
    for l in p.stderr:
        print (l)
        if b'compiled' in l :break
        if b"redone_expr.ExpressionError" in l:
            err_out.write(l.split(b':')[1])
        if l.startswith(b"HERE"):
            err_out.write(l)
            break
    '''        
    err_out.close()

    tree = []
    print ('FUGG')
    empty_cnt = 0
    #p.wait()
    '''
    while True:
        print ('poll', p.poll())   
        l = p.stdout.readline()
        l = l.decode('utf8')
        print (l)
        if len(l) < 1:
            empty_cnt += 1
            if empty_cnt > 10:
                print ('!!!') 
                break
            continue
        else:
            empty_cnt = 0
            tree.append(l)
        if len(l)<1 or l.startswith('\n'):
            lang = 'unknown'
            if tree[0].startswith('# lang'):
                lang = tree[0].split(':')[-1].strip()
                if lang not in langs:
                    langs.add(lang)
                    xx = open(res_file(ticket + '.langs'), 'w')
                    xx.write(json.dumps(list(langs)))
                    xx.close()
            
            if counts[lang]%10==0:
                if lang not in outfs.keys():
                    outfs[lang] = open(res_file(lang + '_' + ticket + '_' + str(round(counts[lang],-1)) + '.conllu'), 'a+t')
                else:
                    outfs[lang].close()
                    outfs[lang] = open(res_file(lang + '_' + ticket + '_' + str(round(counts[lang],-1)) + '.conllu'), 'a+t')                    
            counts[lang] += 1
            for tl in tree:
                outfs[lang].write(tl)
            tree = []


    for of in outfs.keys():
        outfs[of].close()
    '''
    p.wait()
    print ('END')    
    outf = open(res_file(ticket+'.done'),'w')
    outf.close()                    

def get_passhash(passw):
    salt = 'erthya!!!4235'
    return hashlib.sha256(salt.encode() + passw.encode()).hexdigest()

        
@app.route('/drevesnik/help/', defaults={'site_lang': 'sl'})
@app.route('/drevesnik/help/<site_lang>/')
def help(site_lang):
    global config_folder
    inf = open(config_folder + f'dep-search_query-lang_original_{site_lang}.md', 'r')
    md_text = inf.read()
    inf.close()
    return "<html><head><style>body\n{\n  padding-left: 40px; font-family: 'Open Sans'; font-size: 14px;}\n}\n></style><body>" + markdown.markdown(md_text)  + "</head></body></html>"


@app.route('/drevesnik/remove_db/<db_name>')
def rmdb(db_name):
    global config_folder

    db_r = db_name
    inf = open(config_folder + 'config.json', 'r')
    xx = json.load(inf)
    inf.close()
    
    fd = get_db_locations()

    if check_creds(request):
        os.system('rm -rf ' + fd[db_r])
        os.system('cd ..; python3 docker_add_dbs.py')
        return redirect("/db_config")
    else:
        return render_template("login.html")

@app.route('/drevesnik/index_db', methods=['POST'])
def chansge_pw():
    global config_folder

    inf = open(config_folder + 'config.json', 'r')
    xx = json.load(inf)
    inf.close()
    
    db_name = request.form['name']
    db_lang = request.form['lang']
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(xx['db_folder'] + filename)    

    if check_creds(request):
        outf = open('index_' + filename + '.sh','wt')
        outf.write('cd ..; cat ' + xx['db_folder'] + filename + ' | python3 build_index.py -d ' + xx['db_folder'] + '/' + db_name + ' --lang ' + db_lang + ' 2>&1 > ' + xx['db_folder'] + filename + '.log\n')
        outf.write('python3 docker_add_dbs.py\n')
        outf.close()
        os.system('chmod +x ' + 'index_' + filename + '.sh')
        os.system('sh ' + 'index_' + filename + '.sh &')
        #os.system('cd ..; cat ' + xx['db_folder'] + filename + ' | python3 build_index.py -d ' + xx['db_folder'] + '/' + db_name + ' --lang ' + db_lang + ' 1&2> ' + xx['db_folder'] + filename + '.log')
        #os.system('cd ..; python3 docker_add_dbs.py')
        
    return redirect("/check_index/" + filename + '.log')


@app.route('/drevesnik/check_index/<filename>')
def rrt(filename):
    global config_folder
    if check_creds(request):
        inf = open(config_folder + 'config.json', 'r')
        xx = json.load(inf)
        inf.close()
        inf = open(xx['db_folder'] + filename,'rt')
        ff = inf.read()
        ff = ff.replace('\n','<br>')
        inf.close()
    return render_template('check_log.html', log=ff)

@app.route('/drevesnik/db_config')
def db_config():
    global config_folder

    inf = open(config_folder + 'config.json', 'r')
    xx = json.load(inf)
    inf.close() 

    xxx = ''
    dd = get_db_locations()
    for k in dd.keys():
        #
        #xxx += '<a href=' + '/remove_db/' + k + '>Remove ' + k + '</a><br>'
        xxx += '<input type="button" value="Remove ' + k + '" onclick="if(window.confirm(\'Sure?\')){window.location = \'' + '/remove_db/' + k + '\';}" /><br>'


    if check_creds(request):
        return render_template("db_config.html", dbs=xxx)
    return render_template('login.html')


def check_creds(req):
    
    try:
        session_id = req.cookies.get('session_id')
        
        inf = open('sessions','rt')
        xln = inf.readline()
        inf.close()
        right_sess_id, xtime = xln.strip().split('\t')
        print (session_id, right_sess_id, float(xtime) > time.time())
        if session_id == right_sess_id and time.time() < float(xtime):
            return True
        else:
            return False
    except:
        return False

    
@app.route('/drevesnik/do_query/<dbs>/<query>/<m>/<langs>/')
def xxquery_process(dbs, query, m, langs):

    xdbs = get_db_locations()

    limit = 5000
    if len(langs) > 0:
        p = subprocess.Popen(['python3', 'query.py', '-d', xdbs[dbs], '-m', m, '--langs', langs, query], cwd='../', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(['python3', 'query.py', '-d', xdbs[dbs], '-m', m, query], cwd='../', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def generate():
        for oo in p.stdout:
            yield oo

    return Response(generate(), mimetype='text')



#https://stackoverflow.com/questions/34344836/will-hashtime-time-always-be-unique
def unique_id():
    return str(hash(time.time()))


@app.route('/drevesnik/static/<path:path>')
def send_js(path):
    print (path)
    return send_from_directory('static', path)


@app.route('/drevesnik/translations/<path:path>')
def send_translations(path):
    print (f'{config_folder}html_translations',path)
    return send_from_directory(f'{config_folder}html_translations', path)


@app.route('/drevesnik/get_branding')
def send_branding():
    return send_from_directory(f'{config_folder}', 'branding.json')


@app.route('/drevesnik/', defaults={'site_lang':'sl'})
@app.route('/drevesnik/<site_lang>')
def mnf(site_lang):
    global main_page_called
    global main_page_timer
    global config_folder
    main_page_call_lock.acquire()
    main_page_called += 1
    if time.time() - main_page_timer > 20:
        main_page_timer = time.time()
        update_main_page_called_file(main_page_called)
        main_page_called = 0
    main_page_call_lock.release()
    
    return render_template("qx_hack.html", site_lang=site_lang)

@app.route('/drevesnik/get_dbs_json/')
def gdsb():
    global index_folder
    inf = open(index_folder + 'dbs.json','rt')
    dbs = json.load(inf)
    inf.close()
    return jsonify([dbs[key] for key in dbs])


def flatten(current, key='', result=dict()):
    if isinstance(current, dict):
        for k in current:
            new_key = k
            flatten(current[k], new_key, result)
    else:
        result[key] = current
    return result


def get_db_locations():
    global index_folder

    inf = open(index_folder + 'dbs.json','rt')
    dbs = json.load(inf)
    inf.close()
    
    dbs = {name: index_folder + name for name in dbs}

    flat_dict = flatten(dbs)
        

    return flat_dict




def get_node_with_kids(dd, db_desc, xid):
    import natsort
    tr = []
    for ixx, kid in enumerate(natsort.natsorted(dd.keys())):
        #is end node?
        if kid not in db_desc:
            db_desc[kid] = kid
        if isinstance(dd[kid], str):
            if len(xid) > 0:
                tr.append({'id': str(kid), 'text': str(db_desc[kid]), 'children':[], "state": {"opened" : True}})
            else:
                tr.append({'id': str(kid), 'text': str(db_desc[kid]), 'children':[], "state": {"opened" : True}})
        else:
            if len(xid) > 0:
                tr.append({'id': str(kid), 'text': str(db_desc[kid]), 'children':get_node_with_kids(dd[kid], xid + '-' + str(ixx)), "state": {"opened" : False}})
            else:
                tr.append({'id': str(kid), 'text': str(db_desc[kid]), 'children':get_node_with_kids(dd[kid], xid + '-' + str(ixx)), "state": {"opened" : False}})
    return tr
    


    return json.dumps(xx)





@app.route("/drevesnik/get_dbs/")
def gdb():
    dbs = get_db_locations()
    xx = []
    for k in dbs:
        xx.append(k)
    return json.dumps(xx)

@app.route("/drevesnik/get_langs/<db>")
def dbl(db):

    dbs = get_db_locations()
    
    inf = open(dbs[db] + '/langs', 'rt')
    
    xx = []
    for ln in inf:
        xx.append(ln.strip())

    inf.close()
    xx.sort()

    return jsonify(xx)

@app.route("/drevesnik/get_langs_post/", methods=['POST'])
def dbdl():

    dbs = request.form.getlist('data[]')
    return jsonify(get_db_langs(dbs))
    
def get_db_langs(dbs):
    fdbs = get_db_locations()
    print (fdbs)
    xx = []
    for db in dbs:
        print(fdbs[db] + '/langs')
        inf = open(fdbs[db] + '/langs', 'rt')
        for ln in inf:
            xx.append(ln.strip())

        inf.close()
    xx.sort()

    return xx


def file_generator_lang(ticket, lang):

    step = 10
    c = 0
    while True:
        fname = res_file(lang + '_' + ticket + '_' + str(c) + '.conllu')
        if not os.path.isfile(fname):
            break
        inf = open(fname, 'r')
        for l in inf:
            yield l
        inf.close()
        c += step
        

def file_generator(ticket):

    files = glob.glob(res_file('*'+ticket+'*.conllu'))
    files.sort()

    sent_files = set()
    while True:

        #
        for f in files:
            inf = open(f,'r')
            for l in inf:
                yield l
            inf.close()
            sent_files.add(f)

        #
        xfiles = set(glob.glob(res_file('*'+ticket+'*.conllu')))
        xx = xfiles - sent_files
        if len(xx) > 0:
            #
            files = list(xx)
        else:
            break
            

def start_query_for_cache(cached_calls):
    with open("skip_cache_clean.txt", "w") as cache_file:
        with open(cached_calls, "r") as call_file:
            for line in call_file:
                dbs, query, langs, limit, case, rand, small_sent, ticket = line.strip().split("\t")       
                print("calling", dbs, query, langs, limit, case, rand, small_sent, ticket)
                rand = rand=='true'
                
                case = case=='true'

                if small_sent == 'true':
                    query = query.strip() + " & S=small"
                p = Process(target=query_process, args=(dbs,query, langs, ticket, limit, case, rand, False))
                p.start()
                cache_file.write(ticket + "\n")


start_query_for_cache(config_folder + "cache_calls.txt")


@app.route("/drevesnik/download/<ticket>")
def dl(ticket):

    content_gen = file_generator(ticket)
    response = Response(stream_with_context(content_gen))

    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "inline; filename=" + ticket + '.conllu'

    return response


@app.route("/drevesnik/download/<ticket>/<lang>")
def dll(ticket, lang):

    content_gen = file_generator_lang(ticket, lang)
    response = Response(stream_with_context(content_gen))

    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "inline; filename=" + lang + '_' + ticket + '.conllu'

    return response

@app.route("/drevesnik/kwic_download/<ticket>")
def kdl(ticket):

    content_gen = kwic_gen(res_file('*' + ticket + '*.conllu'))
    response = Response(stream_with_context(content_gen))

    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "inline; filename=" + ticket + '.tsv'

    return response


@app.route("/drevesnik/kwic_download/<ticket>/<lang>")
def kdll(ticket, lang):

    content_gen = kwic_gen(res_file(lang + '_' + ticket + '*.conllu'))
    response = Response(stream_with_context(content_gen))

    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "inline; filename=" + lang + '_' + ticket + '.tsv'

    return response

relx = ["dependent_words","dependent_lemmas", "left_words","left_lemmas", "right_words","right_lemmas","parent_words","parent_lemmas","deptypes_as_dependent","deptypes_as_parent","hit_words","hit_lemmas"]


@app.route('/drevesnik/freqs/<ticket>', defaults={'site_lang':'sl'})
@app.route("/drevesnik/freqs/<site_lang>/<ticket>")
def ffr(ticket, site_lang):
    global relx
    global config_folder
    with open(f'{config_folder}statistics_translations_{site_lang}.json') as translation_file:
        translations = json.load(translation_file)
    ret = get_freqs(res_file('*_' + ticket + '*.conllu'), site_lang)
    return render_template(f'freqs.html', ret=ret, relx=[translations[i] for i in relx], most_common = translations["most_common"],
        count = translations["count"], xurl=f"/drevesnik/json_freqs/{site_lang}/" + ticket, site_lang=site_lang)


@app.route('/drevesnik/json_freqs/<ticket>', defaults={'site_lang':'sl'})
@app.route("/drevesnik/json_freqs/<site_lang>/<ticket>")
def fffr(ticket, site_lang):

    ret = json.dumps(get_freqs(res_file('*_' + ticket + '*.conllu'), site_lang), indent=4, sort_keys=True)

    response = Response(stream_with_context(ret))

    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Disposition'] = "inline; filename=" + ticket + '.json'

    return response


@app.route("/drevesnik/json_freqs/<ticket>/<lang>")
def fr(ticket, lang):

    ret = json.dumps(get_freqs(res_file(lang + '_' + ticket + '*.conllu')), indent=4, sort_keys=True)
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")    
    return resp



@app.route("/drevesnik/start_query/<dbs>/<query>/<limit>/<case>/<rand>")
def hello_qc(dbs, query, limit, case):

    langs = ''

    case = case=='true'
    rand = rand=='true'
    ticket = unique_id()
    p = Process(target=query_process, args=(dbs,query, langs, ticket, limit, case, rand))
    p.start()
    return ticket

@app.route("/drevesnik/start_query/<dbs>/<query>/<langs>/<limit>/<case>/<rand>")
def hello_qcc(dbs, query, langs, limit, case):

    case = case=='true'
    rand = rand=='true'

    ticket = unique_id()
    p = Process(target=query_process, args=(dbs,query, langs, ticket, limit, case, rand))
    p.start()
    return ticket

@app.route("/drevesnik/start_query/", methods=['POST'])
def start_post():


    dbs = request.form['dbs']
    #dbs = "sl"
    query = request.form['query']
    langs = request.form['langs']
    limit = request.form['limit']
    case = request.form['case']
    rand = request.form['rand']
    small_sent = request.form['small_sent']
    
    rand = rand=='true'
    
    case = case=='true'


    print ('case', case)
    print(dbs, "|", query, "|", langs, "|", limit, "|", case)

    ticket = unique_id()
    print (dbs,query, langs, ticket, limit, case)   
    
    if small_sent == 'true':
        query = query.strip() + " & S=small"
    p = Process(target=query_process, args=(dbs,query, langs, ticket, limit, case, rand))
    p.start()
    return ticket

from dep_search import redone_expr#, get_tags

"""
@app.route("/get_tags/", methods=['POST'])
def tagset():

    dbs = request.form['dbs']
    langs = request.form['langs']
    
    xdbs = get_db_locations()

    xdb_string = []
    langs = langs.split(',')
    for x in dbs.split(','):
        if len(langs) > 0 and len(langs[0]) > 0:
            langs_in_db = get_db_langs([x])
            if len(set(langs).intersection(set(langs_in_db))) > 0:
                xdb_string.append(xdbs[x])
        else:
            try:
                xdb_string.append(xdbs[x])
            except:
                pass
    
    dep_types, pos, tags = get_tags.get_tags_list(xdb_string)
    dep_types, pos, tags = list(dep_types), list(pos), list(tags)

    dep_types.sort()
    pos.sort()
    tags.sort()

    return jsonify([dep_types, pos, tags])
"""

@app.route("/drevesnik/check_query_syntax/", methods=['POST'])
def chek_syn():
    query = request.form['query']
    return jsonify(redone_expr.check_and_give_error(query))

@app.route("/drevesnik/query_info/<ticket>")
def qinf(ticket):
    try:
        inf = open(res_file(ticket + '.json'),'rt')
        rr = inf.read()
        print(rr, "2")
        inf.close()
    except:
        rr = '{}'
    print(rr, "1")
    return rr

@app.route("/drevesnik/kill_query/<ticket>")
def kill_q(ticket):
    return ticket

@app.route("/drevesnik/get_result_count/<ticket>")
def get_res_count(ticket):

    try:
        files = glob.glob(res_file('*' + ticket + '*.conllu'))
        print (files)
        res = {}
        for f in files:
            lang = '_'.join(f.split('/')[-1].split('_')[:-2])
            number = int(f.split('/')[-1].split('_')[-1].split('.')[0])
            if lang not in res.keys():
                res[lang] = 0
            if number > res[lang]:
                res[lang] = number

        better_res = {}
        for k in res:
            ## lang_ticket_number
            inf = open(res_file(str(k) + '_' + ticket + '_' + str(res[k])+".conllu"), 'rt')
            cnt = 0
            for l in inf:
                if '# lang:' in l:
                    cnt += 1
            inf.close()
            better_res[k] = res[k] + cnt

        inf = open(res_file(ticket + '_err'),'rt')
        errors = inf.read()
        inf.close()
        if len(better_res) < 1 and len(errors) > 0: better_res = {'': errors}
    except:
        better_res = {}

    tr = []
    for k in better_res.keys():
        if better_res[k] < 1:
            tr.append(k)
    for k in tr:
        del better_res[k]

    return jsonify(better_res)


@app.route("/drevesnik/is_query_finished/<ticket>")
def gxet_res_count(ticket):
    if os.path.exists(res_file(ticket+'.done')):
        print(True)
        return jsonify(True)
    else:
        print(False)
        return jsonify(False)

@app.route("/drevesnik/get_result_langs/<ticket>")
def get_langs(ticket):

    langs = set()
    try:
        xx = open(res_file(ticket + '.langs'), 'r')
        langs = json.load(xx)
        xx.close()
    except:
        langs = []
    langs = list(langs)    
    langs.sort()
    print (langs)
    return jsonify(list(langs))

@app.route("/drevesnik/get_tree_count/<ticket>/<lang>/")
def get_tree_count(ticket, lang):

    trees = 0

    curr_tree = []
    inf = open(res_file(ticket),'rt')
    for l in inf:
        curr_tree.append(l)
        if l == '\n':
            for c in curr_tree:
                if c.startswith('# lang:') and lang in c:
                    trees += 1
            curr_tree = []

    return json.dumps(trees)

import time
@app.route("/drevesnik/show/<ticket>/<lang>/<start>/<end>", defaults={"site_lang": "sl"})
@app.route("/drevesnik/show/<site_lang>/<ticket>/<lang>/<start>/<end>")
def get_xtrees(ticket, lang, start, end, site_lang):
    global config_folder
    global index_folder

    try:
        start = int(start)
        end = int(end)
    except:
        start = 0
        end = 10

    inf = open(config_folder + 'config.json', 'r')
    xx = json.load(inf)
    inf.close()


    trees = []

    tc = 0
    curr_tree = []
    try:
        inf = open(res_file(ticket+'.json'), 'r')
        inf.close()
    except:
        time.sleep(0.5)

    if lang == 'undefined':
        #
        try:
            inf = open(res_file(ticket+'.json'), 'r')
            db = json.load(inf)
            db = db["dbs"]
            inf.close()
        except:
            return render_template(f'query.html', start=start, end=end, lang=lang, idx=ticket, site_lang=site_lang)

        dbs = get_db_locations()

        for dib in db.split(','):
            inf = open(index_folder + dbs[dib][8:] + '/langs', 'rt')
            xx = []
            for ln in inf:
                xx.append(ln.strip())

            inf.close()
        return render_template(f'query.html', start=start, end=end, lang=xx[0], idx=ticket, site_lang=site_lang)
        #except:
        #    return render_template('query.html', start=0, end=(end-start), lang='unknown', idx=ticket)
  
    return render_template(f'query.html', start=start, end=end, lang=lang, idx=ticket, site_lang=site_lang)           


@app.route("/drevesnik/get_trees/<ticket>/<lang>/<start>/<end>", defaults={"site_lang": "sl"})
@app.route("/drevesnik/get_trees/<site_lang>/<ticket>/<lang>/<int:start>/<int:end>")
def get_trees(site_lang, ticket, lang, start, end):

    trees = []

    tc = 0
    curr_tree = []
    its_on = False

    #lets find a starting point
    files = glob.glob(res_file(lang + '_' + ticket + '*.conllu'))
    files.sort()
    prev = ''
    filelist = []
    for f in files:
        #print (int(f.split('_')[-1].split('.')[0]), start, end, (int(f.split('_')[-1].split('.')[0]) >= int(start)) and (int(f.split('_')[-1].split('.')[0]) <= int(end)))
        if (int(f.split('_')[-1].split('.')[0]) >= int(start)) and (int(f.split('_')[-1].split('.')[0]) < int(end)):
            filelist.append(f)

    for f in filelist:
        inf = open(f,'rt')
        '''
        for l in inf:
            curr_tree.append(l)
            if l == '\n':
                for c in curr_tree:
                    if c.startswith('# lang: ' + lang) or (c.startswith('# lang: ') and lang in c):
                        #if tc > start_tree - start:
                        trees.append(''.join(curr_tree[:]))
                        #if tc > start-end:
                        #    break
                        tc += 1
                curr_tree = []
        '''
        trees.extend(inf.readlines())
        inf.close()

    src = ''.join(trees).split('\n')
    return render_template(f"result_tbl.html",trees=yield_trees(src))


@app.route("/drevesnik/get_page_tree_count/<ticket>/<lang>/<int:start>/<int:end>")
def get_page_tree_count(ticket, lang, start, end):

    trees = []

    tc = 0
    curr_tree = []
    its_on = False

    #lets find a starting point
    files = glob.glob(res_file(lang + '_' + ticket + '*.conllu'))
    files.sort()
    prev = ''
    filelist = []
    for f in files:
        #print (int(f.split('_')[-1].split('.')[0]), start, end, (int(f.split('_')[-1].split('.')[0]) >= int(start)) and (int(f.split('_')[-1].split('.')[0]) <= int(end)))
        if (int(f.split('_')[-1].split('.')[0]) >= int(start)) and (int(f.split('_')[-1].split('.')[0]) < int(end)):
            filelist.append(f)

    for f in filelist:
        inf = open(f,'rt')
        '''
        for l in inf:
            curr_tree.append(l)
            if l == '\n':
                for c in curr_tree:
                    if c.startswith('# lang: ' + lang) or (c.startswith('# lang: ') and lang in c):
                        #if tc > start_tree - start:
                        trees.append(''.join(curr_tree[:]))
                        #if tc > start-end:
                        #    break
                        tc += 1
                curr_tree = []
        '''
        trees.extend(inf.readlines())
        inf.close()

    count = 0
    for l in trees:
        if l.startswith('# hittoken:'): count += 1
    print(count)
    return jsonify(count)


@app.route("/drevesnik/get_err/<ticket>")
def get_err(ticket):

    trees = []

    tc = 0
    curr_tree = []
    inf = open(res_file(ticket+'.err'),'rt')
    err = inf.read()
    inf.close()

    #Syntax error at the token 'ccc' HERE: 'ccc '...

    to_return = ''
    if "Syntax error" in err:
        to_return = err.split('redone_expr.ExpressionError:')[1].split('During')[0]
    return err

@app.route("/drevesnik/tget_trees/<ticket>/<lang>/<int:start>/<int:end>")
def tget_trees(ticket, lang, start, end):

    trees = []

    tc = 0
    curr_tree = []
    inf = open(res_file(ticket),'rt')
    for l in inf:
        curr_tree.append(l)
        if l == '\n':
            
            for c in curr_tree:
                if c.startswith('# lang: ' + lang):
                    if tc <= end and tc >= start:
                        trees.append(''.join(curr_tree[:]))
                    tc += 1
            curr_tree = []
            
    return json.dumps(''.join(trees))


def yield_trees(src):
    current_tree=[]
    current_comment=[]
    current_context=u""
    for line in src[:-1]:
        if line.startswith(u"# visual-style"):
            current_tree.append(line)
        elif line.startswith(u"# URL:"):
            current_comment.append(Markup(u'<a href="{link}">{link}</a>'.format(link=line.split(u":",1)[1].strip())))
        elif line.startswith(u"# context-hit"):
            current_context+=(u' <b>{sent}</b>'.format(sent=escape(line.split(u":",1)[1].strip())))
        elif line.startswith(u"# context"):
            current_context+=(u' {sent}'.format(sent=escape(line.split(u":",1)[1].strip())))
        elif line.startswith(u"# hittoken") or line.startswith(u"# sent_id"):
            current_tree.append(line)
        elif not line.startswith(u"#"):
            current_tree.append(line)
        if line==u"":
            current_comment.append(Markup(current_context))
            yield u"\n".join(current_tree), current_comment
            current_comment=[]
            current_tree=[]
            current_context=u""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--port', type=int, default=5000, help='Port. Default %(default)d.')
    parser.add_argument('--host', default='0.0.0.0', help='Host. Default %(default)s.')
    parser.add_argument('--debug', default=False, action="store_true", help='Flask debug mode')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port,debug=args.debug)
