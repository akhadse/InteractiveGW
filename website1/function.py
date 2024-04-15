# Define your function here
def generate_video_for_varying_param(form_data):
    # Process the input parameter here (Example function)
    for x in form_data:
        print(x)
        print(form_data.get(x))
        print(type(form_data.get(x)))
        print('-------------------------------------------- \n')
        
    output = "Done!!!!"
    
    return output