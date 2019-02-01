Function Initialize() Uint64
10  STORE("number",10)
20 RETURN 0 
End Function 

Function ChangeValue(new_val Uint64) Uint64
30  STORE("number",new_val)
50  RETURN 0
END FUNCTION

Function Print() Uint64
5   DIM value as Uint64
10  LET value = LOAD("number")
15   printf "%d asdffdsa" value
20  RETURN 1
END FUNCTION
