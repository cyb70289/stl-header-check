A tool to find missing stl headers in a c++ source file.
The stl headers are supposed to be directly included in the source file, not through other includes indirectly.

**analyse-cpp.py**

Check and list missing stl headers.

*Example commands:*

```
$ python3 analyse-cpp.py head.hpp src.cpp
$ find ~/my-project/ -name "*.hpp" | xargs python3 analyse-cpp.py
```

*Example outputs:*

```
FILE: /home/me/my-project/include/mytest.hpp
++++++++++ MISSING HEADERS ++++++++++
+#include <cstring>     // std::memcpy
+#include <type_traits> // std::enable_if
+#include <utility>     // std::pair
```

**stl-func-to-header.py**

Python script to create a dict to map std:xxxxx to the headers defining it. E.g., `std::cout -> <iostream>`.

The info is fetched and parsed from www.cplusplus.com webpage.

**stl-func-to-header.pickle**

Pickle file storing the dict. Created by stl-func-to-header.py.

**stl-func-to-header.csv**

A csv file storing the function to header mapping. Generated from stl-func-to-header.py stdout.

**Know issues**

Some stl functions/classes are not available on cplusplus website, e.g., `std::integer_sequence`.
And some info is not complete, e.g., `chrono` class is not listed in the chrono page.
These symbols are missing in the generated dictionary and skipped in source code analysis.
