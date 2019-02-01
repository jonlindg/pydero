
	Function Initialize() Uint64
    10  STORE("message_count",1)
	20  STORE("message0", "Hello world!")
	30 RETURN 0 
	End Function 
	
    Function Write(text String) Uint64
    5   IF EXISTS(SIGNER())==0 THEN GOTO 60
    10  DIM current_message_count as Uint64
    20  LET current_message_count = LOAD("message_count")
    30  STORE("message"+current_message_count,LOAD(SIGNER())+": "+text)
    40  STORE("message_count",current_message_count+1)
    50  RETURN 0
    60  RETURN 1
    END FUNCTION

    Function Register(name String) Uint64
    5   IF EXISTS(SIGNER())==1 THEN GOTO 40
    6   IF EXISTS(name)==1 THEN GOTO 50
    7   DIM username,signer as String
    8   LET username = name
    9   LET signer = SIGNER()
    10  STORE(SIGNER(),name)
    20  STORE(name,SIGNER())
    25  PRINTF "%s is now associated to username %s" signer username
    30  RETURN 0
    40  PRINTF "This address is already registered"
    45  RETURN 1
    50  PRINTF "This username is already taken"
    55  RETURN 1
    END FUNCTION

    Function Get_number_of_messages() Uint64
    5   DIM message_count as Uint64
    6   LET message_count = LOAD("message_count")
    10  PRINTF "Number of messages: %d" message_count
    20  RETURN 0
    END FUNCTION

    FUNCTION Print_message(n Uint64) Uint64
    5   DIM message as String
    6   LET message = LOAD("message"+n)
    10  PRINTF "%s" message
    20  RETURN 0
    END FUNCTION


	
