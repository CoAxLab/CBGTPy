def choose_pipeline(choice):
    global par
    if choice == 'plastic':
        import init_params_direct_indirect as par
    if choice == 'stopsignal':
        import init_params_hyperdirect as par
        
def getpar():
    return par