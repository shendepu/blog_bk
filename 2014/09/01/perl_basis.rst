Perl Basis
==========






Expression
^^^^^^^^^^


Operators

* ``\+`` 
* ``\-``
* ``\*``
* ``/``
* ``a ** b``
* ``a . b``
* ``a % b``
* ``( sub-expr )``
* ``\+=``, ``\-=``, ``\*=``, ``/=``
* ``\x``
* ``\\``: returns the reference to an existing variable
* ``->``: can be used to directly access the elements of an array or a hash referenced by a certain hash. e.g. ``$array_ref->[5]`` will retrieve the 5th element of the array pointed to by ``$array_ref``
  
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

* ``[ @array ]`` - a Dynamic Reference to an Array
* ``{ %hash }`` - a Dynamic Reference to a Hash


Functions

* ``length``: ``print length("There's more than one way to do it"), "\n";`` 
* ``substr``: ``print substr("A long string", 1, 4), "\n";`` 
* ``int``: ``print "The whole part of 5.67 is " . int(5.67) . "\n";``
* ``@ARGV``
* ``split``: e.g. @components = split(/$regexp/, $string);
* ``map``: e.g. @new_array = (map { <Some Expression with $_> } @array);
* ``sort``
* ``<=>``: ``$x <=> $y`` returns -1 if ``$x`` is numerically lesser than ``$y``, 1 if it's greater, and zero if they are equal.
* ``cmp``: does the same for string comparison
* ``grep``

Escape Sequences

* ``\\ \\``
* ``\\"``
* ``\\$``
* ``\\@``
* ``\\n``
* ``\\r``
* ``\\t``
* ``\\xDD`` - where "DD" are two hexadecimal digits - gives the character whose ASCII code is "DD".
* ``&&``
* ``||``
* ``! $x``
* ``,`` - The comma concatenates two arrays. ``@lines = ("One fish", "Two fish", "Red fish", "Blue fish");``

Input

.. code-block:: perl

    print "Please enter your name:\n";
    $name = <>;
    chomp($name);
    print "Hello, ", $name, "!\n";


Comparison Operator


+-------------------+------------------------+
| String Operator   | Numerical Operator     |
+===================+========================+
| eq                | ==                     |
+-------------------+------------------------+
| ne                | !=                     |
+-------------------+------------------------+
| gt                | >                      |
+-------------------+------------------------+
| lt                | <                      |
+-------------------+------------------------+
| ge                | >=                     |
+-------------------+------------------------+
| le                | <=                     |
+-------------------+------------------------+

True Expressions vs False Expression

In Perl every expression is considered **true** except for the following three cases:

1. The number 0.
2. The empty string ("").
3. A special value called undef. This is the default value of every variable that was not initialized before it was accessed.

Statement

1. ``if () {} elseif () {} else {}``
2. ``while () {}``
3. ``last``, ``next``
4. ``for(row = 1 ; $row <= 10; $row++) { }``

Variables

* ``$x`` - variable
* ``@array`` - array. 
    - ``scalar(@myarray)``: refer to the number of elements in myarray
    - ``$#myarray``: is equal to the maximal index itself (or -1 if the array is empty)
* ``%hash`` - hash map

Array

* ``$myarray[-$n]`` is equivalent to ``$myarray[scalar(@myarray)-$n]``.
* ``push``, ``pop``, ``shift``, ``join``, ``reverse``

Hash

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

* ``open my $my_file_handle, $mode, $file_path;``
* ``close($my_file_handle);``

``$mode``

+----------------+----------------------------------------------------------+
|>               |Writing (the original file will be erased before          | 
|                |the function starts).                                     | 
+----------------+----------------------------------------------------------+
|< (or nothing)  |Reading                                                   |
|                |                                                          |
+----------------+----------------------------------------------------------+
|>>              |Appending (the file pointer will start at the end         |
|                |and the file will not be overridden)                      |
+----------------+----------------------------------------------------------+
|+<              |Read-write, or just write without truncating.             |
+----------------+----------------------------------------------------------+


Regular Expression

* The ``"."`` stands for any character
* The ``[ ... ]`` specifies more than one option for a character
* ``(?: ... )`` cluster grouping notation
* ``( ... )`` capture grouping notation
* Binding operator ``=~`` tells Perl to match the pattern on the right against the string on the left, instead of matching against ``$_``.
* ``m//``: match as being like word processor's "search" feature.
* ``s///``: the operator simply replaces whatever part of a variable matches the pattern with a replacement string.

* ``$&``: the part of the string that actually matched the pattern is automatically stored in ``$&``.
* ``$```: whatever came before the matched section in $& is in ``$```
* ``$'``: whatever came after the matched section in $& is in ``$'``
* ``${^PREMATCH}``, ``${^MATCH}`` and ``${^POSTMATCH}``

.. code-block:: perl

    if ("Hello there, neighbor" =~ /\s(\w+),/) {
        print "That actually matched '$&'.\n";
    }
    # $` is "Hello"
    # $& is " there,"
    # $' is " neighbor"

* Named Captures (?<LABEL>PATTERN), $+
  
.. code-block:: perl

    my $names = 'Fred or Barney';
    if ( $names =~ m/(?<name1>\w+) (?:and|or) (?<name2>\w+)/ ) {
        say "I saw $+{name1} and $+{name2}";
    }




Modifier

* **``/g``**: the modifier tells s/// to make all possible non-overlapping replacements.
* **``/i``**: Case-insensitive matching
* **``/s``**: make . match any character
* **``/e``**: tells s/// the right side is treated as a normal Perl expression, giving you the ability to use operators and functions.

.. code-block:: perl

    $string =~ s/^([A-Za-z]+)/length($1)/e;






.. author:: default
.. categories:: none
.. tags:: none
.. comments::
