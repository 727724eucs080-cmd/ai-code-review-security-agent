import json
import os
import subprocess
import tempfile



class PylintTool:


    @staticmethod
    def scan(code: str):


        temp_path = None


        try:


            with tempfile.NamedTemporaryFile(

                suffix=".py",

                delete=False,

                mode="w",

                encoding="utf-8"

            ) as temp:


                temp.write(code)

                temp_path = temp.name



            result = subprocess.run(

                [

                    "pylint",

                    temp_path,

                    "--output-format=json",

                    "--score=no"

                ],

                capture_output=True,

                text=True,

                timeout=30

            )



            if result.stdout:


                return json.loads(

                    result.stdout

                )



            return []



        except subprocess.TimeoutExpired:


            return []



        except Exception:


            return []



        finally:


            if temp_path and os.path.exists(temp_path):

                os.remove(temp_path)