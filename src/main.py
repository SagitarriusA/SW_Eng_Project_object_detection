import os


if __name__ == "__main__":
    image_name = 'test_image_00.png'
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(script_dir, '../images', image_name))

    # Check if the path exists
    if os.path.exists(path):
        print(f'Path is valid: {path}')
    else:
        print(f'Path does not exist: {path}')
