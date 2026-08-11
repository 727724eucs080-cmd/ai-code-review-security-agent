import json
import os
import subprocess
import tempfile


class BanditTool:


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

                    "bandit",

                    temp_path,

                    "-f",

                    "json"

                ],

                capture_output=True,

                text=True,

                timeout=30

            )



            if result.stdout:


                return json.loads(

                    result.stdout

                )



            return {


                "results": []

            }



        except subprocess.TimeoutExpired:


            return {


                "error":

                "Bandit scan timed out.",


                "results":

                []

            }



        except Exception as e:


            return {


                "error":

                str(e),


                "results":

                []

            }



        finally:


            if temp_path and os.path.exists(temp_path):

                os.remove(temp_path)