from flask import Flask, render_template, jsonify

# create the application object
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')  # render a template


@app.route('/my-link/')
def my_link():
  print ('I got clicked!')

  return 'Click.'

@app.route('/barcodes')
def home():
    return render_template('barcodes.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
