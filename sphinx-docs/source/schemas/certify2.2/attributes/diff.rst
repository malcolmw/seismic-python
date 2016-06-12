.. _certify2.2-diff_attributes:

**diff** -- command to check the results of execution
-----------------------------------------------------

This command is executed after the test to check for
validity of the results.  If this is not specified,
the default test is to compare results/testid with
correct/testid.  For convenience, the following
substitutions are performed before the test is
executed:

%r        results/testid
%R  results/testid/testid
%c        correct/testid
%C  correct/testid/testid

* **Field width:** 150
* **Format:** %-150s
