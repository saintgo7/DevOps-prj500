#!/bin/bash

# This script will help create README files for all programs

# Array of programs 106-120 with their descriptions
declare -A programs_106_120
programs_106_120["106"]="functions:Functions in C++:function declaration, parameters, overloading, recursion, lambdas"
programs_106_120["107"]="arrays:Arrays in C++:static arrays, multidimensional arrays, std::array, algorithms"
programs_106_120["108"]="pointers:Pointers in C++:pointer basics, arithmetic, dynamic memory, function pointers"
programs_106_120["109"]="references:References in C++:lvalue references, const references, rvalue references, move semantics"
programs_106_120["110"]="strings:Strings in C++:C-strings, std::string, string operations, std::string_view"
programs_106_120["111"]="structures:Structures in C++:struct definition, nested structures, member functions"
programs_106_120["112"]="enums:Enumerations in C++:enum, enum class, scoped enums"
programs_106_120["113"]="file_io:File I/O in C++:ifstream, ofstream, binary files, error handling"
programs_106_120["114"]="preprocessor:Preprocessor Directives:macros, conditional compilation, include guards"
programs_106_120["115"]="namespaces:Namespaces in C++:namespace definition, using declarations, nested namespaces"
programs_106_120["116"]="memory_management:Memory Management:new/delete, memory leaks, RAII"
programs_106_120["117"]="const_constexpr:Const and Constexpr:const correctness, constexpr functions"
programs_106_120["118"]="type_casting:Type Casting:static_cast, dynamic_cast, const_cast, reinterpret_cast"
programs_106_120["119"]="error_handling:Error Handling:exceptions, try-catch, custom exceptions"
programs_106_120["120"]="standard_io:Standard I/O:cin, cout, formatting, manipulators"

echo "Program mapping created"
