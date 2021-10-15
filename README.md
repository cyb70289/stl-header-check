A tool to find missing stl headers in a c++ source/header file.
The stl headers are supposed to be directly included in the source file, not through other includes indirectly.

**check-stl-headers.py**

Check and list missing stl headers.

*Example commands:*

```
$ python3 check-stl-headers.py file1.hpp file2.cpp ...
$ find ~/my-project/ -name "*.hpp" | xargs python3 check-stl-headers.py
```

*Example outputs:*

```
FILE: /home/work/my-project/include/mytest.hpp
++++++++++ MISSING HEADERS ++++++++++
+#include <cstring>     // std::memcpy
+#include <type_traits> // std::enable_if
+#include <utility>     // std::pair
```

**stl-func-to-header.py**

Python script to create a dict to map std:xxxxx to the headers defining it. E.g., map `std::cout` to `<iostream>`.

Please note one stl function may be defined in several headers. So the value of the dict is a set. E.g., key = `sin`, value = `{cmath, complex, valarray}`.

The stl reference is fetched and parsed from www.cplusplus.com webpage. E.g., classes/functions in `<tuple>` is extracted from html page http://www.cplusplus.com/reference/tuple/, in the box at left bottom corner.

**stl-func-to-header.pickle**

Pickle file storing the dict. Created by stl-func-to-header.py.

**stl-func-to-header.csv**

A csv file storing the function to header mapping. Generated from stl-func-to-header.py stdout.

**Know issues**

Some stl functions/classes are not available on cplusplus website, e.g., `std::integer_sequence`.
And some info is not complete, e.g., `chrono` class is not listed in the chrono  reference page.
These symbols are missing in the generated dictionary and skipped in source code analysis.
