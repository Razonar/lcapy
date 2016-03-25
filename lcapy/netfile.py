import lcapy.grammar as grammar
from lcapy.parser import Parser


class NetfileMixin(object):

    def init_parser(self, cpts):
        self.parser = Parser(cpts, grammar)        

    def include(self, string):

        parts = string.split(' ')
        if len(parts) < 2 or parts[0] != '.include':
            raise ValueError('Expecting include filename in %s' % string)
        filename = parts[1]
        if len(parts) == 2:
            return self.netfile_add(filename, self.namespace)
        
        if len(parts) != 4 and parts[2] != 'as':
            raise ValueError('Expecting include filename as name in %s' % string)
        name = parts[3]
        namespace = self.namespace
        self.namespace = name + '.' + namespace
        ret = self.netfile_add(filename, self.namespace)        
        self.namespace = namespace
        return ret

    def parse(self, string, namespace=''):
        """The general form is: 'Name Np Nm symbol'
        where Np is the positive nose and Nm is the negative node.

        A positive current is defined to flow from the positive node
        to the negative node.
        """

        if string == '':
            return None            

        if string[0] == ';':
            #TODO
            #self.opts.add(string[1:])
            return None

        if string[0:9] == '.include ':
            self.include(string)
            return None

        cpt = self.parser.parse(namespace + string, self)
        return cpt

    def add(self, string, namespace=''):
        """The general form is: 'Name Np Nm symbol'
        where Np is the positive nose and Nm is the negative node.

        A positive current is defined to flow from the positive node
        to the negative node.
        """

        if '\n' in string:
            lines = string.split('\n')
            for line in lines:
                self.add(line.strip(), namespace)
            return

        cpt = self.parse(string, namespace)
        if cpt is not None:
            self._cpt_add(cpt)
