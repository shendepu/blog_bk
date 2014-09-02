Perl Basis
==========




Expression
----------

True Expressions vs False Expression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Perl every expression is considered **true** except for the following three cases:

1. The number 0.
2. The empty string ("").
3. A special value called undef. This is the default value of every variable that was not initialized before it was accessed.

Operators
----------

* ``\-``
* ``\*``
* ``/``
* ``a ** b``
* ``a . b``
* ``a % b``
* ``( sub-expr )``
* ``+=``, ``-=``, ``*=``, ``/=``, ``**=``
* ``<<=``, ``>>=``, ``||=``, ``&&=``
* ``&=``, ``|=``
* ``.=``, ``%=``, ``^=``
* ``//=``, ``x=``
* ``>>``, ``<<``
* ``\x``
* ``\\``: 
  
    returns the reference to an existing variable

* ``->``: 

    can be used to directly access the elements of an array or a hash referenced by a certain hash. e.g. *$array_ref->[5]* will retrieve the 5th element of the array pointed to by *$array_ref*
  
.. code-block:: perl

    use strict;
    use warnings;

    my $sum = 0;

    sub update_sum
    {
        my $ref_to_sum = shift;
        foreach my $item (@_)
        {
            # The ${ ... } dereferences the variable
            ${$ref_to_sum} += $item;
        }
    }

    update_sum(\$sum, 5, 4, 9, 10, 11);
    update_sum(\$sum, 100, 80, 7, 24);

    print "\$sum is now ", $sum, "\n";

* ``[ @array ]``
    
    a Dynamic Reference to an Array

* ``{ %hash }`` 
  
    a Dynamic Reference to a Hash

* ``=~`` 

    binds a scalar expression to  a pattern matach

* ``!~`` 

    just like *=~* except return value is negated in the logical sense

* ``&&``, ``||``
* ``and``, ``or`` 

    identical to *&&* and *||*, but is much lower in prededence

* ``! $x``

* ``&`` 

    returns its operands ANDed together bit by bit

* ``|`` 
  
    returns its operands ORed together bit by bit

* ``^`` 

    returns its operands XORed together bit by bit.

* ``//`` 

    is exactly the same as ``||``, except that it tests the left hand side's definedness instead of its truth.
  
.. code-block:: perl

     $home =  $ENV{HOME}
           // $ENV{LOGDIR}
           // (getpwuid($<))[7]
           // die "You're homeless!\n";

* ``..`` 

    range operator, which is really two different operators depending on the context

* ``...`` 

    behave just like *..* does, but does not test right operand until next evaluation

.. code-block:: perl

    @lines = ("   - Foo",
              "01 - Bar",
              "1  - Baz",
              "   - Quux");
    
    # print out
    # 01 - Bar          
    foreach (@lines) {
        if (/0/ .. /1/) {
            print "$_\n";
        }
    }
 
    # print out
    # 01 - Bar  
    # 1  - Baz        
    foreach (@lines) {
        if (/0/ ... /1/) {
            print "$_\n";
        }
    } 

    # Difference between .. and ... is ... test right operand until next
    # evaluation of range operator 
    #
    # .. : if (/0/ .. /1/) implicitly means if ($_ == /0/ .. $_ == /1/),
    #      the range operator becomes true at element 2 for left operand,
    #      and immediately evaluate right operand that set operator false, 
    #      but return true for current. 
    #
    # ... : range operator becomes true at element 2 for left operand 
    #      evaluation, but does not test right operand. 
    #
    #      At next evaluation, since operator is true, left operand will 
    #      not be tested. Since operator is true, it tests right operand /1/, 
    #      then operator becomes flase while return value is still true for 
    #      current.
    #
    #      At next evaluation (for "   - Quux""), left operand is tested 
    #      since operator is false, but failed, so element is not printed. 

* ``?:`` 
* ``,`` 

    Binary "," is the comma operator. In scalar context it evaluates its left argument, throws that value away, then evaluates its right argument and returns that value. This is just like C's comma operator.

    In list context, it's just the list argument separator, and inserts both its arguments into the list. These arguments are also evaluated from left to right.

    The comma concatenates two arrays. *@lines = ("One fish", "Two fish", "Red fish", "Blue fish");*

* ``=>``

    The *=>* operator is a synonym for the comma except that it causes a word on its left to be interpreted as a string if it begins with a letter or underscore and is composed only of letters, digits and underscores. 


Comparison Operator
^^^^^^^^^^^^^^^^^^^

* ``eq``, ``ne``, ``gt``, ``lt``, ``ge``, ``ne``
  
    String comparison operator

* ``==``, ``!=``, ``>``, ``<``, ``>=``, ``<=``
  
    Numerical comparison operator

* ``<=>``: 
  
    *$x <=> $y* returns -1 if *$x* is numerically lesser than *$y*, 1 if it's greater, and zero if they are equal.

* ``cmp``

    does the same for string comparison

* ``~~``

    does a smartmatch between its arguments (*since 5.10.1*)


Quote and Quote-like Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------+---------+-----------------+--------------+
| Customary | Generic | Meaning         | Interpolates |
+===========+=========+=================+==============+
| ''        | q{}     | Literal         | no           |
+-----------+---------+-----------------+--------------+
| ""        | qq{}    | Literal         | yes          |
+-----------+---------+-----------------+--------------+
| \`\`      | qx{}    | command         | yes*         |
+-----------+---------+-----------------+--------------+
|           | qw{}    | Word list       | no           |
+-----------+---------+-----------------+--------------+
| //        | m{}     | Pattern match   | yes*         |
+-----------+---------+-----------------+--------------+
|           | qr{}    | Pattern         | yes*         |
+-----------+---------+-----------------+--------------+
|           | s{}{}   | Substitution    | yes*         |
+-----------+---------+-----------------+--------------+
|           | tr{}{}  | Transliteration | no           |
+-----------+---------+-----------------+--------------+
|           | y{}{}   | Transliteration | no           |
+-----------+---------+-----------------+--------------+
| <<EOF     |         | here-doc        | yes*         |
+-----------+---------+-----------------+--------------+

\* unless the delimiter is ''.

Variables
---------

Variable Notations:
^^^^^^^^^^^^^^^^^^^

* ``$x`` 

    *$* prefix a variable

* ``@array`` 

    *@* prefix an array. 

    - ``scalar(@myarray)``

        refer to the number of elements in myarray

    - ``$#myarray``

        is equal to the maximal index itself (or -1 if the array is empty)

* ``%hash`` 

    *%* prefix a hash map


Special Variables
^^^^^^^^^^^^^^^^^^

* ``$ARG``, ``$_``
    
    The default input and pattern-searching space

    Here are the places where Perl will assume $_ even if you don't use it:

    - The following functions use $_ as a default argument:
    
      abs, alarm, chomp, chop, chr, chroot, cos, defined, eval, evalbytes, exp, fc, glob, hex, int, lc, lcfirst, length, log, lstat, mkdir, oct, ord, pos, print, printf, quotemeta, readlink, readpipe, ref, require, reverse (in scalar context only), rmdir, say, sin, split (for its second argument), sqrt, stat, study, uc, ucfirst, unlink, unpack.
    - All file tests (-f , -d ) except for -t , which defaults to STDIN. See -X
    - The pattern matching operations m//, s/// and tr/// (aka y///) when used without an =~ operator.
    - The default iterator variable in a foreach loop if no other variable is supplied.
    - The implicit iterator variable in the grep() and map() functions.
    - The implicit variable of given() .
    - The default place to put the next value or input record when a <FH> , readline, readdir or each operation's result is tested by itself as the sole criterion of a while test. Outside a while test, this will not happen.

* ``@_`` 
    
    Within a subroutine the array *@_* contains the parameters passed to that subroutine. Inside a subroutine, *@_* is the default array for the array operators **push**, **pop**, **shift**, and **unshift**.

* ``$LIST_SEPARATOR``, ``$"``
  
    When an array or an array slice is interpolated into a double-quoted string or a similar context such as /.../ , its elements are separated by this value. Default is a space. 

* ``$PROCESS_ID``, ``$PID``, ``$$``
    
    The process number of the Perl running this script.

* ``$PROGRAM_NAME``, ``$0``
  
    Contains the name of the program being executed.

* ``$REAL_GROUP_ID``, ``$GID``, ``$(``
  
    The real gid of this process.

* ``$EFFECTIVE_GROUP_ID``, ``$EGID``, ``$)``
  
    The effective gid of this process.

* ``$REAL_USER_ID``, ``$UID``, ``$<``
  
    The real uid of this process. 

* ``$EFFECTIVE_USER_ID``, ``$EUID``, ``$>``
  
    The effective uid of this process.

* ``$OSNAME``, ``$^O``
  
    The name of the operating system under which this copy of Perl was built

* ``$SUBSCRIPT_SEPARATOR``, ``$SUBSEP``, ``$;``
  
    The subscript separator for multidimensional array emulation. Default is "\034", the same as SUBSEP in awk. 

* ``$a``, ``$b``
  
    Special package variables when using *sort()*, see `sort() <http://perldoc.perl.org/functions/sort.html>`_

* ``%ENV``

    The hash *%ENV* contains your current environment. As of *v5.18.0*, both keys and values stored in *%ENV* are stringified.

* ``$SYSTEM_FD_MAX``, ``$^F``

    The maximum system file descriptor, ordinarily 2.

* ``@F``

    The array *@F* contains the fields of each line read in when autosplit mode is turned on

* ``@INC``
  
    The array *@INC* contains the list of places that the *do EXPR*, *require*, or *use* constructs look for their library files. 

* ``%INC``

    The hash *%INC* contains entries for each filename included via the *do*, *require*, or *use* operators.

* ``$BASETIME``, ``$^T``

    The time at which the program began running, in seconds since the epoch (beginning of 1970). 

* ``$PERL_VERSION``, ``$^V``
  
    The revision, version, and subversion of the Perl interpreter

* ``$EXECUTABLE_NAME``, ``$^X``
  
    The name used to execute the current copy of Perl

Variable related to regular expressions 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: perl

    $str =~ /pattern/;

    print $`, $&, $'; # bad: perfomance hit
    
    print             # good: no perfomance hit
        substr($str, 0,     $-[0]),
        substr($str, $-[0], $+[0]-$-[0]),
        substr($str, $+[0]);

* ``$<digits> ($1, $2, ...)``

    Contains the subpattern from the corresponding set of capturing parentheses from the last successful pattern match, not counting patterns matched in nested blocks that have been exited already.

* ``$MATCH``, ``$&``
  
    The string matched by the last successful pattern match

* ``${^MATCH}``
  
    This is similar to *$&* (*$MATCH*) except that it does not incur the performance penalty associated with that variable.

* ``$PREMATCH``, ``$\```

    The string preceding whatever was matched by the last successful pattern match

* ``${^PREMATCH}``

    This is similar to *$`* (*$PREMATCH*) except that it does not incur the performance penalty associated with that variable.

* ``$POSTMATCH``, ``$'``
  
    The string following whatever was matched by the last successful pattern match

* ``${^POSTMATCH}``
    
    This is similar to *$'* (*$POSTMATCH*) except that it does not incur the performance penalty associated with that variable.

* ``$LAST_PAREN_MATCH``, ``$+``

    The text matched by the last bracket of the last successful search pattern. 

* ``$LAST_SUBMATCH_RESULT``, ``$^N``
  
    The text matched by the used group most-recently closed (i.e. the group with the rightmost closing parenthesis) of the last successful search pattern.

* ``@LAST_MATCH_END``, ``@+``
    
    This array holds the offsets of the ends of the last successful submatches in the currently active dynamic scope.

* ``%LAST_PAREN_MATCH``, ``%+``

    Similar to *@+*, the *%+* hash allows access to the named capture buffers, should they exist, in the last successful match in the currently active dynamic scope.

* ``@LAST_MATCH_START``, ``@-``

* ``%LAST_MATCH_START``, ``%-``

.. code-block:: perl

    $` is the same as substr($var, 0, $-[0])
    $& is the same as substr($var, $-[0], $+[0] - $-[0])
    $' is the same as substr($var, $+[0])
    $1 is the same as substr($var, $-[1], $+[1] - $-[1])
    $2 is the same as substr($var, $-[2], $+[2] - $-[2])
    $3 is the same as substr($var, $-[3], $+[3] - $-[3])

* ``$LAST_REGEXP_CODE_RESULT``, ``$^R``
  
* ``${^RE_DEBUG_FLAGS}``
* ``${^RE_TRIE_MAXBUF}``



Variables related to file handle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``$,``, ``$OFS``, ``IO::Handle->output_field_separator( EXPR )``, ``$OUTPUT_FIELD_SEPARATOR``

    The output field separator for the print operator. If defined, this value is printed between each of print's arguments. Default is undef.

* ``$.``, ``$NR``, ``HANDLE->input_line_number( EXPR )``, ``$INPUT_LINE_NUMBER``

    Current line number for the last filehandle accessed.

* ``$/``, ``$RS``, ``IO::Handle->input_record_separator( EXPR )``, ``$INPUT_RECORD_SEPARATOR``

    The input record separator, newline by default. 

* ``$\``, ``$ORS``, ``IO::Handle->output_record_separator( EXPR )``, ``$OUTPUT_RECORD_SEPARATOR``

    he output record separator for the print operator.

* ``$|``, ``HANDLE->autoflush( EXPR )``, ``$OUTPUT_AUTOFLUSH``

    If set to nonzero, forces a flush right away and after every write or print on the currently selected output channel. Default is 0 

* ``${^LAST_FH}``

    This read-only variable contains a reference to the last-read filehandle. *since v5.18.0*


Variables related to formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``$^A``, ``$ACCUMULATOR``

    The current value of the write() accumulator for format() lines.

* ``$^L``, ``IO::Handle->format_formfeed(EXPR)``, ``$FORMAT_FORMFEED``

    What formats output as a form feed. The default is \f .

* ``$%``, ``HANDLE->format_page_number(EXPR)``, ``$FORMAT_PAGE_NUMBER``
    
    The current page number of the currently selected output channel.

* ``$-``, ``HANDLE->format_lines_left(EXPR)``, ``$FORMAT_LINES_LEFT``

    The number of lines left on the page of the currently selected output channel.

* ``$:``, ``IO::Handle->format_line_break_characters EXPR``, ``$FORMAT_LINE_BREAK_CHARACTERS``

    The default is " \n-"

* ``$=``, ``HANDLE->format_lines_per_page(EXPR)``, ``$FORMAT_LINES_PER_PAGE``

    The current page length (printable lines) of the currently selected output channel. The default is 60.

* ``$^``, ``HANDLE->format_top_name(EXPR)``, ``$FORMAT_TOP_NAME``

    The name of the current top-of-page format for the currently selected output channel. The default is the name of the filehandle with _TOP appended.

* ``$~``, ``HANDLE->format_name(EXPR)``, ``$FORMAT_NAME``

    The name of the current report format for the currently selected output channel. The default format name is the same as the filehandle name.


Error variables
^^^^^^^^^^^^^^^

$@ , $! , $^E , and $? => Perl interpreter, C library, operating system, or an external program


* ``$^E``, ``$EXTENDED_OS_ERROR``

    Error information specific to the current operating system. 

* ``$!``, ``$OS_ERROR``, ``$ERRNO``

    When referenced, $! retrieves the current value of the C errno integer variable.

* ``$?``, ``$CHILD_ERROR``
  
    The status returned by the last pipe close, backtick (`` ) command, successful call to wait() or waitpid(), or from the system() operator.

* ``$@``, ``$EVAL_ERROR``
  
    The Perl syntax error message from the last eval() operator

* ``%!``, ``%OS_ERROR``, ``%ERRNO``

    Each element of %! has a true value only if $! is set to that value. 

* ``$^S``, ``$EXCEPTIONS_BEING_CAUGHT``

    Current state of the interpreter.

    1. undef       - Parsing module, eval, or main program
    2. true (1)    - Executing an eval
    3. false (0)   - Otherwise

* ``$^W``, ``$WARNING``
    
    The current value of the warning switch, initially true if -w was used





















Functions
---------

* ``length``

    e.g. *print length("There's more than one way to do it"), "\n";*

* ``substr``

    e.g. *print substr("A long string", 1, 4), "\n";*

* ``int``

    e.g. *print "The whole part of 5.67 is " . int(5.67) . "\n";*

* ``split``

    e.g. *@components = split(/$regexp/, $string);*

* ``map``

    e.g. *@new_array = (map { <Some Expression with $_> } @array);*

* ``sort``
* ``grep``
* ``die``: 
* ``print``
* ``say``
    
    Just like *print*, but implicitly appends a newline.

.. code-block:: perl

    die "Can't cd to spool: $!\n" unless chdir '/usr/spool/news';
    chdir '/usr/spool/news' or die "Can't cd to spool: $!\n"
    chdir $foo    || die;

* ``ref``
    
    Returns a non-empty string if EXPR is a reference, the empty string otherwise. If EXPR is not specified, ``$_`` will be used. The value returned depends on the type of thing the reference is a reference to.

    Builtin types includes: ``SCALAR``, ``ARRAY``, ``HASH``, ``CODE``, ``REF``, ``GLOB``, ``LVALUE``, ``FORMAT``, ``IO``, ``VSTRING``, ``Regexp``



Escape Sequences

* ``\\ \\``
* ``\\"``
* ``\\$``
* ``\\@``
* ``\\n``
* ``\\r``
* ``\\t``
* ``\\xDD`` 

    where "DD" are two hexadecimal digits - gives the character whose ASCII code is "DD".

Input

.. code-block:: perl

    print "Please enter your name:\n";
    $name = <>;
    chomp($name);
    print "Hello, ", $name, "!\n";





Statement
---------

1. ``if () {} elseif () {} else {}``
2. ``while () {}``
3. ``last``, ``next``
4. ``for(row = 1 ; $row <= 10; $row++) { }``



Array
-----

* ``$myarray[-$n]`` 
    
    is equivalent to ``$myarray[scalar(@myarray)-$n]``.

* ``push``, ``pop``, ``shift``, ``join``, ``reverse``

Hash
----

* ``exists($myhash{$mykey})``
* ``keys(%myhash)``
* ``delete``

.. code-block:: perl

    %hash1 = (
    "shlomi" => "fish",
    "orr" => "dunkelman",
    "guy" => "keren"
    );

    %hash2 = (
        "george" => "washington",
        "jules" => "verne",
        "isaac" => "newton"
        );

    %combined = (%hash1, %hash2);

    foreach $key (keys(%combined))
    {
        print $key, " = ", $combined{$key}, "\n";
    }

File Input/Output
-----------------

* ``open my $my_file_handle, $mode, $file_path;``
* ``close($my_file_handle);``

mode
^^^^

* ``>``
  
    Writing (the original file will be erased before the function starts).

* ``<`` (or nothing)
  
    Reading

* ``>>``
  
    Appending (the file pointer will start at the end and the file will not be overridden) 

* ``+<``
  
    Read-write, or just write without truncating.    



Regular Expression
------------------

* ``"."`` 
  
    stands for any character

* ``[ ... ]`` 
  
    specifies more than one option for a character

* ``(?: ... )`` 
    
    cluster grouping notation

* ``( ... )`` 
  
    capture grouping notation

* ``=~`` 
  
    Binding operator tells Perl to match the pattern on the right against the string on the left, instead of matching against ``$_``.

* ``m//``

    match as being like word processor's "search" feature.

* ``s///``

    the operator simply replaces whatever part of a variable matches the pattern with a replacement string.

* ``tr///`` (aka ``y///``) 
* ``$&``

    the part of the string that actually matched the pattern is automatically stored in ``$&``.

* ``$```

    whatever came before the matched section in $& is in ``$```

* ``$'``

    whatever came after the matched section in $& is in ``$'``

* ``${^PREMATCH}``, ``${^MATCH}`` and ``${^POSTMATCH}``

.. code-block:: perl

    if ("Hello there, neighbor" =~ /\s(\w+),/) {
        print "That actually matched '$&'.\n";
    }
    # $` is "Hello"
    # $& is " there,"
    # $' is " neighbor"

* ``(?<LABEL>PATTERN)``, ``$+``
  
    Named Captures
  
.. code-block:: perl

    my $names = 'Fred or Barney';
    if ( $names =~ m/(?<name1>\w+) (?:and|or) (?<name2>\w+)/ ) {
        say "I saw $+{name1} and $+{name2}";
    }



Modifier
^^^^^^^^

* ``/g``

    the modifier tells *s///* to make all possible non-overlapping replacements
* ``/i``

    Case-insensitive matching

* ``/s``

    make *.* match any character

* ``/e``

    tells *s///* the right side is treated as a normal Perl expression, giving you the ability to use operators and functions.

.. code-block:: perl

    $string =~ s/^([A-Za-z]+)/length($1)/e;






References
----------

`Perl Doc <http://perldoc.perl.org/index.html>`_


.. author:: default
.. categories:: perl
.. tags:: perl
.. comments::
