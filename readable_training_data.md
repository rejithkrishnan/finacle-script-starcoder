# Finacle Training Data Set

This document contains 146 examples used for fine-tuning the model.

## Example 1

### Prompt

> Create a simple Finacle script that prints 'Hello World'.

### Expected Script

```bash
<--start
# This is a comment
print("Hello World")
end-->
```

---

## Example 2

### Prompt

> Assign the number 100 to scratchpad variable sv_a and print it.

### Expected Script

```bash
<--start
sv_a = 100
print(sv_a)
end-->
```

---

## Example 3

### Prompt

> Assign the string 'Finacle' to a local variable lv_b and print it.

### Expected Script

```bash
<--start
lv_b = "Finacle"
print(lv_b)
end-->
```

---

## Example 4

### Prompt

> Add the numbers 55 and 45 and store the result in sv_c.

### Expected Script

```bash
<--start
sv_a = 55
sv_b = 45
sv_c = sv_a + sv_b
print(sv_c)
end-->
```

---

## Example 5

### Prompt

> Subtract 25 from 75 and print the output.

### Expected Script

```bash
<--start
sv_x = 75
sv_y = 25
sv_z = sv_x - sv_y
print(sv_z)
end-->
```

---

## Example 6

### Prompt

> Multiply 12 by 10 and display the result.

### Expected Script

```bash
<--start
sv_m = 12
sv_n = 10
sv_result = sv_m * sv_n
print(sv_result)
end-->
```

---

## Example 7

### Prompt

> Divide 100 by 4 and show the result.

### Expected Script

```bash
<--start
sv_p = 100
sv_q = 4
sv_r = sv_p / sv_q
print(sv_r)
end-->
```

---

## Example 8

### Prompt

> Concatenate the strings 'Core' and 'Banking' with a space in between.

### Expected Script

```bash
<--start
sv_str1 = "Core"
sv_str2 = "Banking"
sv_full = sv_str1 + " " + sv_str2
print(sv_full)
end-->
```

---

## Example 9

### Prompt

> Check if sv_a is equal to 50. If so, print 'Equal'.

### Expected Script

```bash
<--start
sv_a = 50
if (sv_a == 50) then
  print("Equal")
endif
end-->
```

---

## Example 10

### Prompt

> If variable sv_b is not equal to 'TEST', print 'Not Equal'.

### Expected Script

```bash
<--start
sv_b = "PROD"
if (sv_b != "TEST") then
  print("Not Equal")
endif
end-->
```

---

## Example 11

### Prompt

> If sv_c is greater than 100, print 'Greater', otherwise print 'Not Greater'.

### Expected Script

```bash
<--start
sv_c = 101
if (sv_c > 100) then
  print("Greater")
else
  print("Not Greater")
endif
end-->
```

---

## Example 12

### Prompt

> Check if sv_d is less than or equal to 5. If it is, print 'OK'.

### Expected Script

```bash
<--start
sv_d = 5
if (sv_d <= 5) then
  print("OK")
endif
end-->
```

---

## Example 13

### Prompt

> If sv_a is 'Y' AND sv_b is 'ACTIVE', print 'Proceed'.

### Expected Script

```bash
<--start
sv_a = "Y"
sv_b = "ACTIVE"
if ((sv_a == "Y") AND (sv_b == "ACTIVE")) then
  print("Proceed")
endif
end-->
```

---

## Example 14

### Prompt

> If sv_status is 'CLOSED' OR sv_status is 'LOCKED', print 'Action Required'.

### Expected Script

```bash
<--start
sv_status = "CLOSED"
if ((sv_status == "CLOSED") OR (sv_status == "LOCKED")) then
  print("Action Required")
endif
end-->
```

---

## Example 15

### Prompt

> Use a while loop to print numbers from 1 to 3.

### Expected Script

```bash
<--start
lv_a = 1
while (lv_a <= 3)
do
  print(lv_a)
  lv_a = lv_a + 1
endwhile
end-->
```

---

## Example 16

### Prompt

> Use the unary minus operator to make the number 10 negative.

### Expected Script

```bash
<--start
sv_a = 10
sv_b = -sv_a
print(sv_b)
end-->
```

---

## Example 17

### Prompt

> Jump to a label named 'skip_section' using GOTO.

### Expected Script

```bash
<--start
print("Part 1")
GOTO skip_section
print("This should not be printed")
skip_section:
print("Part 2")
end-->
```

---

## Example 18

### Prompt

> Call a subroutine named 'print_routine' using GOSUB and then exit.

### Expected Script

```bash
<--start
GOSUB print_routine
EXITSCRIPT
print_routine:
  print("Inside subroutine")
  RETURN
end-->
```

---

## Example 19

### Prompt

> Call another script named 'child_script.scr'.

### Expected Script

```bash
<--start
print("Calling another script...")
CALL("child_script.scr")
print("Returned from child script.")
end-->
```

---

## Example 20

### Prompt

> Start execution of a script named 'new_process.scr' and do not return.

### Expected Script

```bash
<--start
print("Starting new process...")
START("new_process.scr")
# This line will not be reached
end-->
```

---

## Example 21

### Prompt

> Extract 'abc' from the string 'xyzabcdef' using MID$.

### Expected Script

```bash
<--start
sv_s = "xyzabcdef"
sv_sub = Mid$(sv_s, 3, 3)
print(sv_sub)
end-->
```

---

## Example 22

### Prompt

> Get the first 4 characters of the string 'FinacleCore'.

### Expected Script

```bash
<--start
sv_s = "FinacleCore"
sv_left = Left$(sv_s, 4)
print(sv_left)
end-->
```

---

## Example 23

### Prompt

> Get the last 4 characters of 'FinacleCore'.

### Expected Script

```bash
<--start
sv_s = "FinacleCore"
sv_right = Right$(sv_s, 4)
print(sv_right)
end-->
```

---

## Example 24

### Prompt

> Convert the string '123.45' to a double and print it.

### Expected Script

```bash
<--start
sv_a = CDOUBLE("123.45")
print(sv_a)
end-->
```

---

## Example 25

### Prompt

> Convert the string '987' to an integer.

### Expected Script

```bash
<--start
sv_a = CINT("987")
print(sv_a)
end-->
```

---

## Example 26

### Prompt

> Convert the string 'HeLLo' to all lowercase.

### Expected Script

```bash
<--start
sv_a = TOLOWER("HeLLo")
print(sv_a)
end-->
```

---

## Example 27

### Prompt

> Convert 'world' to all uppercase.

### Expected Script

```bash
<--start
sv_a = TOUPPER("world")
print(sv_a)
end-->
```

---

## Example 28

### Prompt

> Find the length of the string 'Extensibility'.

### Expected Script

```bash
<--start
sv_len = STRLEN("Extensibility")
print(sv_len)
end-->
```

---

## Example 29

### Prompt

> Get the character at position 5 in the string 'Finacle Scripting'.

### Expected Script

```bash
<--start
sv_char = CHARAT("Finacle Scripting", 5)
print(sv_char)
end-->
```

---

## Example 30

### Prompt

> Remove leading spaces from the string '  indented'.

### Expected Script

```bash
<--start
sv_a = "  indented"
sv_b = LTRIM(sv_a)
print(sv_b)
end-->
```

---

## Example 31

### Prompt

> Remove trailing spaces from 'padded   '.

### Expected Script

```bash
<--start
sv_a = "padded   "
sv_b = RTRIM(sv_a)
print(sv_b)
end-->
```

---

## Example 32

### Prompt

> Remove both leading and trailing asterisks from '***TRIMMED***'.

### Expected Script

```bash
<--start
sv_a = "***TRIMMED***"
sv_b = TRIM(sv_a, "*")
print(sv_b)
end-->
```

---

## Example 33

### Prompt

> Left-pad the string 'ID' with zeros to a total length of 8.

### Expected Script

```bash
<--start
sv_a = "ID"
sv_b = LPAD(sv_a, 8, "0")
print(sv_b)
end-->
```

---

## Example 34

### Prompt

> Right-pad the string 'User' with '#' to a total length of 10.

### Expected Script

```bash
<--start
sv_a = "User"
sv_b = RPAD(sv_a, 10, "#")
print(sv_b)
end-->
```

---

## Example 35

### Prompt

> Check if a repository named 'GLOBAL' exists.

### Expected Script

```bash
<--start
sv_exists = REPEXISTS("GLOBAL")
if (sv_exists == 1) then
  print("Repository exists.")
else
  print("Repository does not exist.")
endif
end-->
```

---

## Example 36

### Prompt

> Check if a class named 'INPUT' exists in the 'BANCS' repository.

### Expected Script

```bash
<--start
sv_exists = CLASSEXISTS("BANCS", "INPUT")
if (sv_exists == 1) then
  print("Class exists.")
endif
end-->
```

---

## Example 37

### Prompt

> Check if the field 'userId' exists in 'BANCS.STDIN'.

### Expected Script

```bash
<--start
sv_exists = FIELDEXISTS(BANCS.STDIN.userId)
if (sv_exists == 1) then
  print("Field exists.")
endif
end-->
```

---

## Example 38

### Prompt

> Create a temporary repository named 'MY_TEMP_REP'.

### Expected Script

```bash
<--start
CREATEREP("MY_TEMP_REP")
print("Repository created.")
end-->
```

---

## Example 39

### Prompt

> Create a STRING class named 'DATA' in the 'MY_TEMP_REP' repository.

### Expected Script

```bash
<--start
# Assumes MY_TEMP_REP exists
# 5 is the type for STRING
CREATECLASS("MY_TEMP_REP", "DATA", 5)
print("Class created.")
end-->
```

---

## Example 40

### Prompt

> Delete the temporary class 'DATA' from the 'MY_TEMP_REP' repository.

### Expected Script

```bash
<--start
DELETECLASS("MY_TEMP_REP", "DATA")
print("Class deleted.")
end-->
```

---

## Example 41

### Prompt

> Delete the temporary repository 'MY_TEMP_REP'.

### Expected Script

```bash
<--start
DELETEREP("MY_TEMP_REP")
print("Repository deleted.")
end-->
```

---

## Example 42

### Prompt

> Assign the value 'test_user' to the repository field BANCS.INPUT.user.

### Expected Script

```bash
<--start
BANCS.INPUT.user = "test_user"
print(BANCS.INPUT.user)
end-->
```

---

## Example 43

### Prompt

> Copy the value from repository field BANCS.STDIN.userId to sv_a.

### Expected Script

```bash
<--start
# This assumes the field has a value
sv_a = BANCS.STDIN.userId
print(sv_a)
end-->
```

---

## Example 44

### Prompt

> Set the script return status to Failure.

### Expected Script

```bash
<--start
BANCS.OUTPUT.successOrFailure = "F"
end-->
```

---

## Example 45

### Prompt

> Set the script return status to Success.

### Expected Script

```bash
<--start
BANCS.OUTPUT.successOrFailure = "S"
end-->
```

---

## Example 46

### Prompt

> Turn on script tracing.

### Expected Script

```bash
<--start
TRACE ON
print("Tracing is now active.")
end-->
```

---

## Example 47

### Prompt

> Turn off script tracing.

### Expected Script

```bash
<--start
TRACE OFF
print("Tracing is now inactive.")
end-->
```

---

## Example 48

### Prompt

> Exit the current script immediately.

### Expected Script

```bash
<--start
print("About to exit...")
EXITSCRIPT
print("This will not be printed.")
end-->
```

---

## Example 49

### Prompt

> Call a user hook function named 'VALIDATE_USER'.

### Expected Script

```bash
<--start
sv_a = URHK_VALIDATE_USER("some_input_data")
if (sv_a == 0) then
  print("User hook successful.")
else
  print("User hook failed.")
endif
end-->
```

---

## Example 50

### Prompt

> Call a user routine 'CalculateInterest' from the default library.

### Expected Script

```bash
<--start
sv_a = URTN_CalculateInterest("account_data")
print(sv_a)
end-->
```

---

## Example 51

### Prompt

> Set a library name to 'CUSTOM.DLL' for user routines.

### Expected Script

```bash
<--start
LIBNAME "CUSTOM.DLL"
sv_a = URTN_CustomRoutine("data")
print(sv_a)
end-->
```

---

## Example 52

### Prompt

> Find the position of 'script' in 'Finacle scripting language'.

### Expected Script

```bash
<--start
sv_pos = GETPOSITION("Finacle scripting language", "script")
print(sv_pos)
end-->
```

---

## Example 53

### Prompt

> Do a case-insensitive search for 'FINACLE' in 'Welcome to Finacle'.

### Expected Script

```bash
<--start
sv_pos = GETIPOSITION("Welcome to Finacle", "FINACLE")
print(sv_pos)
end-->
```

---

## Example 54

### Prompt

> Compare the strings 'Hello' and 'hello' without case sensitivity.

### Expected Script

```bash
<--start
sv_result = STRICMP("Hello", "hello")
if (sv_result == 1) then
  print("Strings are the same, ignoring case.")
endif
end-->
```

---

## Example 55

### Prompt

> Assign 12 to sv_a, 20 to sv_b. Check if sv_a is less than sv_b.

### Expected Script

```bash
<--start
sv_a = 12
sv_b = 20
if (sv_a < sv_b) then
  print("sv_a is less than sv_b")
endif
end-->
```

---

## Example 56

### Prompt

> Check if sv_x is greater than or equal to 100.

### Expected Script

```bash
<--start
sv_x = 100
if (sv_x >= 100) then
  print("sv_x is 100 or more.")
endif
end-->
```

---

## Example 57

### Prompt

> Loop while a counter lv_i is less than 5, incrementing it each time.

### Expected Script

```bash
<--start
lv_i = 0
while (lv_i < 5)
do
  print(lv_i)
  lv_i = lv_i + 1
endwhile
end-->
```

---

## Example 58

### Prompt

> If BANCS.INPUT.acct_type is 'SBA' or 'CAA', print 'Operative Account'.

### Expected Script

```bash
<--start
# Assuming BANCS.INPUT.acct_type is set
if ((BANCS.INPUT.acct_type == "SBA") OR (BANCS.INPUT.acct_type == "CAA")) then
  print("Operative Account")
endif
end-->
```

---

## Example 59

### Prompt

> Create an integer class 'COUNTERS' in repository 'SESSION'.

### Expected Script

```bash
<--start
# 1 is the type for INTEGER
CREATEREP("SESSION")
CREATECLASS("SESSION", "COUNTERS", 1)
SESSION.COUNTERS.login_attempts = 0
print(SESSION.COUNTERS.login_attempts)
end-->
```

---

## Example 60

### Prompt

> Create a double class 'BALANCES' in repository 'SESSION'.

### Expected Script

```bash
<--start
# 2 is the type for DOUBLE
CREATEREP("SESSION")
CREATECLASS("SESSION", "BALANCES", 2)
SESSION.BALANCES.min_bal = 100.50
print(SESSION.BALANCES.min_bal)
end-->
```

---

## Example 61

### Prompt

> Find the difference between 500 and 125.

### Expected Script

```bash
<--start
sv_a = 500
sv_b = 125
sv_diff = sv_a - sv_b
print(sv_diff)
end-->
```

---

## Example 62

### Prompt

> Calculate 7 times 8.

### Expected Script

```bash
<--start
sv_a = 7
sv_b = 8
sv_prod = sv_a * sv_b
print(sv_prod)
end-->
```

---

## Example 63

### Prompt

> Divide 99 by 3.

### Expected Script

```bash
<--start
sv_a = 99
sv_b = 3
sv_quotient = sv_a / sv_b
print(sv_quotient)
end-->
```

---

## Example 64

### Prompt

> Add 'Mr. ' to the name 'Stark'.

### Expected Script

```bash
<--start
sv_title = "Mr. "
sv_name = "Stark"
sv_full_name = sv_title + sv_name
print(sv_full_name)
end-->
```

---

## Example 65

### Prompt

> If a local variable lv_flag is 0, print 'Flag is off'.

### Expected Script

```bash
<--start
lv_flag = 0
if (lv_flag == 0) then
  print("Flag is off")
endif
end-->
```

---

## Example 66

### Prompt

> If sv_country is not 'IN', print 'International'.

### Expected Script

```bash
<--start
sv_country = "US"
if (sv_country != "IN") then
  print("International")
endif
end-->
```

---

## Example 67

### Prompt

> If sv_age is greater than 60, print 'Senior'. Else, print 'Not senior'.

### Expected Script

```bash
<--start
sv_age = 65
if (sv_age > 60) then
  print("Senior")
else
  print("Not senior")
endif
end-->
```

---

## Example 68

### Prompt

> If sv_score is less than 50, print 'Fail'.

### Expected Script

```bash
<--start
sv_score = 49
if (sv_score < 50) then
  print("Fail")
endif
end-->
```

---

## Example 69

### Prompt

> If product code is 'A' and region is 'North', print 'Category A-North'.

### Expected Script

```bash
<--start
sv_prod = "A"
sv_region = "North"
if ((sv_prod == "A") AND (sv_region == "North")) then
  print("Category A-North")
endif
end-->
```

---

## Example 70

### Prompt

> If sv_env is 'UAT' or 'SIT', print 'Test Environment'.

### Expected Script

```bash
<--start
sv_env = "UAT"
if ((sv_env == "UAT") OR (sv_env == "SIT")) then
  print("Test Environment")
endif
end-->
```

---

## Example 71

### Prompt

> Use a while loop to print even numbers from 2 to 10.

### Expected Script

```bash
<--start
lv_a = 2
while (lv_a <= 10)
do
  print(lv_a)
  lv_a = lv_a + 2
endwhile
end-->
```

---

## Example 72

### Prompt

> Make sv_b the negative of sv_a, where sv_a is -5.

### Expected Script

```bash
<--start
sv_a = -5
sv_b = -sv_a
print(sv_b)
end-->
```

---

## Example 73

### Prompt

> Extract 'Script' from 'Finacle-Script-Tool' using MID$.

### Expected Script

```bash
<--start
sv_s = "Finacle-Script-Tool"
sv_sub = Mid$(sv_s, 8, 6)
print(sv_sub)
end-->
```

---

## Example 74

### Prompt

> Get the first 7 characters of 'Welcome'.

### Expected Script

```bash
<--start
sv_s = "Welcome"
sv_left = Left$(sv_s, 7)
print(sv_left)
end-->
```

---

## Example 75

### Prompt

> Get the last 3 characters of 'Automation'.

### Expected Script

```bash
<--start
sv_s = "Automation"
sv_right = Right$(sv_s, 3)
print(sv_right)
end-->
```

---

## Example 76

### Prompt

> Convert the string '99.99' to a double data type.

### Expected Script

```bash
<--start
sv_a = CDOUBLE("99.99")
print(sv_a)
end-->
```

---

## Example 77

### Prompt

> Convert '42' from a string to an integer.

### Expected Script

```bash
<--start
sv_a = CINT("42")
print(sv_a)
end-->
```

---

## Example 78

### Prompt

> Convert 'FINACLE' to lowercase.

### Expected Script

```bash
<--start
sv_a = TOLOWER("FINACLE")
print(sv_a)
end-->
```

---

## Example 79

### Prompt

> Convert 'custom' to uppercase.

### Expected Script

```bash
<--start
sv_a = TOUPPER("custom")
print(sv_a)
end-->
```

---

## Example 80

### Prompt

> What is the length of the string 'Repository'?

### Expected Script

```bash
<--start
sv_len = STRLEN("Repository")
print(sv_len)
end-->
```

---

## Example 81

### Prompt

> What is the character at position 0 of 'Script'?

### Expected Script

```bash
<--start
sv_char = CHARAT("Script", 0)
print(sv_char)
end-->
```

---

## Example 82

### Prompt

> Trim leading hyphens from '---data'.

### Expected Script

```bash
<--start
sv_a = "---data"
sv_b = LTRIM(sv_a, "-")
print(sv_b)
end-->
```

---

## Example 83

### Prompt

> Trim trailing slashes from 'path//'.

### Expected Script

```bash
<--start
sv_a = "path//"
sv_b = RTRIM(sv_a, "/")
print(sv_b)
end-->
```

---

## Example 84

### Prompt

> Remove leading and trailing spaces from '  padded string  '.

### Expected Script

```bash
<--start
sv_a = "  padded string  "
sv_b = TRIM(sv_a)
print(sv_b)
end-->
```

---

## Example 85

### Prompt

> Left-pad 'Go' with '>' to a length of 5.

### Expected Script

```bash
<--start
sv_a = "Go"
sv_b = LPAD(sv_a, 5, ">")
print(sv_b)
end-->
```

---

## Example 86

### Prompt

> Right-pad 'End' with '<' to a length of 6.

### Expected Script

```bash
<--start
sv_a = "End"
sv_b = RPAD(sv_a, 6, "<")
print(sv_b)
end-->
```

---

## Example 87

### Prompt

> If repository 'USER_REP' does not exist, create it.

### Expected Script

```bash
<--start
if (REPEXISTS("USER_REP") == 0) then
  CREATEREP("USER_REP")
  print("Repository Created.")
endif
end-->
```

---

## Example 88

### Prompt

> If class 'PREFS' does not exist in 'USER_REP', create it as a STRING class.

### Expected Script

```bash
<--start
# Assumes USER_REP exists
if (CLASSEXISTS("USER_REP", "PREFS") == 0) then
  CREATECLASS("USER_REP", "PREFS", 5)
  print("Class Created.")
endif
end-->
```

---

## Example 89

### Prompt

> If field 'theme' does not exist in USER_REP.PREFS, create and set it to 'dark'.

### Expected Script

```bash
<--start
if (FIELDEXISTS(USER_REP.PREFS.theme) == 0) then
  USER_REP.PREFS.theme = "dark"
  print(USER_REP.PREFS.theme)
endif
end-->
```

---

## Example 90

### Prompt

> Assign an integer value 2025 to the repository field CONFIG.SYSTEM.year.

### Expected Script

```bash
<--start
# Assumes CONFIG.SYSTEM is an INTEGER class
CONFIG.SYSTEM.year = 2025
print(CONFIG.SYSTEM.year)
end-->
```

---

## Example 91

### Prompt

> Read the value of the 'onlineOrBatch' field from the 'BANCS.STDIN' repository into a variable.

### Expected Script

```bash
<--start
sv_mode = BANCS.STDIN.onlineOrBatch
print(sv_mode)
end-->
```

---

## Example 92

### Prompt

> Write a nested if statement. If sv_a > 10, then check if sv_b > 20.

### Expected Script

```bash
<--start
sv_a = 11
sv_b = 21
if (sv_a > 10) then
  print("sv_a is greater than 10")
  if (sv_b > 20) then
    print("sv_b is also greater than 20")
  endif
endif
end-->
```

---

## Example 93

### Prompt

> Use GOSUB inside an if condition to call a subroutine.

### Expected Script

```bash
<--start
sv_a = 1
if (sv_a == 1) THEN
  GOSUB sub1
ENDIF
EXITSCRIPT
sub1:
  print("In subroutine 1")
  RETURN
end-->
```

---

## Example 94

### Prompt

> Dynamically change the type of sv_a from an integer to a string.

### Expected Script

```bash
<--start
sv_a = 12345
print("sv_a is an integer now.")
sv_a = "Hello"
print("sv_a is a string now.")
end-->
```

---

## Example 95

### Prompt

> Call a user hook named 'FETCH_CUST_DATA' and check the return value.

### Expected Script

```bash
<--start
sv_ret = URHK_FETCH_CUST_DATA("cif_id_123")
if (sv_ret == 0) then
  print("Fetch successful")
else
  print("Fetch failed")
endif
end-->
```

---

## Example 96

### Prompt

> Calculate 15 plus 30 minus 10.

### Expected Script

```bash
<--start
sv_result = 15 + 30 - 10
print(sv_result)
end-->
```

---

## Example 97

### Prompt

> Create a script to find the difference between 99 and 44.

### Expected Script

```bash
<--start
sv_val1 = 99
sv_val2 = 44
sv_result = sv_val1 - sv_val2
print(sv_result)
end-->
```

---

## Example 98

### Prompt

> Calculate 3 multiplied by 4 plus 5.

### Expected Script

```bash
<--start
sv_a = 3
sv_b = 4
sv_c = 5
sv_result = sv_a * sv_b + sv_c
print(sv_result)
end-->
```

---

## Example 99

### Prompt

> Check if a string 'test' is equal to 'test'.

### Expected Script

```bash
<--start
if ("test" == "test") then
  print("Strings are equal")
endif
end-->
```

---

## Example 100

### Prompt

> Loop from 10 down to 1 and print each number.

### Expected Script

```bash
<--start
lv_i = 10
while (lv_i > 0)
do
  print(lv_i)
  lv_i = lv_i - 1
endwhile
end-->
```

---

## Example 101

### Prompt

> Check if BANCS.INPUT.value is empty. If it is, set success to 'F'.

### Expected Script

```bash
<--start
if (BANCS.INPUT.value == "") then
  BANCS.OUTPUT.successOrFailure = "F"
else
  BANCS.OUTPUT.successOrFailure = "S"
endif
end-->
```

---

## Example 102

### Prompt

> Replace the middle 2 characters of '123456' with 'XX' using SET$.

### Expected Script

```bash
<--start
sv_a = "123456"
sv_b = SET$(sv_a, 2, 2, "XX")
print(sv_b)
end-->
```

---

## Example 103

### Prompt

> Format the number 12.345 to two decimal places.

### Expected Script

```bash
<--start
sv_a = 12.345
sv_b = FORMAT$(sv_a, "%.2f")
print(sv_b)
end-->
```

---

## Example 104

### Prompt

> Create a temporary repository 'LOGS', a string class 'MESSAGES', and add a field 'error1' with value 'File not found'.

### Expected Script

```bash
<--start
CREATEREP("LOGS")
CREATECLASS("LOGS", "MESSAGES", 5)
LOGS.MESSAGES.error1 = "File not found"
print(LOGS.MESSAGES.error1)
end-->
```

---

## Example 105

### Prompt

> In a loop, if the counter is 5, use GOTO to jump to the end.

### Expected Script

```bash
<--start
lv_i = 0
while (lv_i < 10)
do
  if (lv_i == 5) then
    GOTO end_loop
  endif
  print(lv_i)
  lv_i = lv_i + 1
endwhile
end_loop:
print("Loop finished.")
end-->
```

---

## Example 106

### Prompt

> What is 200 minus 75?

### Expected Script

```bash
<--start
sv_a = 200
sv_b = 75
sv_c = sv_a - sv_b
print(sv_c)
end-->
```

---

## Example 107

### Prompt

> How do you represent 1500 multiplied by 2?

### Expected Script

```bash
<--start
sv_a = 1500
sv_b = 2
sv_c = sv_a * sv_b
print(sv_c)
end-->
```

---

## Example 108

### Prompt

> Find the sum of 1, 2, 3, 4, and 5 using a loop.

### Expected Script

```bash
<--start
lv_sum = 0
lv_i = 1
while (lv_i <= 5)
do
  lv_sum = lv_sum + lv_i
  lv_i = lv_i + 1
endwhile
print(lv_sum)
end-->
```

---

## Example 109

### Prompt

> If a string sv_a is longer than 10 characters, print 'Too long'.

### Expected Script

```bash
<--start
sv_a = "This is a very long string"
if (STRLEN(sv_a) > 10) then
  print("Too long")
endif
end-->
```

---

## Example 110

### Prompt

> Read the home currency code into a variable.

### Expected Script

```bash
<--start
sv_home_ccy = BANCS.STDIN.homeCrncyCode
print(sv_home_ccy)
end-->
```

---

## Example 111

### Prompt

> Check if the current menu option is 'HACLI'.

### Expected Script

```bash
<--start
if (BANCS.STDIN.menuOption == "HACLI") then
  print("Customer Inquiry Menu")
endif
end-->
```

---

## Example 112

### Prompt

> Add a string to the HTML output buffer.

### Expected Script

```bash
<--start
AddToHTML("<h1>Welcome User</h1>")
end-->
```

---

## Example 113

### Prompt

> Execute an external program 'validate.exe' with argument 'data.xml'.

### Expected Script

```bash
<--start
sv_ret = UREX("validate.exe", "returndata.tmp", "data.xml")
print(sv_ret)
end-->
```

---

## Example 114

### Prompt

> If lv_a is not 1 and not 2, print 'Other'.

### Expected Script

```bash
<--start
lv_a = 3
if ((lv_a != 1) AND (lv_a != 2)) then
  print("Other")
endif
end-->
```

---

## Example 115

### Prompt

> Combine 'Hello' and 123 into a single string.

### Expected Script

```bash
<--start
sv_a = "Hello"
sv_b = 123
sv_c = sv_a + sv_b
print(sv_c)
end-->
```

---

## Example 116

### Prompt

> Create a float class 'RATES' and add a field 'tax_rate'.

### Expected Script

```bash
<--start
# 3 is the type for FLOAT
CREATEREP("CONFIG")
CREATECLASS("CONFIG", "RATES", 3)
CONFIG.RATES.tax_rate = 0.15
print(CONFIG.RATES.tax_rate)
end-->
```

---

## Example 117

### Prompt

> Write a script that does nothing but has a start and end tag.

### Expected Script

```bash
<--start
# This script is empty.
end-->
```

---

## Example 118

### Prompt

> Set a variable to the result of 100/5.

### Expected Script

```bash
<--start
sv_a = 100/5
print(sv_a)
end-->
```

---

## Example 119

### Prompt

> In a loop from 1 to 10, print 'Five' when the counter hits 5.

### Expected Script

```bash
<--start
lv_i = 1
while (lv_i <= 10)
do
  if (lv_i == 5) then
    print("Five")
  else
    print(lv_i)
  endif
  lv_i = lv_i + 1
endwhile
end-->
```

---

## Example 120

### Prompt

> What is the result of 10 minus 20?

### Expected Script

```bash
<--start
sv_a = 10
sv_b = 20
sv_c = sv_a - sv_b
print(sv_c)
end-->
```

---

## Example 121

### Prompt

> Take the string 'abcde', get the middle character 'c'.

### Expected Script

```bash
<--start
sv_a = "abcde"
sv_b = Mid$(sv_a, 2, 1)
print(sv_b)
end-->
```

---

## Example 122

### Prompt

> Check if BANCS.STDIN.WFflg is equal to 'Y'.

### Expected Script

```bash
<--start
# Checks if script is a workflow script
if (BANCS.STDIN.WFflg == "Y") then
  print("This is a workflow script.")
endif
end-->
```

---

## Example 123

### Prompt

> Use PUTREPFIELD to set the value of a field named 'MY_REP.MY_CLASS.MY_FIELD'.

### Expected Script

```bash
<--start
CREATEREP("MY_REP")
CREATECLASS("MY_REP", "MY_CLASS", 5)
sv_a = "MY_REP.MY_CLASS.MY_FIELD"
sv_b = "My Value"
PUTREPFIELD(sv_a, sv_b)
end-->
```

---

## Example 124

### Prompt

> Use GETREPFIELD to retrieve the value of 'MY_REP.MY_CLASS.MY_FIELD'.

### Expected Script

```bash
<--start
# Assumes the field was set previously
sv_a = "MY_REP.MY_CLASS.MY_FIELD"
sv_b = GETREPFIELD(sv_a)
print(sv_b)
end-->
```

---

## Example 125

### Prompt

> Write a script to check if 25 is greater than 15.

### Expected Script

```bash
<--start
if (25 > 15) then
  print("Yes, 25 is greater.")
endif
end-->
```

---

## Example 126

### Prompt

> Take the number 50 and subtract 5.

### Expected Script

```bash
<--start
sv_a = 50 - 5
print(sv_a)
end-->
```

---

## Example 127

### Prompt

> Print the current system date from the BANCS.STDIN repository.

### Expected Script

```bash
<--start
sv_date = BANCS.STDIN.sysDate
print(sv_date)
end-->
```

---

## Example 128

### Prompt

> Format an account number by taking the last 4 digits of '12345678' and prefixing with 'ACC-'.

### Expected Script

```bash
<--start
sv_full_num = "12345678"
sv_last_four = Right$(sv_full_num, 4)
sv_formatted = "ACC-" + sv_last_four
print(sv_formatted)
end-->
```

---

## Example 129

### Prompt

> If input value in BANCS.INPUT.amount is less than 1000 and the transaction type is 'CASH', set a flag.

### Expected Script

```bash
<--start
lv_flag = 0
if ((CINT(BANCS.INPUT.amount) < 1000) AND (BANCS.INPUT.tranType == "CASH")) then
  lv_flag = 1
endif
print(lv_flag)
end-->
```

---

## Example 130

### Prompt

> Create a character class and store the character 'A'.

### Expected Script

```bash
<--start
# 4 is the type for CHAR
CREATEREP("TEMP")
CREATECLASS("TEMP", "CHARS", 4)
TEMP.CHARS.myChar = 'A'
print(TEMP.CHARS.myChar)
end-->
```

---

## Example 131

### Prompt

> Use a subroutine to add two numbers.

### Expected Script

```bash
<--start
sv_x = 10
sv_y = 20
GOSUB add_routine
print(sv_z)
EXITSCRIPT
add_routine:
  sv_z = sv_x + sv_y
  RETURN
end-->
```

---

## Example 132

### Prompt

> If sv_a is 1, print 'One'. If it's 2, print 'Two'. Otherwise, print 'Other'.

### Expected Script

```bash
<--start
sv_a = 2
if (sv_a == 1) then
  print("One")
else
  if (sv_a == 2) then
    print("Two")
  else
    print("Other")
  endif
endif
end-->
```

---

## Example 133

### Prompt

> Find the result of (10 + 5) * 2.

### Expected Script

```bash
<--start
sv_result = (10 + 5) * 2
print(sv_result)
end-->
```

---

## Example 134

### Prompt

> Print the description of the current service outlet (SOL).

### Expected Script

```bash
<--start
sv_sol_desc = BANCS.STDIN.mySolDesc
print(sv_sol_desc)
end-->
```

---

## Example 135

### Prompt

> Demonstrate a simple GOTO loop that prints 3 times.

### Expected Script

```bash
<--start
sv_a = 3
loop_start:
if (sv_a == 0) then
  GOTO loop_end
endif
print(sv_a)
sv_a = sv_a - 1
GOTO loop_start
loop_end:
end-->
```

---

## Example 136

### Prompt

> If sv_a is not null, process it. (Check for empty string)

### Expected Script

```bash
<--start
sv_a = "some data"
if (sv_a != "") then
  print("Processing data...")
endif
end-->
```

---

## Example 137

### Prompt

> Pad the number 123 with leading zeros to make it 5 digits long.

### Expected Script

```bash
<--start
sv_a = 123
sv_b = LPAD(sv_a, 5, "0")
print(sv_b)
end-->
```

---

## Example 138

### Prompt

> Convert a char 'c' to a string.

### Expected Script

```bash
<--start
sv_a = 'c'
sv_b = GETSTRING(sv_a)
print(sv_b)
end-->
```

---

## Example 139

### Prompt

> Create a script that calculates 1000 minus 1.

### Expected Script

```bash
<--start
sv_a = 1000 - 1
print(sv_a)
end-->
```

---

## Example 140

### Prompt

> Assign 25 to sv_a. Check if sv_a is less than 30 OR greater than 20.

### Expected Script

```bash
<--start
sv_a = 25
if ((sv_a < 30) OR (sv_a > 20)) then
  print("Condition met.")
endif
end-->
```

---

## Example 141

### Prompt

> What is 50 divided by 2, plus 10?

### Expected Script

```bash
<--start
sv_result = 50 / 2 + 10
print(sv_result)
end-->
```

---

## Example 142

### Prompt

> Check if the length of 'Hello' is 5.

### Expected Script

```bash
<--start
if (STRLEN("Hello") == 5) then
  print("Length is 5.")
endif
end-->
```

---

## Example 143

### Prompt

> Take the uppercase of 'test' and compare it to 'TEST'.

### Expected Script

```bash
<--start
sv_a = TOUPPER("test")
if (sv_a == "TEST") then
  print("Match")
endif
end-->
```

---

## Example 144

### Prompt

> Show me a script that does a subtraction: 42 minus 12.

### Expected Script

```bash
<--start
sv_a = 42
sv_b = 12
sv_c = sv_a - sv_b
print(sv_c)
end-->
```

---

## Example 145

### Prompt

> Calculate 33 - 11 and print the value.

### Expected Script

```bash
<--start
lv_a = 33
lv_b = 11
lv_c = lv_a - lv_b
print(lv_c)
end-->
```

---

## Example 146

### Prompt

> Give me the result of 77 subtracted by 7.

### Expected Script

```bash
<--start
sv_result = 77 - 7
print(sv_result)
end-->
```

---

