import json


class JSONExporter:

    @staticmethod
    def export(report):

        return json.dumps(

            report,

            indent=4

        )