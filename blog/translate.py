import os

from js2py import get_file_contents, translate_js, translate_js6, write_file_contents

def translate_file(input_path, output_path):
    js = get_file_contents(input_path)

    py_code = translate_js6(js)
    lib_name = os.path.basename(output_path).split('.')[0]
    head = '__all__ = [%s]\n\n# Don\'t look below, you will not understand this Python code :) I don\'t.\n\n' % repr(
        lib_name)
    tail = '\n\n# Add lib to the module scope\n%s = var.to_python()' % lib_name
    out = head + py_code + tail
    write_file_contents(output_path, out)


try:
    bn = f'translate/blog-split'
    print(bn)
    translate_file(bn+'.js', bn+'.py')
except:
    pass
