#coding=utf-8
from tree_sitter import Language,Parser
import warnings
warnings.simplefilter('ignore', FutureWarning) 
 
Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',
  
  # Include one or more languages
  [
    'vendor/tree-sitter-java-master',
    'vendor/tree-sitter-c-sharp-master',
  ]
)