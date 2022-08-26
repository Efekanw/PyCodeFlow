from lark.visitors import Visitor_Recursive
from queue import Queue
import pygraphviz as pgv
import os
import path_finder
from lark import Lark
from lark.indenter import PythonIndenter

#0-1180
#0 - 700
# , count_if, count_import, count_assign, count_expr, count_with, count_for, count_while

class Visit_Floww(Visitor_Recursive):

    def __init__(self, filename, path, A, node, func_name, count_if, count_import, count_assign, count_expr, count_with, count_for, count_while, count_def, count_class, count_return):
        self.filename = filename
        self.path = path
        self.list_import_path = []
        self.list_import_name = []
        self.count_if = count_if
        self.count_import = count_import
        self.count_assign = count_assign
        self.count_expr = count_expr
        self.count_with = count_with
        self.count_for = count_for
        self.count_while = count_while
        self.count_def = count_def
        self.count_class = count_class
        self.count_return = count_return
        if node != '':
            self.subgraph_def = 1
            self.valid = 0
            self.A = A
            self.node = node
            self.func_name = func_name
            self.subgraph = 1
        else:
            self.subgraph_def = 0
            self.subgraph_class = 0
            self.A = A
            self.valid = 1
            self.subgraph = 0

    new_else = ''
    flag_else = 1
    counter_if = 0
    node_elif = ''
    node_else = ''
    first_subnode = ''
    first_sub = 0
    is_function = 0
    is_def = 0
    is_if = 0
    suite_while = 0
    suite_for = 0
    stack_pos = []
    stack_stmt = []
    ifend = []
    list_import_path = []
    list_import_name = []
    node_elif = ''
    is_importpath = 0
    is_importname = 0
    is_funccall = 0
    last_pop = ''
    list_false = []

    # list_group.append(main_group)
    # dwg.add(main_group)

    column = 0
    depth = 0
    end_pos = 0
    x = 1180 / 2
    y = 50




    def funccall(self, tree):
        if self.subgraph_def == 0:
            self.is_funccall = 1

    def return_counters(self):
        list_counters = {}
        list_counters['if'] = (self.count_if)
        list_counters['def'] = (self.count_def)
        list_counters['for'] = (self.count_for)
        list_counters['import'] = (self.count_import)
        list_counters['expr'] = (self.count_expr)
        list_counters['assign'] = (self.count_assign)
        list_counters['while'] = (self.count_while)
        list_counters['with'] = (self.count_with)
        return list_counters

    def assign_counters(self, list_counters):
        self.count_if = list_counters['if']
        self.count_def = list_counters['def']
        self.count_for = list_counters['for']
        self.count_import = list_counters['import']
        self.count_expr = list_counters['expr']
        self.count_assign = list_counters['assign']
        self.count_while = list_counters['while']
        self.count_with = list_counters['with']

    def name(self, tree):
        print('a')
        # try:
        #     if self.subgraph == 0:
        #         if self.is_importpath == 1:
        #             self.list_import_path.append(tree.children[0])
        #             self.is_importpath = 0
        #         elif self.is_importname == 1:
        #             self.list_import_name.append(tree.children[0])
        #             self.is_importname = 0
        #         elif self.is_funccall == 1:
        #             self.is_funccall = 0
        #             if tree.children[0] in self.list_import_name:
        #                 index = self.list_import_name.index(tree.children[0])
        #                 filename = self.list_import_path[index] + '.py'
        #                 print("path filename --- ")
        #                 print(filename)
        #                 print(os.getcwd())
        #                 path = path_finder.find_path(filename, os.getcwd())
        #                 print(path)
        #                 kwargs = dict(postlex=PythonIndenter(), start='file_input')
        #                 python_parser3 = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser='lalr',
        #                                                         **kwargs, propagate_positions=True)
        #                 file_str = open(path).read()
        #                 print(file_str)
        #                 tree = python_parser3.parse(file_str)
        #                 print(tree.pretty())
        #                 visitor = Visit_Floww(self.list_import_path[index] + '.py', path, self.A, node=self.A.nodes()[-1], func_name=tree.children[0], count_if=self.count_if, count_import=self.count_import, count_assign=self.count_assign, count_expr=self.count_expr, count_with=self.count_with, count_for=self.count_for, count_while=self.count_while, count_def=self.count_def)
        #                 visitor.visit_topdown(tree)
        #                 list_counters = visitor.return_counters()
        #                 self.assign_counters(list_counters)
        # except:
        #     print("name error")

    def get_file_lines(self):
        self.lines = open(self.path).readlines()

    def export_svg(self):
        self.A.draw('file.svg', format("svg"), prog='dot')
        #self.main_group.add(self.list_group[0])

    def file_input(self, tree):
        if self.subgraph_def == 0:
            self.get_file_lines()
            self.A.add_node('Start', shape='ellipse')
            node = self.A.get_node('Start')
            node.attr["class"] = "start"

    def import_stmt(self, tree):
        try:
            if (len(self.stack_pos) < 1) or (self.subgraph_def == 0 and self.subgraph_class == 0 and self.stack_stmt[-1] != 'class' + str(self.count_class) and self.stack_stmt[-1] != 'def' + str(self.count_def)):
                if self.is_if == 0:
                    text = ''
                    for i in range(tree.meta.line - 1, tree.meta.end_line):
                        text += self.lines[i]
                    if tree.meta.line == tree.meta.end_line:
                        text = text.strip()
                    # text = self.lines[tree.meta.line - 1][0:-1].strip()
                    print(text)
                    print('end line --')
                    print(tree.meta.end_line)
                    n = 'import' + str(self.count_import)
                    self.A.add_node(n=n, label=text, shape='ellipse')
                    if self.first_sub == 0:
                        prevnode = self.A.nodes()[-2]
                    else:
                        prevnode = self.first_subnode
                        self.first_sub = 0
                    self.A.add_edge(prevnode, n)
                    self.count_import += 1
        except:
            print("import_stmt error")

    def dotted_name(self, tree):
        self.is_importpath = 1

    def import_as_name(self, tree):
        self.is_importname = 1

    def with_stmt(self, tree):
        self.stmts(tree, 'with')

    def return_stmt(self, tree):
        self.stmts(tree, 'return')

    def funcdef(self, tree):
        try:
            self.count_def += 1
            if self.subgraph == 1 and self.valid == 0:
                self.lines = open(self.path).readlines()
                text = self.lines[tree.meta.line - 1][0:-1].strip()
                text = text.split()[1].split('(')[0]
                if text == self.func_name:
                    self.A.add_node(n=self.func_name, label=text, shape='septagon')
                    node = self.A.get_node(self.func_name)
                    node.attr["class"] = "show_hide"
                    self.A.add_edge(self.node, self.func_name)
                    self.stack_stmt.append('def' + str(self.count_def))
                    self.stack_pos.append(tree.meta.end_pos)
                    print("maingraph")
                    print(self.A.string())
                    self.A = self.A.add_subgraph(name="cluster1", style='filled', color='lightgrey')
                    attributes = {}
                    attributes.update(style='filled',
                                      color='yellow',
                                      label='cluster 2 label')
                    print("subgraph")
                    print(self.A.string())
                    self.first_subnode = self.func_name
                    self.first_sub = 1
                    self.valid = 1
                    self.func_name = ''
            elif self.count_def > 1 or self.subgraph == 0:
                self.valid = 0
                n = 'def' + str(self.count_def)
                self.stack_pos.append(tree.meta.end_pos)
                self.stack_stmt.append('def' + str(self.count_def))
                self.stmt_pop(tree, n)
                # if tree.meta.start_pos >= self.stack_pos[-1]: # if for poplama durumu eklenmeli
                #     self.stack_pos.pop()
                #     stmt = self.stack_stmt.pop()
                #     if stmt == 'def' + str(self.count_def):
                #         self.count_def -= 1
                #


            # elif self.subgraph == 0 or self.valid == 1:
            #     if tree.meta.start_pos >= self.stack_pos[-1]:
            #         self.stack_pos.pop()
            #         self.stack_stmt.pop()
            #     self.stack_pos.append(tree.meta.end_pos)
            #     self.stack_stmt.append('def' + str(self.count_def))
        except:
            print('funcdef error')

    def classdef(self, tree):
        try:
            self.count_class += 1
            if self.subgraph == 1 and self.valid == 0:
                self.lines = open(self.path).readlines()
                text = self.lines[tree.meta.line - 1][0:-1].strip()
                text = text.split()[1].split('(')[0]
                if text == self.func_name:
                    self.A.add_node(n=self.func_name, label=text, shape='septagon')
                    node = self.A.get_node(self.func_name)
                    node.attr["class"] = "show_hide"
                    self.A.add_edge(self.node, self.func_name)
                    self.stack_stmt.append('def' + str(self.count_def))
                    self.stack_pos.append(tree.meta.end_pos)
                    print("maingraph")
                    print(self.A.string())
                    self.A = self.A.add_subgraph(name="cluster1", style='filled', color='lightgrey')
                    attributes = {}
                    attributes.update(style='filled',
                                      color='yellow',
                                      label='cluster 2 label')
                    print("subgraph")
                    print(self.A.string())
                    self.first_subnode = self.func_name
                    self.first_sub = 1
                    self.valid = 1
                    self.func_name = ''
            elif self.count_def > 1 or self.subgraph == 0:
                self.valid = 0
                n = 'class' + str(self.count_class)
                self.stack_pos.append(tree.meta.end_pos)
                self.stack_stmt.append('class' + str(self.count_class))
                self.stmt_pop(tree, n)
                # if tree.meta.start_pos >= self.stack_pos[-1]: # if for poplama durumu eklenmeli
                #     self.stack_pos.pop()
                #     stmt = self.stack_stmt.pop()
                #     if stmt == 'def' + str(self.count_def):
                #         self.count_def -= 1
                #

            # elif self.subgraph == 0 or self.valid == 1:
            #     if tree.meta.start_pos >= self.stack_pos[-1]:
            #         self.stack_pos.pop()
            #         self.stack_stmt.pop()
            #     self.stack_pos.append(tree.meta.end_pos)
            #     self.stack_stmt.append('def' + str(self.count_def))
        except:
            print('class error')

    def stmt_pop(self, tree, n):
        try:
            try:
                index = self.A.nodes().index(n)
            except:
                index = -1
            # if n == '':
            #     index = -1
            # else:
            #     index = self.A.nodes().index(n)
            prevnode = ''
            if self.first_sub == 0:
                prevnode = self.A.nodes()[-2]
            else:
                prevnode = self.first_subnode
                self.first_sub = 0
            # if len(self.stack_pos) > 0 and self.stack_pos[-1] <= tree.meta.start_pos:
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if self.valid == 1:
                while len(self.stack_pos) > 0 and self.stack_pos[-1] <= tree.meta.start_pos:
                    stmt = ''
                    if n.startswith('else'):
                        inden_if = self.stack_stmt[-1].split()[2]
                        if self.stack_stmt[-1].startswith('if'):
                            self.last_pop = 'elifs'
                            break
                        else:
                            self.stack_pos.pop()
                            stmt = self.stack_stmt.pop()
                    else:
                        self.stack_pos.pop()
                        stmt = self.stack_stmt.pop()
                    if stmt == 'class' + str(self.count_class):
                        if self.subgraph == 1 and self.count_class < 1:
                            self.valid = 0
                        self.count_def -= 1
                        self.last_pop = stmt
                    if stmt == 'def' + str(self.count_def):
                        if self.subgraph == 1 and self.count_def < 1:
                            self.valid = 0
                        self.count_def -= 1
                        # if self.count_def > 0:
                        #     self.subgraph = 1
                        # else:
                        #     self.subgraph = 0
                        # self.sub_end = 1
                        self.last_pop = stmt
                        # print(self.A.string())
                        # self.A.add_nodes_from(self.A.nodes(), color='red', style='invis')
                        # self.A.add_edges_from(self.A.edges(), color='blue', style='dashed')
                        # print(self.A.string())
                    # if stmt == 'elifs' + str(self.count_for):
                    #     self.stack_pos.pop()
                    #     stmt = self.stack_stmt.pop()
                    # node_elif = self.node_elif
                    # node_else = ''
                    if stmt == 'for' + str(self.count_for):
                        node = self.A.get_node(stmt)
                        self.A.add_edge(node, n, label='Yes')
                    if stmt == 'else' + str(self.counter_if) + ' ' + str(self.count_if):
                        self.flag_else = 1
                        stmt = self.stack_stmt.pop()
                        self.stack_pos.pop()
                        print("elif true")
                        print(self.A.nodes()[index - 1])
                        self.node_else = self.A.nodes()[index - 1]
                    if stmt == 'elif' + str(self.counter_if) + ' ' + str(self.count_if): # else bağı
                        # self.stack_stmt.pop()
                        # self.stack_pos.pop()
                        print("else true")
                        print(self.A.nodes()[index - 1])
                        self.node_elif = self.A.nodes()[index - 1]
                        index = self.A.nodes().index('elif' + str(self.counter_if))
                        node = self.A.nodes()[index]
                        self.A.add_edge(node, n, label='False')
                    #if stmt == 'if' + str(self.count_if):
                    if stmt.startswith('if'):   ######### eklemeler bu kısıma yapılacak
                        counter = stmt.split()[1]
                        indent = stmt.split()[2]
                        list_if_nodes = [i for i in self.A.nodes() if i.startswith('if')]
                        list_if_indents = [i.split()[2] for i in list_if_nodes]
                        list_elif_nodes = [i for i in self.A.nodes() if i.startswith('elif')]
                        list_elif_indents = [i.split()[2] for i in list_elif_nodes]
                        if ('elif' in list_elif_nodes and str(self.count_if) in list_elif_indents) and self.new_else in self.A.nodes():
                            node1 = self.new_else
                            index = self.A.nodes().index('elif' + str(self.counter_if) + ' ' + str(self.count_if)) - 1
                            node2 = self.A.nodes()[index]
                            self.A.add_edge(node1, n, label='False')
                            self.A.add_edge(node2, n)
                            self.A.add_edge(self.node_elif, n)
                            self.A.add_edge(self.node_else, n)
                        elif ('elif' in list_elif_nodes and str(self.count_if) in list_elif_indents):
                            node1 = 'elif' + str(self.counter_if) + ' ' + str(self.count_if)
                            index = self.A.nodes().index('elif' + str(self.counter_if) + ' ' + str(self.count_if)) - 1
                            node2 = self.A.nodes()[index]
                            self.A.add_edge(node1, n, label='False')
                            self.A.add_edge(node2, n)
                            self.A.add_edge(self.node_elif, n) # count 1 den büyükse her ifden bir false çek if in true su zaten tek geliyor
                        elif self.new_else in self.A.nodes():
                            #node1 = 'else' + str(c_if)
                            index = self.A.nodes().index(self.new_else) - 1
                            node2 = self.A.nodes()[index]
                            #self.A.add_edge(node1, n,) #false
                            self.A.add_edge(node2, n)
                            self.A.add_edge(self.node_else, n)
                        elif ('elif' not in list_elif_nodes and str(self.count_if) not in list_elif_indents)and self.new_else not in self.A.nodes():
                            if len(self.list_false) > 0:
                                self.A.add_edges_from(self.list_false, n, label='False')
                            elif int(indent) > 0:
                                self.list_false.append('if' + counter)
                            else:
                                node1 = 'if' + counter
                                node2 = self.A.nodes()[-2]
                                self.A.add_edge(node1, n, label='False')
                                self.A.add_edge(node2, n)
                        self.count_if -= 1
                        self.new_else = ''
                    # if stmt == 'elifs' + str(self.count_if):
                    #     self.stack_pos.pop()
                    #     stmt = self.stack_stmt.pop()
                    self.last_pop = stmt
                # if self.subgraph == 0 and self.stack_stmt[-1] == 'def' + str(self.count_def) or self.stack_stmt[-1] == 'class' + str(self.count_class):
                #     stmt = self.stack_stmt.pop() # def pop
                #     self.stack_pos.pop()
                #     if stmt == 'def' + str(self.count_def):
                #         self.count_def -= 1
                #     elif stmt == 'class' + str(self.count_class):
                #         self.count_class -= 1
                #     self.valid = 0
                #if self.last_pop != 'elifs' + str(self.counter_if) + ' ' + str(self.count_if):
                if not self.last_pop.startswith('elifs'):
                    if 'else' + str(self.counter_if) + ' ' + str(self.count_if) in self.stack_stmt and self.flag_else == 1:
                        index = self.A.nodes().index('if' + str(self.counter_if))
                        node = self.A.nodes()[index]
                        self.A.add_edge(node, n, label='False')
                        self.new_else = n
                        self.flag_else = 0
                    elif len(self.stack_pos) > 0 and self.stack_pos[-1] > tree.meta.start_pos and (
                            self.A.nodes()[index - 1].startswith('if') or self.A.nodes()[index - 1].startswith('elif') or
                            self.A.nodes()[index - 1].startswith('else')):
                        self.A.add_edge(prevnode, n, label='True') # else in true göstergesi if ile kaldırılabilir
                    elif len(self.stack_pos) > 0 and self.stack_pos[-1] > tree.meta.start_pos and (
                            self.A.nodes()[index - 1] == 'for' + str(self.count_for)):
                        self.A.add_edge(prevnode, n, label='No')
                        self.A.add_edge(n, prevnode, label='Try Next Item')
                    elif self.last_pop != 'elif' + str(self.counter_if):
                            self.A.add_edge(prevnode, n)
                else:
                    self.last_pop = ''
        except:
            print('stmt error')

    def stmts(self, tree, stmt_type):
        try: # func kontrolü
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if self.valid == 1: #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                text = ''
                for i in range(tree.meta.line - 1, tree.meta.end_line):
                    text += self.lines[i]
                if tree.meta.line == tree.meta.end_line:
                    text = text.strip()
                n = ''
                #if len(self.stack_pos) < 1 or ('def' + str(self.count_def) not in self.stack_stmt or self.stack_pos[-1] > tree.meta.start_pos):
                if stmt_type == 'assign':
                    n = stmt_type + str(self.count_assign)
                    self.count_assign += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                elif stmt_type == 'expr':
                    n = stmt_type + str(self.count_expr)
                    self.count_expr += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                elif stmt_type == 'with':
                    n = stmt_type + str(self.count_with)
                    self.count_with += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                elif stmt_type == 'for':
                    text = self.lines[tree.meta.line - 1][0:-1].strip()
                    text = text[4:-1]
                    n = stmt_type + str(self.count_for)
                    self.A.add_node(n=n, label=text, shape='hexagon')
                elif stmt_type == 'return':
                    n = stmt_type + str(self.count_return)
                    self.count_return += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                self.stmt_pop(tree, n)
        except:
            print("stmts error")

    def assign_stmt(self, tree):
            self.stmts(tree, 'assign')

    def expr_stmt(self, tree):
            self.stmts(tree, 'expr')

    def elifs(self, tree):
        try:
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if self.valid == 1: #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                # stmt_pop çağır elifs poplansın counter if ona göre düşecek
                self.stmt_pop(tree, 'elifs' + str(self.counter_if) + ' ' + str(self.count_if))
                self.stack_pos.append(1)
                self.stack_stmt.append('elifs' + str(self.counter_if) + ' ' + str(self.count_if))
                print("--elif pos--")
        except:
            print("elifs error")


    def suite(self, tree):
        try:
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if (self.valid == 1 and 'elif' + str(self.counter_if) + ' ' + str(self.count_if) in self.stack_stmt) or (self.valid == 1 and self.stack_stmt[-1] == 'elifs' + str(self.counter_if) + ' ' + str(self.count_if)): #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                if 'elif' + str(self.counter_if) + ' ' + str(self.count_if) in self.stack_stmt:
                    index = self.stack_stmt.index('elif' + str(self.counter_if) + ' ' + str(self.count_if))
                elif 'elifs' + str(self.counter_if) + ' ' + str(self.count_if) in self.stack_stmt:
                    index = self.stack_stmt.index('elifs' + str(self.counter_if) + ' ' + str(self.count_if))
                if self.stack_pos[index] <= tree.meta.start_pos:
                    n = 'else' + str(self.counter_if) + ' ' + str(self.count_if)
                    text = self.lines[tree.meta.line - 1][0:-1].strip()
                    #self.A.add_node(n=n, label=text, shape='diamond')
                    self.stmt_pop(tree, n)
                    self.stack_stmt.append('else' + str(self.counter_if) + ' ' + str(self.count_if))
                    self.stack_pos.append(tree.meta.end_pos)

                # if 'elif' + str(self.count_if) in self.stack_stmt:
                #     index = self.stack_stmt.index('elif' + str(self.count_if))
                #     end_pos = self.stack_pos[index]
                #     if end_pos <= tree.meta.start_pos:

                        # text = self.lines[tree.meta.line - 1][0:-1].strip()
                        # n = 'else' + str(self.count_if)
                        # self.A.add_node(n=n, label=text, shape='diamond')
                        # node = self.A.get_node('elif' + str(self.count_if))
                        # self.A.add_edge(node, n, label='False')
                        # index = self.A.nodes().index(n)
                        # self.node_elif = self.A.nodes()[index - 1]
                # if len(self.stack_pos) > 0 and (self.stack_pos[-1] < tree.meta.start_pos and (self.stack_stmt[-1] == 'for' + str(self.count_for) or self.stack_stmt[-1] == 'while' + str(self.count_while))):
                #     self.stack_pos.pop()
                #     stmt = self.stack_stmt.pop()
                #     if stmt == 'for':
                #         self.suite_for = 1
                #     elif stmt == 'while':
                #         self.suite_while = 1
                    #if stmt == 'for' + str(for)
                # elif len(self.stack_pos) > 0 and (self.stack_stmt[-1] == 'elifs' + str(self.count_if)):
                #     self.stack_pos.pop()
                #     stmt = self.stack_stmt.pop()
                #     self.stack_stmt.append('else' + str(self.count_if))
                #     self.stack_pos.append(tree.meta.end_pos)
                #     text = self.lines[tree.meta.line - 1][0:-1].strip()
                #     n = 'else' + str(self.count_if)
                #     self.A.add_node(n=n, label=text, shape='diamond')
                #     node = self.A.get_node('if' + str(self.count_if))
                #     self.A.add_edge(node, n, label='False')
        except:
            print("suite error")

    def elif_(self, tree):
        try:
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if self.valid == 1: #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                text = self.lines[tree.meta.line - 1][0:-1].strip()
                print(text)
                n = 'elif ' + str(self.counter_if) + ' ' + str(self.count_if)
                self.A.add_node(n=n, label=text, shape='diamond')
                self.stmt_pop(tree, n)
                self.stack_pos.append(tree.meta.end_pos)
                self.stack_stmt.append('elif'+str(self.counter_if) + ' ' + str(self.count_if))

                # n = 'elif' + str(self.count_if)
                # self.A.add_node(n=n, label=text, shape='diamond')
                # node = self.A.get_node('if'+str(self.count_if))
                # self.A.add_edge(node, n, label='False')
        except:
            print("elif_ error")

    def if_stmt(self, tree): # eğer poplanan funcdef ise ve func sayısı 1 ise if işlemi yapılacak
        try:
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if self.valid == 1: #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                text = self.lines[tree.meta.line - 1][0:-1].strip()
                text = text[3:-1]
                n = 'if ' + str(self.counter_if + 1) + ' ' + str(self.count_if)
                self.counter_if += 1
                self.A.add_node(n=n, label=text, shape='diamond')
                self.stmt_pop(tree, n)
                self.count_if += 1
                self.stack_stmt.append(n)
                self.stack_pos.append(tree.meta.end_pos)
                # if self.first_sub == 0:
                #     prevnode = self.A.nodes()[-2]
                # else:
                #     prevnode = self.first_subnode
                #     self.first_sub = 0
                # if self.count_if > 1:
                #     self.A.add_edge(prevnode, n, label='True')
                # else:
                #     self.A.add_edge(prevnode, n)
                self.is_if = 1
        except:
            print("if error")

    def for_stmt(self, tree):
        try:
            while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0): # if ve diğer nodelara eklenemli
                if tree.meta.start_pos >= self.stack_pos[-1]:
                    self.stack_pos.pop()
                    stmt = self.stack_stmt.pop()
                    if stmt == 'def' + str(self.count_def):
                        self.count_def -= 1
                        if self.count_def == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_def == 0 and self.subgraph == 0:
                            self.valid = 1
                    if stmt == 'class' + str(self.count_class):
                        self.count_class -= 1
                        if self.count_class == 1 and self.subgraph == 1:
                            self.valid = 1
                        elif self.count_class == 0 and self.subgraph == 0:
                            self.valid = 1
                else:
                    break
            if self.valid == 1: #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                self.count_for += 1
                # if len(self.stack_pos) == 0 or self.stack_pos[-1] > tree.meta.start_pos:
                #     self.stack_pos.append(tree.meta.end_pos)
                #     self.stack_stmt.append('for' + str(self.count_for))
                # elif len(self.stack_pos) > 0 and (self.stack_pos[-1] <= tree.meta.start_pos):
                #     self.stack_pos.pop()
                #     stmt = self.stack_stmt.pop()
                #     if stmt == 'elifs' + str(self.count_if):
                #         self.stack_pos.pop()
                #         stmt = self.stack_stmt.pop()
                #     if stmt == 'if' + str(self.count_if):
                #         self.count_if -= 1
                #     elif stmt == 'for' + str(self.count_for):
                #         self.count_for -= 1
                #     self.stack_pos.append(tree.meta.end_pos)
                #     self.stack_stmt.append('for' + str(self.count_for))
                self.stmts(tree, 'for')
        except:
            print("for stmt error")

