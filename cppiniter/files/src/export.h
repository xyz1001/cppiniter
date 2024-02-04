#pragma once

// clang-format off
// Generic helper definitions for shared library support
#if defined _WIN32 || defined __CYGWIN__
  #define {{{project_name_uppercase}}}_HELPER_DLL_IMPORT __declspec(dllimport)
  #define {{{project_name_uppercase}}}_HELPER_DLL_EXPORT __declspec(dllexport)
  #define {{{project_name_uppercase}}}_HELPER_DLL_LOCAL
#else
  #if __GNUC__ >= 4
    #define {{{project_name_uppercase}}}_HELPER_DLL_IMPORT __attribute__ ((visibility ("default")))
    #define {{{project_name_uppercase}}}_HELPER_DLL_EXPORT __attribute__ ((visibility ("default")))
    #define {{{project_name_uppercase}}}_HELPER_DLL_LOCAL  __attribute__ ((visibility ("hidden")))
  #else
    #define {{{project_name_uppercase}}}_HELPER_DLL_IMPORT
    #define {{{project_name_uppercase}}}_HELPER_DLL_EXPORT
    #define {{{project_name_uppercase}}}_HELPER_DLL_LOCAL
  #endif
#endif

// Now we use the generic helper definitions above to define {{{project_name_uppercase}}}_API and {{{project_name_uppercase}}}_LOCAL.
// {{{project_name_uppercase}}}_API is used for the public API symbols. It either DLL imports or DLL exports (or does nothing for static build)
// {{{project_name_uppercase}}}_LOCAL is used for non-api symbols.

#ifdef {{{project_name_uppercase}}}_DLL // defined if {{{project_name_uppercase}}} is compiled as a DLL
  #ifdef {{{project_name_uppercase}}}_DLL_EXPORTS // defined if we are building the {{{project_name_uppercase}}} DLL (instead of using it)
    #define {{{project_name_uppercase}}}_API {{{project_name_uppercase}}}_HELPER_DLL_EXPORT
  #else
    #define {{{project_name_uppercase}}}_API {{{project_name_uppercase}}}_HELPER_DLL_IMPORT
  #endif // {{{project_name_uppercase}}}_DLL_EXPORTS
  #define {{{project_name_uppercase}}}_LOCAL {{{project_name_uppercase}}}_HELPER_DLL_LOCAL
#else // {{{project_name_uppercase}}}_DLL is not defined: this means {{{project_name_uppercase}}} is a static lib.
  #define {{{project_name_uppercase}}}_API
  #define {{{project_name_uppercase}}}_LOCAL
#endif // {{{project_name_uppercase}}}_DLL
// clang-format on
