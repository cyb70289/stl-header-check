# scan source file to see if there's missing or redundant stl headers

import pickle
import os
import re
import sys


# returns a set of all std::xxxx and a set of all stl headers from a c++ source
def get_stl_funcs_headers(fn):
    content = open(fn).read()

    headers = set()
    tokens = re.findall(r'#include[ \t]+<[a-zA-Z0-9_]+>', content)
    for token in tokens:
        header = token[token.find('<')+1 : -1]
        headers.add(header)

    funcs = set()
    tokens = re.findall(r'std::[a-zA-Z0-9_]+', content)
    for token in tokens:
        func = token[5:]
        funcs.add(func)

    if verbose:
        print('headers: {}'.format(sorted(headers)))
        print('funcs: {}'.format(sorted(funcs)))
    return funcs, headers


verbose = '-v' in sys.argv
fn = os.path.dirname(os.path.realpath(__file__)) + '/stl-func-to-header.pickle'
funcs_to_headers = pickle.load(open(fn, 'rb'))

for fn in sys.argv[1:]:
    if fn == '-v':
        continue
    funcs, headers = get_stl_funcs_headers(fn)

    missing_headers = []

    for func in funcs:
        if func not in funcs_to_headers:
            if verbose:
                print('SKIP std::{}, not in cplusplus.com?'.format(func))
            continue
        required_headers = funcs_to_headers[func]
        # some func may be defined in several headers
        # make sure at least one of them is included
        if not (headers & required_headers):
            missing_headers.append((func, required_headers))

    if missing_headers:
        print('FILE:', fn)
        print('++++++++++ MISSING HEADERS ++++++++++'.format(fn))
        # sort missing headers by len(required_headers)
        missing_headers = sorted(missing_headers, key=lambda x: len(x[1]))
        headers_so_far = set()
        for func, required_headers in missing_headers:
            if not (headers_so_far & required_headers):
                print('+#include', end='')
                for header in sorted(required_headers):
                    print(' <{}>'.format(header), end='')
                headers_so_far = headers_so_far.union(required_headers)
                print('\t// std::{}'.format(func))
        print('\n')
