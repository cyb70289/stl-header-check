# create a pickle file maps stl functions/classes to headers defining them
# one function may be defined in several headers
# e.g., {'sin':{'cmath','complex','valarray'}, 'cout':{'iostream'}, ...}
# you can also redirect stdout to a csv file

import pickle
import os
import re
import sys
from urllib.request import urlopen


def dprint(*msg):
    print('DEBUG:', *msg, file = sys.stderr)


# return a list of all stl headers
def retrieve_stl_headers():
    # Dump stl headers installed by libstdc++ under ubuntu
    #
    # STL_HDR_DIR="/usr/include/c++/9"
    # HDRS=$(find "${STL_HDR_DIR}" -maxdepth 1 -type f \( ! -iname "*.*" \))
    # echo $(for hdr in $HDRS; do basename $hdr; done | sort)

    headers = \
        '''
        algorithm any array atomic bit bitset cassert ccomplex cctype cerrno
        cfenv cfloat charconv chrono cinttypes ciso646 climits clocale cmath
        codecvt complex condition_variable csetjmp csignal cstdalign cstdarg
        cstdbool cstddef cstdint cstdio cstdlib cstring ctgmath ctime cuchar
        cwchar cwctype deque exception execution filesystem forward_list
        fstream functional future initializer_list iomanip ios iosfwd iostream
        istream iterator limits list locale map memory memory_resource mutex
        new numeric optional ostream queue random ratio regex scoped_allocator
        set shared_mutex sstream stack stdexcept streambuf string string_view
        system_error thread tuple typeindex typeinfo type_traits unordered_map
        unordered_set utility valarray variant vector version
        '''
    return headers.split()


# return a list of all functions/classes exported in an stl header
def retrieve_stl_funcs(header):
    # retrieve stl reference from cplusplus.com
    stl_ref_url = 'http://www.cplusplus.com/reference/{}/'.format(header)
    # extract function/class from http response
    # e.g., "/reference/iostream/cout/"
    stl_func_tag = '"/reference/{}/'.format(header)

    dprint('retrieving functions/classes in <{}>...'.format(header))
    funcs = set()
    try:
        page = urlopen(stl_ref_url).read().decode()
    except:
        dprint('FAILED AND SKIPPED <{}> !!!'.format(header))
        return []
    func_end = -1
    while True:
        tag_start = page.find(stl_func_tag, func_end + 1)
        if tag_start == -1:
            break
        func_start = tag_start + len(stl_func_tag)
        func_end = page.find('/"', func_start)
        if func_end == -1:
            break
        func = page[func_start:func_end]
        if not re.search(r'[^a-zA-Z0-9_]', func):
            funcs.add(func)
    return sorted(funcs)


out_file = 'stl-func-to-header.pickle'
if sys.argv[-1] != '-f' and os.path.exists(out_file):
    dprint('{} already exists!'.format(out_file))
    sys.exit()

funcs_to_headers = {}
headers = retrieve_stl_headers()
for header in headers:
    funcs = retrieve_stl_funcs(header)
    for func in funcs:
        if func in funcs_to_headers:
            funcs_to_headers[func].add(header)
        else:
            funcs_to_headers[func]={header}
        print('std::{},<{}>'.format(func, header))

with open(out_file, 'wb') as f:
    pickle.dump(funcs_to_headers, f)
