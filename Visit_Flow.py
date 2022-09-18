from lark.visitors import Visitor_Recursive
import os
import path_finder
from lark import Lark
from lark.indenter import PythonIndenter


class Visit_Floww(Visitor_Recursive):

    def __init__(self, filename, path, A, node, func_name, counter_if, count_import, count_assign, count_expr, count_with, count_for, count_while, count_def, count_class, count_return, count_break, count_continue,count_try,count_if,count_sub, clickfile_name):
        self.filename = filename
        self.path = path
        self.list_import_path = []
        self.list_import_name = []
        self.counter_if = counter_if
        self.count_import = count_import
        self.count_assign = count_assign
        self.count_expr = count_expr
        self.count_with = count_with
        self.count_for = count_for
        self.count_while = count_while
        self.count_class = count_class
        self.count_return = count_return
        self.count_break = count_break
        self.count_continue = count_continue
        self.count_try = count_try
        self.count_sub = count_sub
        self.clickfile_name = clickfile_name
        if node != '':
            self.subgraph_def = 1
            self.valid = 0
            index = -1
            node_l = A.nodes()[index]
            for i in range(0, len(A.nodes())):
                if node_l.startswith('end'):
                    node_l = A.nodes()[index - i]
                else:
                    break
            self.last_main_node = node_l
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
        self.new_else = ''
        self.flag_else = 1
        self.node_elif = ''
        self.node_else = ''
        self.first_subnode = ''
        self.first_sub = 0
        self.is_function = 0
        self.is_def = 0
        self.is_if = 0
        self.is_loop = 0
        self.suite_while = 0
        self.suite_for = 0
        self.stack_pos = []
        self.stack_stmt = []
        self.ifend = []
        self.list_import_path = []
        self.list_import_name = []
        self.node_elif = ''
        self.is_importpath = 0
        self.is_importname = 0
        self.is_funccall = 0
        self.last_pop = ''
        self.dict_false = {}
        self.dict_true = {}
        self.dict_break = {}
        self.dict_continue = {}
        self.dict_false = {}
        self.dict_else_nodes = {}
        self.elif_false = ''
        self.index_dict_false = -1
        self.count_pop_for = 0
        self.list_last_pop = []
        self.last_node_loop = ''
        self.count_pop = 0
        self.list_control = []
        self.break_contine = 1
        self.counter_loop = 0
        self.column = 0
        self.depth = 0
        self.end_pos = 0
        self.x = 1180 / 2
        self.y = 50
        self.last_pos = 0
        self.is_sub = 0
        self.count_graph_def = 0
        self.pop_def = 0
        self.count_def = 0
        self.count_indent = 0

    def get_file_lines(self):
        self.lines = open(self.path).readlines()

    def export_svg(self):
        self.A.draw('file.svg', format("svg"), prog='dot')

    def subnodes(self):
        print(len(self.A.nodes()))
        return len(self.A.nodes())

    def return_counters(self):
        list_counters = {}
        list_counters['if'] = (self.counter_if)
        list_counters['for'] = (self.count_for)
        list_counters['import'] = (self.count_import)
        list_counters['expr'] = (self.count_expr)
        list_counters['assign'] = (self.count_assign)
        list_counters['while'] = (self.count_while)
        list_counters['with'] = (self.count_with)
        list_counters['class'] = self.count_class
        list_counters['return'] = self.count_return
        list_counters['break'] = self.count_break
        list_counters['continue'] = self.count_continue
        list_counters['try'] = self.count_try
        list_counters['sub']= self.count_sub
        return list_counters

    def assign_counters(self, list_counters):
        self.counter_if = list_counters['if']
        self.count_for = list_counters['for']
        self.count_import = list_counters['import']
        self.count_expr = list_counters['expr']
        self.count_assign = list_counters['assign']
        self.count_while = list_counters['while']
        self.count_with = list_counters['with']
        self.count_class = list_counters['class']
        self.count_return = list_counters['return']
        self.count_break = list_counters['break']
        self.count_continue = list_counters['continue']
        self.count_try = list_counters['try']
        self.count_sub = list_counters['sub']

    def funccall(self, tree):
        current_indent = ((int(tree.meta.column) - 1) / 4)
        if self.subgraph_def == 0 or (len(self.stack_stmt) > 0 and (self.subgraph == 1 and int(current_indent) > int(self.stack_stmt[-1].split()[2]))):
            self.is_funccall = 1

    def name(self, tree):
        try:
            current_indent = ((int(tree.meta.column) - 1)/ 4)
            if self.subgraph == 0 or (len(self.stack_stmt) > 0 and (self.subgraph == 1 and int(current_indent) > int(self.stack_stmt[-1].split()[2]))) or self.is_importpath == 1 or self.is_importname == 1:
                if self.is_importpath == 1:
                    self.list_import_path.append(tree.children[0])
                    self.is_importpath = 0
                elif self.is_importname == 1:
                    self.list_import_name.append(tree.children[0])
                    self.is_importname = 0
                elif self.is_funccall == 1:
                    self.is_funccall = 0
                    if tree.children[0] in self.list_import_name:
                        index = self.list_import_name.index(tree.children[0])
                        filename = self.list_import_path[index] + '.py'
                        func_name = tree.children[0]
                        path = path_finder.find_path(filename, os.getcwd() + '/tmp')
                        kwargs = dict(postlex=PythonIndenter(), start='file_input')
                        python_parser3 = Lark.open_from_package('lark', 'python.lark', ['grammars'], parser='lalr',
                                                                **kwargs, propagate_positions=True)
                        file_str = open(path).read()
                        tree = python_parser3.parse(file_str)
                        index = -1
                        node = self.A.nodes()[index]
                        for i in range(0, len(self.A.nodes())):
                            if node.startswith('end'):
                                node = self.A.nodes()[index - i]
                            else:
                                break
                        visitor = Visit_Floww(self.list_import_path[index] + '.py', path, self.A, node=node, func_name=func_name, counter_if=self.counter_if, count_import=self.count_import, count_assign=self.count_assign, count_expr=self.count_expr, count_with=self.count_with, count_for=self.count_for, count_while=self.count_while, count_def=self.count_def, count_class=self.count_class, count_try=self.count_try, count_continue=self.count_continue, count_break=self.count_break, count_return=self.count_return, count_if=self.count_indent, count_sub=self.count_sub, clickfile_name=filename)
                        visitor.visit_topdown(tree)
                        list_counters = visitor.return_counters()
                        self.assign_counters(list_counters)
                        self.A.edges()[-1].attr["class"] = 'invis-edge invis-edge_' + str(self.count_sub)
                        self.count_sub += 1
                        print('subgraph node size')
        except:
            print("name error")

    def file_input(self, tree):
        if self.subgraph_def == 0:
            self.get_file_lines()
            self.A.add_node('Start', shape='ellipse')
            node = self.A.get_node('Start')
            node.attr["class"] = "start"
        else:
            self.get_file_lines()

    def import_stmt(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                if self.is_if == 0:
                    text = ''
                    for i in range(tree.meta.line - 1, tree.meta.end_line):
                        text += self.lines[i]
                    if tree.meta.line == tree.meta.end_line:
                        text = text.strip()
                    n = 'import' + str(self.count_import)
                    self.A.add_node(n=n, label=text, shape='rect')
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
                    self.count_sub += 1
                    self.A = self.A.add_subgraph(name="cluster_"+str(self.count_sub))
                    attributes = {}
                    attributes.update(style='invis',
                                      color='yellow',
                                      label='cluster 2 label')
                    self.A.add_node(n=self.func_name, label=text, shape='septagon')
                    self.A.add_edge(self.node, self.func_name)
                    self.stack_stmt.append('def ' + str(self.count_def) + ' ' + str(self.count_indent))
                    self.stack_pos.append(tree.meta.end_pos)
                    self.A.add_edge(self.last_main_node, self.func_name)
                    func_node = self.A.get_node(self.last_main_node)
                    self.first_subnode = self.func_name
                    self.first_sub = 1
                    self.valid = 1
                    self.func_name = ''
                else:
                    self.count_def -= 1
            elif self.count_def > 1 or self.subgraph == 0:
                self.valid = 0
                n = 'def ' + str(self.count_def) + ' ' + str(self.count_indent)
                if self.count_def > 1 and self.subgraph == 1:
                    self.A.add_node(n=n, label=n, shape='septagon')
                if self.subgraph == 0:
                    self.stack_pos.append(tree.meta.end_pos)
                    self.stack_stmt.append('def ' + str(self.count_def) + ' ' + str(self.count_indent))
                else:
                    self.stmt_pop(tree, n)
                    if self.pop_def == 0:
                        self.stack_pos.append(tree.meta.end_pos)
                        self.stack_stmt.append('def ' + str(self.count_def) + ' ' + str(self.count_indent))
                    else:
                        self.valid = 0
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
                    self.stack_stmt.append('class ' + str(self.count_def) + ' ' + str(self.count_indent))
                    self.stack_pos.append(tree.meta.end_pos)
                    self.A = self.A.add_subgraph(name="cluster1", style='filled', color='lightgrey')
                    attributes = {}
                    attributes.update(style='filled',
                                      color='yellow',
                                      label='cluster 2 label')
                    self.first_subnode = self.func_name
                    self.first_sub = 1
                    self.valid = 1
                    self.func_name = ''
            elif self.count_def > 1 or self.subgraph == 0:
                self.valid = 0
                n = 'class ' + str(self.count_class) + ' ' + str(self.count_indent)
                self.stack_pos.append(tree.meta.end_pos)
                self.stack_stmt.append('class ' + str(self.count_class) + ' ' + str(self.count_indent))
                self.stmt_pop(tree, n)
        except:
            print('class error')

    def try_stmt(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                self.stmts(tree, 'try')
        except:
            print("try error")

    def except_clause(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                self.stmts(tree, 'except')
        except:
            print("except error")

    def stmt_pop(self, tree, n):
        try:
            try:
                self.count_pop_for = 0
                index = self.A.nodes().index(n)
            except:
                index = -1
            prevnode = ''
            valid_prev = 1
            sub_in_sub = 0
            if self.first_sub == 0:
                prevnode = self.A.nodes()[-2]
                for subgraph in self.A.subgraphs():
                    if prevnode in subgraph.nodes():
                        subgraph_node_len = len(subgraph.nodes())
                        prevnode = self.A.nodes()[-2 - subgraph_node_len]

                if prevnode.startswith('end_for') or prevnode.startswith('end_while'):
                    i = -1
                    if prevnode.startswith('end_'):
                        prevnode = self.A.nodes()[i - 1 - 1]
                    else:
                        while not self.A.nodes()[i].startswith('for') and not self.A.nodes()[i].startswith('while'):
                            i -= 1
                            prevnode = self.A.nodes()[i]

                            valid_prev = 0
            else:
                prevnode = self.first_subnode
                self.first_sub = 0
            if ((len(self.stack_pos) > 0 and (True if t.startswith('def') else False for t in self.stack_stmt ) and n.startswith('def') and self.stack_pos[-1] <= tree.meta.start_pos)):
                self.valid = 1
                self.pop_def = 1
            else:
                while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0):
                    if tree.meta.start_pos >= self.stack_pos[-1]:
                        stmt = self.stack_stmt.pop()
                        if stmt.startswith('def'):
                            self.count_def -= 1
                            if self.subgraph == 1:
                                self.valid = 0
                            if self.subgraph == 0:
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
                stmt = ''
                if n.startswith('elifs'):
                    if self.stack_stmt[-1] == n:
                        self.stack_stmt.pop()
                        self.stack_pos.pop()
                else:
                    while len(self.stack_pos) > 0 and self.stack_pos[-1] <= tree.meta.start_pos:
                        stmt = ''
                        elif_indent = 0
                        self.last_pos = self.stack_pos.pop()
                        stmt = self.stack_stmt.pop()

                        if stmt == 'class ' + str(self.count_class) + ' ' + str(self.count_indent):
                            if self.subgraph == 1 and self.count_class < 1:
                                self.valid = 0
                            self.count_def -= 1
                            self.last_pop = stmt
                        if stmt.startswith('def'):
                            if self.subgraph == 1 and self.count_def < 2:
                                self.valid = 0
                            self.count_def -= 1
                            if len(self.A.subgraphs()) > 0:
                                sub_in_sub = 1
                                self.A.add_edge(self.A.nodes()[-2], n)
                            else:
                                sub_in_sub = 0
                            func_node = self.A.get_node(self.last_main_node)
                            if len(self.A.subgraphs()) > 0:
                                for sub in self.A.subgraphs():
                                    if func_node not in sub.nodes() and sub != self.A:
                                        func_node.attr["class"] = "clickable " + str(self.count_sub) + " " + self.clickfile_name
                            else:
                                func_node.attr["class"] = "clickable " + str(self.count_sub) + " " + self.clickfile_name
                            for node in self.A.nodes():
                                if node.attr["class"]:
                                    if node != func_node:
                                        node.attr["class"] += " invis-node_" + str(self.count_sub)
                                else:
                                    node.attr["class"] = "invis-node invis-node_" + str(self.count_sub)
                            for edge in self.A.edges():
                                if edge.attr["class"]:
                                    edge.attr["class"] += " invis-edge_" + str(self.count_sub)
                                else:
                                    edge.attr["class"] = "invis-edge invis-edge_" + str(self.count_sub)
                            self.last_pop = stmt
                            node = self.A.nodes()[-1]
                            node.attr["label"] = "END"
                            node.attr["shape"] = 'oval'
                        if stmt.startswith('except'):
                            self.A.add_edge(n, stmt, label='Yes')
                            index = self.A.nodes().index(stmt) - 2
                            self.subgraph_node_size = 0
                            i = 0
                            node = self.A.nodes()[index]
                            subgraph_node_len = 0
                            for subgraph in self.A.subgraphs():
                                if node in subgraph.nodes():
                                    subgraph_node_len = len(subgraph.nodes())
                                    node = self.A.nodes()[-2 - subgraph_node_len]
                            while node.startswith('end_for') or node.startswith('end_while'):
                                node = self.A.nodes()[-2 - subgraph_node_len - i]
                                i -= 1
                            self.A.add_edge(node,n)
                        if stmt.startswith('while'):
                            indent, node_f = self.loop_pop(n, stmt, tree, 'end_while ', 'False')
                        if stmt.startswith('for'):
                            indent, node_f = self.loop_pop(n, stmt, tree, 'end_for ', 'No')
                        if stmt.startswith('else'):
                            self.flag_else = 0
                            indent = stmt.split()[2]
                            if n.startswith('elif_') or n.startswith('else'):
                                if (len(self.dict_continue) > 0 and self.dict_continue[self.last_pop] !=  self.new_else) and  (len(self.dict_break) > 0 and self.dict_break[self.last_pop] !=  self.new_else):### yeni
                                    self.new_else = self.A.nodes()[-2]
                                    subgraph_node_len = 0
                                    for subgraph in self.A.subgraphs():
                                        if self.new_else in subgraph.nodes():
                                            subgraph_node_len = len(subgraph.nodes())
                                            self.new_else = self.A.nodes()[-2 - subgraph_node_len]
                                    if str(int(indent)-1) not in self.dict_true.keys():
                                        self.dict_true[str(int(indent)-1)] = []
                                    self.dict_true[str(int(indent)-1)].append(self.new_else)
                                    elif_indent = str(int(indent)-1)
                            indent_for, node_for = self.find_loop_node()
                            if node_for.startswith('for') or node_for.startswith('while'):
                                self.new_else = self.dict_else_nodes[str(int(indent))]
                                index = self.A.nodes().index(self.new_else) - 1
                                node = self.A.nodes()[index]
                                subgraph_node_len = 0
                                for subgraph in self.A.subgraphs():
                                    if node in subgraph.nodes():
                                        subgraph_node_len = len(subgraph.nodes())
                                        node = self.A.nodes()[index - subgraph_node_len +1]
                                if indent not in self.dict_true.keys():
                                    self.dict_true[indent] = []
                                self.dict_true[indent].append(node)
                                elif_indent = indent
                            else:
                                self.new_else =self.dict_else_nodes[str(int(indent))]
                                if self.last_pop.startswith('while') or self.last_pop.startswith('for'):
                                    index = self.A.nodes().index(self.new_else) - self.count_pop -1
                                else:
                                    index = self.A.nodes().index(self.new_else) - 1
                                node = self.A.nodes()[index]
                                node_next = self.A.nodes()[index+1]
                                subgraph_node_len = 0
                                for subgraph in self.A.subgraphs():
                                    if node in subgraph.nodes():
                                        subgraph_node_len = len(subgraph.nodes())
                                        node = self.A.nodes()[index - (subgraph_node_len-1)]
                                if not node_next.startswith('end'):
                                    if indent not in self.dict_true.keys():
                                        self.dict_true[indent] = []
                                    self.dict_true[indent].append(node)
                                elif_indent = indent
                            self.last_pop = stmt
                        if stmt.startswith('elif_'):
                            indent = stmt.split()[2]
                            self.index_dict_false = self.dict_false[indent].index(stmt)
                            list_nodes = self.dict_false[indent][0:-1]
                            for node in list_nodes:
                                if node.split()[2] == indent:
                                    node_false = node
                                    break
                            self.dict_false[indent].remove(node_false)
                            self.A.add_edge(node_false, stmt, label='False')
                            index = self.A.nodes().index(stmt) -1
                            node = self.A.nodes()[index]
                            node_next = self.A.nodes()[index+2]
                            subgraph_node_len = 0
                            for subgraph in self.A.subgraphs():
                                if node in subgraph.nodes():
                                    subgraph_node_len = len(subgraph.nodes())
                                    print(self.A.nodes())
                                    node = self.A.nodes()[index - subgraph_node_len + 1]
                            if (n.startswith('elif_') or n.startswith('else')):
                                self.index_dict_false = self.dict_false[indent].index(stmt)
                                n_indent = n.split()[2]
                                if not node_next.startswith('end'):
                                    if indent == n_indent:
                                        elif_indent = indent
                                        if elif_indent not in self.dict_true.keys():
                                            self.dict_true[elif_indent] = []
                                        self.dict_true[elif_indent].append(node)
                                    else:
                                        if str(int(indent) - 1) not in self.dict_true.keys():
                                            self.dict_true[str(int(indent) - 1)] = []
                                        self.dict_true[str(int(indent) - 1)].append(node)
                                        elif_indent = str(int(indent) - 1)
                            elif not node_next.startswith('end'):
                                self.index_dict_false = -1
                                if indent not in self.dict_true.keys():
                                    self.dict_true[indent] = []
                                self.dict_true[indent].append(node)
                            self.last_pop = stmt
                        if stmt.startswith('if'):
                            counter = stmt.split()[1]
                            indent = stmt.split()[2]
                            indent_for, node_for = self.find_loop_node()
                            if n.startswith('else') or n.startswith('elif_'):
                                if not node_for.startswith('for') and not node_for.startswith('while'):
                                    if indent in self.dict_false.keys():
                                        list_false = self.dict_false[indent]
                                        self.index_dict_false = len(list_false) - 1
                                        if str(int(indent) - 1) not in self.dict_false.keys():
                                            self.dict_false[str(int(indent) - 1)] = []
                                        for i in list_false:
                                            self.dict_false[str(int(indent)-1)].append(i)
                                        self.dict_false[indent].clear()
                                    if indent in self.dict_true.keys():
                                        list_true = self.dict_true[str(indent)]
                                        if str(int(indent) - 1) not in self.dict_true.keys():
                                            self.dict_true[str(int(indent) - 1)] = []
                                        for i in list_true:
                                            self.dict_true[str(int(indent)-1)].append(i)
                                        self.dict_true[indent].clear()
                            else:
                                if node_for.startswith('for') or node_for.startswith('while'):
                                    try:
                                        indent_node = n.split()[2]
                                    except:
                                        indent_node = (int(tree.meta.column) - 1) / 4
                                    print(tree.meta.end_column)
                                    if int(indent_node) == int(indent):
                                        if indent in self.dict_false.keys():
                                            for node in self.dict_false[indent]:
                                                self.A.add_edge(node, n, label='False')
                                            self.dict_false[indent].clear()
                                        if indent in self.dict_true.keys():
                                            for node in self.dict_true[indent]:
                                                self.A.add_edge(node, n)
                                            self.dict_true[indent].clear()
                                    else:
                                        if indent in self.dict_false.keys():
                                            for node in self.dict_false[indent]:
                                                self.A.add_edge(node, node_for, label='False')
                                            self.dict_false[indent].clear()
                                        if indent in self.dict_true.keys():
                                            for node in self.dict_true[indent]:
                                                self.A.add_edge(node, node_for)
                                            self.dict_true[indent].clear()
                                else:
                                    if indent in self.dict_false.keys():
                                        for node in self.dict_false[indent]:
                                            self.A.add_edge(node, n, label='False')
                                        self.dict_false[indent].clear()
                                    if indent in self.dict_true.keys():
                                        for node in self.dict_true[indent]:
                                            self.A.add_edge(node, n)
                                        self.dict_true[indent].clear()
                            self.count_indent -= 1
                            self.new_else = ''
                        self.last_pop = stmt

                if not n.startswith('elifs') and sub_in_sub == 0:
                    index = -1
                    node = self.A.nodes()[index - 1 - self.count_pop]
                    subgraph_node_len = 0
                    for subgraph in self.A.subgraphs():
                        if node in subgraph.nodes():
                            self.is_sub = 1
                            subgraph_node_len = len(subgraph.nodes())
                            node = self.A.nodes()[index - subgraph_node_len]
                        if node.startswith('end'):
                            if node.startswith('end'):
                                index = self.A.nodes().index(node) - 1
                                node = self.A.nodes()[index]
                                for i in range(0, len(self.A.nodes())):
                                    if node.startswith('end'):
                                        node = self.A.nodes()[index - i]
                                    else:
                                        break
                    node_for = ''
                    node_indent = -1
                    i = -1
                    c = 0
                    if len(self.stack_stmt) > 0:
                        node_for = self.stack_stmt[i]
                        node_indent = node_for.split()[2]
                        if node_for.startswith('while') or node_for.startswith('for') or node_for.startswith('if'):
                            node_indent = node_for.split()[2]
                        else:
                            node_indent= -1
                        while len(self.stack_stmt) > c and (
                                not self.stack_stmt[i].startswith('for') and not self.stack_stmt[i].startswith(
                                'while')):
                            i -= 1
                            c += 1
                            try:
                                node_for = self.stack_stmt[i]
                                node_indent = node_for.split()[2]
                            except:
                                node_indent = -1
                                print('invalid')
                    if len(self.stack_stmt) > 0 and self.stack_stmt[-1].startswith('else') and self.flag_else == 1:
                        self.flag_else = 0
                        node = self.stack_stmt[-1]
                        indent = node.split()[2]
                        node_false = self.dict_false[indent][self.index_dict_false]
                        self.dict_false[indent].remove(node_false)
                        self.A.add_edge(node_false, n, label='False')
                        self.last_pop = ''
                        self.new_else = n
                        self.dict_else_nodes[str(self.count_indent - 1)] = self.new_else
                        self.index_dict_false = -1
                    elif not n.startswith('break') and not n.startswith('continue'):
                        cur_indent = (int(tree.meta.column) - 1) / 4
                        if node.startswith('if') or node.startswith('elif_') or node.startswith('else'):
                            indent = node.split()[2]
                        if len(self.stack_pos) > 0 and self.stack_pos[-1] > tree.meta.start_pos and prevnode.startswith('except'):
                            self.A.add_edge(prevnode, n, label='No') # yes
                        elif not n.startswith('else') and self.break_contine == 1 and ((node.startswith('if') or node.startswith('elif_') or node.startswith('else')) and (int(cur_indent) == int(indent)+1)):
                                if node not in self.list_control and n != self.new_else:
                                    self.A.add_edge(node, n, label='True')
                                    self.list_control.append(node)
                        elif len(self.stack_pos) > 0 and self.stack_pos[-1] > tree.meta.start_pos and  (
                                prevnode == 'for ' + str(self.count_for) + ' ' + str(self.count_indent - 1) or prevnode == 'while ' + str(self.count_while) + ' ' + str(self.count_indent - 1)): #  self.A.nodes()[-2
                            if prevnode.startswith('while'):
                                if self.is_sub == 1:
                                    self.A.add_edge(node, n)
                                    self.is_sub = 0
                                else:
                                    self.A.add_edge(prevnode, n, label='True')
                            else:
                                self.A.add_edge(prevnode, n, label='Yes')
                        elif n.startswith('else'):
                            if not self.last_pop.startswith('elif_'):
                                print('x')
                        elif (self.last_pop.startswith('for') or self.last_pop.startswith('while')) and int(node_indent) != int(self.last_pop.split()[2]): # != küüktür büyüktür olabilir
                             self.last_pop = ''
                        elif not self.A.nodes()[-1].startswith('end') and (self.last_pop != 'elif_ ' + str(self.counter_if) + ' ' + str(self.count_indent - 1) and n != 'elif_ ' + str(self.counter_if) + ' ' + str(self.count_indent - 1)): # and di
                            if self.is_sub == 1:
                                self.A.add_edge(node, n)
                                self.is_sub = 0
                            else:
                                self.A.add_edge(prevnode, n)
                    else:
                        self.break_contine = 0
                else:
                    self.last_pop = ''

        except:
            print('stmt error')

    def loop_pop(self, n, stmt, tree, end_string, f_label):
        try:
            indent_node = n.split()[2]
        except:
            indent_node = (int(tree.meta.column) - 1) / 4
        self.counter_loop = 0
        self.is_loop = 0
        self.count_pop += 1
        self.count_pop_for += 1
        indent = stmt.split()[2]
        node = self.A.get_node(stmt)
        counter = node.split()[1]
        end_loop = end_string + counter + ' ' + indent
        self.A.add_node(n=end_loop, label='END', shape='ellipse')
        if node in self.dict_break.keys():
            self.A.add_edge(self.dict_break[node], end_loop, label='break')
        if node in self.dict_continue.keys():
            self.A.add_edge(self.dict_continue[node], node, label='continue')
            self.break_contine = 1
        self.A.add_edge(node, end_loop, label=f_label)
        indent_for, node_for = self.find_loop_node()
        node_f = ''
        if node_for != '':
            node_f = node_for
        if n.startswith('for') or n.startswith('while'):
            indent_n = n.split()[2]
            if int(indent) == int(indent_n):
                self.A.add_edge(end_loop, n, label='Try Next Item')  # next for
            elif int(indent) > int(indent_n) and int(indent) <= int(indent_for):
                self.A.add_edge(end_loop, n,
                                label='Try Next Item')  # next for
            elif int(indent) > int(indent_for) and int(indent_for) != -1:
                self.A.add_edge(end_loop, node_f, label='Try Next Item')
            if self.count_pop_for < 2:
                index = self.A.nodes().index(n) - 1
                node = self.A.nodes()[index]
                for i in range(0, len(self.A.nodes())):
                    if node.startswith('end'):
                        node = self.A.nodes()[index - i]
                    else:
                        break
                subgraph_node_len = 0
                for subgraph in self.A.subgraphs():
                    if node in subgraph.nodes():
                        subgraph_node_len = len(subgraph.nodes())
                        node = self.A.nodes()[index - subgraph_node_len + 1]
                self.A.add_edge(node, stmt, label='Try Next Item')
        elif node_for.startswith('for') or node_for.startswith(
                'while') and int(indent) > int(indent_for):
            if int(indent_node) == int(indent):
                self.A.add_edge(end_loop, n, label='Try Next Item')
            elif int(indent_node) < int(indent):
                self.A.add_edge(end_loop, node_for, label='Try Next Item')
            if self.last_node_loop != stmt:
                if n.startswith('else'):
                    index = -2
                else:
                    index = self.A.nodes().index(n) - 1
                node = self.A.nodes()[index]
                subgraph_node_len = 0
                for subgraph in self.A.subgraphs():
                    if node in subgraph.nodes():
                        subgraph_node_len = len(subgraph.nodes())
                        node = self.A.nodes()[index - subgraph_node_len + 1]
                self.A.add_edge(node, stmt,
                                label='Try Next Item')
                self.last_node_loop = node_for
        else:
            if n.startswith('elif_') or n.startswith('else'):
                if str(int(indent) - 1) not in self.dict_true.keys():
                    self.dict_true[str(int(indent) - 1)] = []
                self.dict_true[str(int(indent) - 1)].append(end_loop)
            else:
                self.A.add_edge(end_loop, n)
            if self.count_pop_for < 2:
                index = -1
                node = self.A.nodes()[index - 1]
                if len(n.split()) == 1 or n.startswith('elif_') or n.startswith('if') or n.startswith(
                        'for') or n.startswith('while'):
                    node = self.A.nodes()[index - 1 - 1]
                else:
                    node = self.A.nodes()[index - 1]
                subgraph_node_len = 0
                for subgraph in self.A.subgraphs():
                    if node in subgraph.nodes():
                        subgraph_node_len = len(subgraph.nodes())
                        node = self.A.nodes()[index - subgraph_node_len - 1]
                self.A.add_edge(node, stmt, label='Try Next Item')
        for i in self.dict_false.keys():
            if int(i) > int(indent):
                list_false = self.dict_false[i]
                for item in list_false:
                    self.A.add_edge(item, stmt)
                self.dict_false[i].clear()
        for i in self.dict_true.keys():
            if int(i) > int(indent):
                list_true = self.dict_true[i]
                for item in list_true:
                    self.A.add_edge(item, stmt)
                self.dict_true[i].clear()
        self.last_pop = stmt
        self.count_indent -= 1
        return indent, node_f

    def find_loop_node(self):
        i = -1
        c = 0
        node_for = ''
        indent_for = -1
        if len(self.stack_stmt) > 0:
            node_for = self.stack_stmt[i]
            try:
                indent_for = node_for.split()[2]
            except:
                indent_for = -1
            while len(self.stack_stmt) > c and (
                    not self.stack_stmt[i].startswith('for') and not self.stack_stmt[i].startswith(
                'while')):  # or while
                i -= 1
                c += 1
                try:
                    node_for = self.stack_stmt[i]
                    indent_for = node_for.split()[2]
                except:
                    #node_for = ''
                    indent_for = -1
                    print('invalid')
        return indent_for, node_for

    def stmts(self, tree, stmt_type):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                text = ''
                if stmt_type != 'try' and stmt_type != 'except':
                    for i in range(tree.meta.line - 1, tree.meta.end_line):
                        text += self.lines[i]
                    if tree.meta.line == tree.meta.end_line:
                        text = text.strip()
                n = ''
                if stmt_type == 'assign':
                    n = stmt_type + str(self.count_assign)
                    self.count_assign += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                    self.stmt_pop(tree, n)
                elif stmt_type == 'expr':
                    n = stmt_type + str(self.count_expr)
                    self.count_expr += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                    self.stmt_pop(tree, n)
                elif stmt_type == 'with':
                    n = stmt_type + str(self.count_with)
                    self.count_with += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                    self.stmt_pop(tree, n)
                elif stmt_type == 'try':
                    self.count_try += 1
                    n = stmt_type + ' ' + str(self.count_try) + ' ' + str(self.count_indent)
                    self.A.add_node(n=n, label='try', shape='rect')
                    self.stmt_pop(tree, n)
                    self.count_indent += 1
                elif stmt_type == 'except':
                    text = 'except'
                    i = 0
                    f = 0
                    while len(self.stack_pos) > 0 and tree.meta.start_pos >= self.stack_pos[i - 1]:
                        i -= 1
                        node_pop = self.stack_stmt[i]
                        f = 1
                    if f == 1:
                        indent_pop = node_pop.split()[2]
                        n = stmt_type + ' ' + str(self.count_try) + ' ' + indent_pop - 1
                    else:
                        n = stmt_type + ' ' + str(self.count_try) + ' ' + str(self.count_indent - 1)
                    self.A.add_node(n=n, label=text, shape='diamond')
                    self.stmt_pop(tree, n)
                    self.stack_stmt.append(n)
                    self.stack_pos.append(tree.meta.end_pos)
                elif stmt_type == 'for':
                    text = self.lines[tree.meta.line - 1][0:-1].strip()
                    text = text[4:-1]
                    self.loop_stmt(str(self.count_for), stmt_type, text, tree)
                elif stmt_type == 'while':
                    text = self.lines[tree.meta.line - 1][0:-1].strip()
                    text = text[6:-1]
                    self.loop_stmt(str(self.count_while), stmt_type, text, tree)
                elif stmt_type == 'return':
                    n = stmt_type + str(self.count_return)
                    self.count_return += 1
                    self.A.add_node(n=n, label=text, shape='rect')
                    self.stmt_pop(tree, n)
                elif stmt_type == 'break':
                    text = 'break'
                    n = stmt_type + ' ' + str(self.count_break) + ' ' + str(self.count_indent)
                    self.stmt_pop(tree, n)
                    i = -1
                    node_loop = ''
                    while (not self.A.nodes()[i].startswith('for') and not self.A.nodes()[i].startswith('while')) or (self.A.nodes()[i].startswith('for') and  self.A.nodes()[i].startswith('while') and (self.count_indent == node_loop.split()[2])):
                        i -= 1
                        node_loop = self.A.nodes()[i]
                    if node_loop not in self.dict_break.keys():
                        self.dict_break[node_loop] = ''
                    self.dict_break[node_loop] =  self.A.nodes()[-1]
                elif stmt_type == 'continue':
                    text = 'continue'
                    n = stmt_type + ' ' + str(self.count_continue) + ' ' + str(self.count_indent)
                    self.stmt_pop(tree, n)
                    i = -1
                    node_loop = ''
                    while not self.A.nodes()[i].startswith('for') and not self.A.nodes()[i].startswith('while'):
                        i -= 1
                        node_loop = self.A.nodes()[i]
                    if node_loop not in self.dict_continue.keys():
                        self.dict_continue[node_loop] = ''
                    self.dict_continue[node_loop] = self.A.nodes()[-1]
        except:
            print("stmts error")

    def loop_stmt(self, count, stmt_type, text, tree):
        i = 0
        f = 0
        c = 0
        while len(self.stack_pos) > c and tree.meta.start_pos >= self.stack_pos[i - 1]:
            i -= 1
            node_pop = self.stack_stmt[i]
            f = 1
            c += 1
        if f == 1:
            indent_pop = node_pop.split()[2]
            n = stmt_type + ' ' + count + ' ' + indent_pop
        else:
            n = stmt_type + ' ' + count + ' ' + str(self.count_indent)
        self.A.add_node(n=n, label=text, shape='hexagon')
        self.counter_loop += 1
        self.stmt_pop(tree, n)
        self.count_indent += 1
        self.stack_stmt.append(n)
        self.stack_pos.append(tree.meta.end_pos)

    def assign_stmt(self, tree):
            self.stmts(tree, 'assign')

    def expr_stmt(self, tree):
            self.stmts(tree, 'expr')

    def elifs(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                self.stmt_pop(tree, 'elifs ' + str(self.counter_if) + ' ' + str(self.count_indent))
                self.stack_pos.append(1)
                self.stack_stmt.append('elifs ' + str(self.counter_if) + ' ' + str(self.count_indent))
                print("--elif pos--")
        except:
            print("elifs error")

    def suite(self, tree):
        try:
            self.check_subgraph(tree)
            pad_indent = 0
            if len(self.stack_stmt) > 0 and ((self.stack_stmt[-1].startswith('for') or self.stack_stmt[-1].startswith('while'))):
                pad_indent = 1
            if (self.valid == 1 and 'elif_ ' + str(self.counter_if) + ' ' + str(self.count_indent - 1 - pad_indent) in self.stack_stmt) or (len(self.stack_stmt) > 0 and (self.valid == 1 and self.stack_stmt[-1] == 'elifs ' + str(self.counter_if) + ' ' + str(self.count_indent))): #or (self.subgraph == 1 and self.count_def > 0 and self.valid == 0):
                if 'elif_ ' + str(self.counter_if) + ' ' + str(self.count_indent - 1 - pad_indent) in self.stack_stmt:
                    index = self.stack_stmt.index('elif_ ' + str(self.counter_if) + ' ' + str(self.count_indent - 1 - pad_indent))
                elif 'elifs ' + str(self.counter_if) + ' ' + str(self.count_indent) in self.stack_stmt:
                    index = self.stack_stmt.index('elifs ' + str(self.counter_if) + ' ' + str(self.count_indent))
                i = index
                node = ''
                valid_else = 0
                while self.stack_pos[i] <= tree.meta.start_pos:
                    valid_else = 1
                    i -= 1
                if valid_else == 1:
                    node = self.stack_stmt[i]
                    indent = node.split()[2]
                    n = 'else ' + str(self.counter_if) + ' ' + indent
                    text = self.lines[tree.meta.line - 1][0:-1].strip()

                    self.stmt_pop(tree, n)
                    self.flag_else = 1
                    self.stack_stmt.append(n)
                    self.stack_pos.append(tree.meta.end_pos)
        except:
            print("suite error")

    def elif_(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                text = self.lines[tree.meta.line - 1][0:-1].strip()
                text = text[5:-1]
                print(text)
                i = -1
                node = ''
                valid_else = 0
                while self.stack_pos[i] <= tree.meta.start_pos:
                    valid_else = 1
                    i -= 1
                if valid_else == 1:
                    node = self.stack_stmt[i]
                    indent = node.split()[2]
                    n = 'elif_ ' + str(self.counter_if) + ' ' + str(indent)
                    self.A.add_node(n=n, label=text, shape='diamond')
                    self.stmt_pop(tree, n)
                    self.stack_pos.append(tree.meta.end_pos)
                    self.stack_stmt.append(n)
                    indent = str(self.count_indent - 1)
                    if indent not in self.dict_false.keys():
                        self.dict_false[indent] = []
                    self.dict_false[indent].append(n)
        except:
            print("elif_ error")

    def if_stmt(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                text=''
                i = 0
                text = self.lines[tree.meta.line - 1][0:-1].strip()
                text = text[3:-1]
                i = 0
                f = 0
                c = 0
                while len(self.stack_pos) > c and tree.meta.start_pos >= self.stack_pos[i - 1]:
                    i -= 1
                    node_pop = self.stack_stmt[i]
                    f = 1
                    c += 1
                if f == 1:
                    indent_pop = node_pop.split()[2]
                    n = 'if' + ' ' + str(self.counter_if) + ' ' + indent_pop
                else:
                    n = 'if' + ' ' + str(self.counter_if) + ' ' + str(self.count_indent)
                self.counter_if += 1
                self.A.add_node(n=n, label=text, shape='diamond')
                self.stmt_pop(tree, n)
                self.count_indent += 1
                self.stack_stmt.append(n)
                self.stack_pos.append(tree.meta.end_pos)
                indent = n.split()[2]
                if indent not in self.dict_false.keys():
                    self.dict_false[indent] = []
                self.dict_false[indent].append(n)
                self.is_if = 1
        except:
            print("if error")

    def continue_stmt(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                self.count_continue += 1
                self.stmts(tree, 'continue')
        except:
            print('continue stmt error')

    def break_stmt(self, tree):
        try:
            self.check_subgraph(tree)
            if self.valid == 1:
                self.count_break += 1
                self.stmts(tree, 'break')
        except:
            print('break stmt error')

    def check_subgraph(self, tree):
        while self.count_def > 1 and self.valid == 0 or (self.subgraph == 0 and self.count_def > 0):
            if tree.meta.start_pos >= self.stack_pos[-1]:
                self.stack_pos.pop()
                stmt = self.stack_stmt.pop()
                if stmt.startswith('def'):
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

    def while_stmt(self, tree):
        try:
            self.count_while += 1
            self.stmts(tree, 'while')
        except:
            print("while stmt error")

    def for_stmt(self, tree):
        try:
            self.count_for += 1
            self.stmts(tree, 'for')
        except:
            print("for stmt error")