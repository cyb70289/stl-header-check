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

    #print('headers: {}'.format(sorted(headers)))
    #print('funcs: {}'.format(sorted(funcs)))
    return funcs, headers


# symbols in these headers may be used without std:: prefix
# e.g., c (memcpy, int32_t), iostream (<<, >>), ...
def get_nostd_headers():
    nostd_headers = \
        '''
        cassert cctype cerrno cfenv cfloat cinttypes ciso646 climits clocale
        cmath csetjmp csignal cstdalign cstdarg cstdbool cstddef cstdint cstdio
        cstdlib cstring ctgmath ctime cuchar cwchar cwctype iostream
        '''
    return set(nostd_headers.split())


verbose = '-v' in sys.argv
fn = os.path.dirname(os.path.realpath(__file__)) + '/stl-func-to-header.pickle'
funcs_to_headers = pickle.load(open(fn, 'rb'))

for fn in sys.argv[1:]:
    if fn == '-v':
        continue
    funcs, headers = get_stl_funcs_headers(fn)

    missing_headers = []
    # exclude headers including funcs can be called without std::
    redundant_headers = headers - get_nostd_headers()

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
        redundant_headers -= required_headers

    if not missing_headers and not redundant_headers:
        continue

    print('FILE:', fn)
    if missing_headers:
        # sort missing headers by len(required_headers)
        missing_headers = sorted(missing_headers, key=lambda x: len(x[1]))
        headers_so_far = set()
        print('++++++++++ MISSING HEADERS ++++++++++'.format(fn))
        for func, required_headers in missing_headers:
            if not (headers_so_far & required_headers):
                print('+#include', end='')
                for header in sorted(required_headers):
                    print(' <{}>'.format(header), end='')
                headers_so_far = headers_so_far.union(required_headers)
                print('\t// std::{}'.format(func))
    # redundant header checking is a bit noisy, hide it if not verbose mode
    if redundant_headers and verbose:
        print('---------- UNUSED HEADERS ----------'.format(fn))
        for header in redundant_headers:
            print('-#include <{}>'.format(header))
    print('\n')
