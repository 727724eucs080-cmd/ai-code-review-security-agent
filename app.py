import os

from flask import Flask, render_template, request

from utils.file_handler import allowed_file

from utils.syntax_checker import (
    check_python_syntax,
    check_java_syntax
)

app = Flask(__name__)

# Folder where uploaded files are stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        uploaded_file = request.files.get("codefile")

        pasted_code = request.form.get("code")

        language = request.form.get("language")

        file_name = ""

        source_code = ""

        syntax_result = {
            "language": "",

            "status": "",

            "message": ""
        }

        # ==================================
        # CASE 1 : FILE UPLOAD
        # ==================================

        if uploaded_file and uploaded_file.filename != "":

            if allowed_file(uploaded_file.filename):

                file_name = uploaded_file.filename

                save_path = os.path.join(

                    app.config["UPLOAD_FOLDER"],

                    file_name
                )

                uploaded_file.save(save_path)

                # Read uploaded file

                with open(

                    save_path,

                    "r",

                    encoding="utf-8"

                ) as file:


                    source_code = file.read()

                # Detect language from extension

                if file_name.endswith(".py"):

                    syntax_result = check_python_syntax(

                        source_code
                    )

                elif file_name.endswith(".java"):

                    syntax_result = check_java_syntax(

                        source_code
                    )

            else:

                syntax_result = {

                    "language": "",

                    "status": "Error",

                    "message":
                    "Only Python (.py) and Java (.java) files are allowed."

                }

        # ==================================
        # CASE 2 : PASTE CODE
        # ==================================

        elif pasted_code and pasted_code.strip():

            source_code = pasted_code

            file_name = "Pasted Code"

            if language == "python":

                syntax_result = check_python_syntax(

                    source_code
                )

            elif language == "java":

                syntax_result = check_java_syntax(

                    source_code
                )

            else:

                syntax_result = {

                    "language": "",

                    "status": "Error",

                    "message":
                    "Please select a programming language."
                }

        # ==================================
        # CASE 3 : NOTHING PROVIDED
        # ==================================

        else:
            
            syntax_result = {

                "language": "",

                "status": "Error",

                "message":
                "Please upload a file or paste code."
            }

        return render_template(

            "result.html",

            file_name=file_name,

            syntax=syntax_result,

            source_code=source_code
        )
    return render_template("index.html")

if __name__ == "__main__":


    app.run(debug=True)