"""
Small proof of concept server for a client.

Takes some IDs and return an Excel document.
"""

from bottle import Bottle, run, request, response
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook


def create_xlsx(object_id, creative_ids):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['creative_id', 'object_id'])
    for creative_id in creative_ids:
        ws.append([creative_id, object_id])
    return save_virtual_workbook(wb)


app = Bottle()


@app.route('/export', method='GET')
def export():
    in_data = {
        'object_id': int(request.params['object_id']),
        'creative_ids': map(int, request.params.getall('creative_ids'))
    }

    xlsx = create_xlsx(**in_data)
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] =\
        'attachment; filename="export.xlsx"'
    return xlsx


if __name__ == '__main__':
    run(app, port=9090)
