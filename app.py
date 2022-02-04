import os

from flask import Flask, render_template, jsonify
import pyknit_methods as pk

# create the application object
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')  # render a template


@app.route('/my-link/')
def my_link():
    entries = {"speed": .65,
               "empty_speed": 1.0,
               "wm32x": 8.5,
               "wm36": 7,
               "wm56": 7.2,
               "wm7": 7.5,
               "wm8": 7.5,
               "wmi": 11,
               "wmi78": 12,
               "front_stitch": 5,
               "back_stitch": 8}

    #Tkinter
    file_path = filedialog.askopenfilename()
    filename = pk.path_leaf(file_path)
    filename = filename[:-4]
    j_txt = pk.JTxt(file_path)
    #Need a form here
    skip = self.skip_reduction_var.get()
    if len(j_txt.colors) < 4:
        skip = 1
    if skip == 1:
        j_txt.reduction_count = 0
    reduced = j_txt.reduce(skip, j_txt.reduction_count)
    #Tkinter
    folder_name = str(askstring("Folder Name", "Name the new folder for this pattern"))
    #Can I use os with flask?
    new_path = os.path.join(os.path.dirname(file_path), folder_name)
    os.makedirs(new_path)
    reduced.save(f"{new_path}/{filename}-birdseye.bmp")
    compressed_txt, __ = j_txt.compress(reduced)
    new_txt_file = open(f"{new_path}/{filename}_J.txt", 'w')
    new_txt_file.write(compressed_txt)
    new_txt_file.close()
    # not sure if this is necessary
    os.chdir('..')
    sheet = pk.make_label(j_txt.colors)
    sheet.save(f"{new_path}/{filename}-color_label.pdf")

    sintral, sintral2x = pk.make_plain_sintral(compressed_txt, entries)
    new_txt_file = open(f"{new_path}/{filename}-sintral440.txt", 'w')
    new_txt_file.write(sintral)
    new_txt_file.close()
    new_txt_file = open(f"{new_path}/{filename}-sintralTC.txt", 'w')
    new_txt_file.write(sintral2x)
    new_txt_file.close()

    return 'Click.'

@app.route('/barcodes')
def home():
    return render_template('barcodes.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
