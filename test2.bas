
Function Initialize() Uint64
10  STORE("number",10)
11  STORE("string1","hello")
12  STORE("string2","world")
20 RETURN 0 
End Function 

Function ChangeValue(new_val1 Uint64,new_val2 Uint64) Uint64
30  STORE("number",new_val1*new_val2)
50  RETURN 0
END FUNCTION

Function DepositAndChangeValue(new_val1 Uint64,value Uint64,new_val2 Uint64) Uint64
30  STORE("number",new_val1*new_val2)
50  RETURN 0
END FUNCTION

Function DepositAndChangeValueAndStrings(new_val1 Uint64,value Uint64,new_val2 Uint64,new_str1 String, new_str2 String) Uint64
30  STORE("number",new_val1*new_val2)
35  STORE("string1",new_str1)
40  STORE("string2",new_str2)
50  RETURN 0
END FUNCTION

Function Withdraw(new_val1 Uint64,amount Uint64,new_val2 Uint64) Uint64
30  STORE("number",new_val1*new_val2)
40  SEND_DERO_TO_ADDRESS(SIGNER(),amount)
50  RETURN 0
END FUNCTION
