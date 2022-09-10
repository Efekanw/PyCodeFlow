from lark import Lark
from lark.indenter import PythonIndenter
from website import create_app
from flask import render_template, Markup, request, flash
from werkzeug.utils import secure_filename
from Visit_Flow import Visit_Floww
import os
import zipfile
import pygraphviz as pgv
import path_finder
import shutil

def create_svg(filename):
    path = path_finder.find_path(filename, os.getcwd() + '/tmp')
    kwargs = dict(postlex=PythonIndenter(), start='file_input')
    python_parser3 = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser='lalr', **kwargs,
                                            propagate_positions=True)
    file_str = open(path).read()
    print(file_str)
    tree = python_parser3.parse(file_str)
    print(tree.pretty())
    A = pgv.AGraph(directed=True, strict=True, bgcolor="lightblue")
    visitor = Visit_Floww(filename, path, A, node='', func_name='', counter_if=0, count_for=0, count_expr=0, count_with=0,
                          count_while=0, count_assign=0, count_import=0, count_def=0, count_class=0, count_return=0,
                          count_break=0, count_continue=0, count_try=0, count_if=0, count_sub=0,clickfile_name='')
    visitor.visit_topdown(tree)
    visitor.export_svg()


app = create_app()

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = ['zip', 'rar']


def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try:
        lst = os.listdir(path)
    except OSError:
        pass  # ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


def allowed_file(filename):
    if filename.lower().endswith(('.zip')) or filename.lower().endswith(('.rar')):
        return True
    else:
        flash('Unvalid file type')
        return False


def custom_dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

@app.route('/', methods=['GET', 'POST'])
def hello():
    return app.response_class(render_template('home.html'))



@app.route('/upload-file', methods=['POST'])
def upload_file():
    path = ''
    filename = 'None'
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mycwd = os.getcwd()
            newcwd = mycwd + '/tmp'
            file.save(os.path.join(newcwd, filename))
            os.chdir(newcwd)
            newcwd += '/files'
            with zipfile.ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(newcwd)
            os.chdir(mycwd)
            path = newcwd
    except Exception as e:
        print(str(e))
    return render_template('file_tree.html', tree=make_tree(path))

@app.route('/show-svg', methods=['POST'])
def show_svg():
    filename = 'None'
    lines = ''
    try:
        filename = str(request.form.get('filename'))
        print("label name --- ")
        print(filename)
    except:
        print('no filename')
    if filename != 'None':
        print(filename)
        create_svg(filename)
        svg = open('file.svg')
        for line in svg.readlines()[6:]:
            lines += line
    return app.response_class(render_template('show_svg.html', svg=Markup(lines)))



if __name__ == "__main__":
    mycwd = os.getcwd()
    newcwd = mycwd + '/tmp'
    shutil.rmtree(newcwd)
    os.mkdir(newcwd)
    app.run(debug=True)

