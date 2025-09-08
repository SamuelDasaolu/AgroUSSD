from interfaces import main_menu
while True:
    code = input("Enter AgroUSSD Code (*556#): ").strip()
    if code != "*556#":
     print("Invalid Code")
    else:
       print("Access Granted")
       main_menu()
      



