#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import OrderedDict


# our option format
# no check, load, save methods for this implemented
example = {
    'name1': (int, True),
    'name2': (bool, False),
    'name3': (float, False),
    'name4': (str, False)
}


class OptPars(object):
    """
    Class for parsing command line arguments
    """
    def __init__(self, optionlist):
        self.optionlist = optionlist

    def __checkrequired(self, passed):
        """
        Checks passed option names
        """
        passedoptions = set(passed)
        if len(passed) != len(passedoptions):
            raise ValueError('Multiple option definition')
        if not (passedoptions <= set(self.optionlist.keys())):
            raise ValueError('Unknown options')
        required = {option for option in self.optionlist if self.optionlist[option][1]}
        if not (required <= passedoptions):
            raise ValueError('Required options missing')

    def printhelp(self):
        """
        Prints help message
        """
        orderedoptions = OrderedDict(sorted(self.optionlist.items(), key=lambda t: -t[1][1]))
        helpmsg = 'Usage: %s' % sys.argv[0]
        for optname, optsetting in orderedoptions.items():
            optsign = '--' + optname
            if optsetting[0] != bool:
                optsign +='=<%s>' % optsetting[0].__name__
            helpmsg += ' ' + (optsign if optsetting[1] else ('['+optsign+']'))
        helpmsgalt = helpmsg.replace('=', ' ')
        helpmsg += '\nOr\n' + helpmsgalt
        helpmsg += '\n\'%s --help\' to show help message\n' % sys.argv[0]
        print(helpmsg)

    def parse(self):
        """
        Parses command line arguments
        returns dictionary {'OptionName': value}
        """
        argv = sys.argv[1:]
        if ('--help' in argv):
            self.printhelp()
            return

        # grouping pairs of passed strings
        splitargs = []
        while argv:
            if argv[0][:2] == '--':
                argpart =[]
                if '=' in argv[0]:
                    splitargs.append(argv.pop(0)[2:].split('='))
                else:
                    argpart.append(argv.pop(0)[2:])
                    argpart.append(argv.pop(0)) if (argv and not argv[0][:2] == '--') else None
                    splitargs.append(argpart)
            else:
                raise ValueError('Incorrect format')

        self.__checkrequired([part[0] for part in splitargs])

        # generating dict {'option': value} from pairs
        optdict = {}
        for part in splitargs:
            opttype = self.optionlist[part[0]][0]
            if opttype == bool:
                if len(part) > 1:
                    raise ValueError('No value needed for boolean flag %s' % part[0])
                optdict.update({part[0]: True})
            else:
                if len(part) == 1:
                    raise ValueError('No value for %s' % part[0])
                optdict.update({part[0]: opttype(part[1])})
        return optdict


if __name__ == '__main__':
    parser = OptPars(example)
    try:
        out = parser.parse()
        print(out)
    except ValueError as e:
        print('\nError: incorrect input passed: %s\n\nSee example of usage:\n' % str(e))
        parser.printhelp()
        sys.exit()
