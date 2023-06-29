import justpy as jp
import base64
import os


def upload_test():
    wp = jp.WebPage()

    dl = jp.A(text='Download', href='/static/af5bbeb474dc4a2ab711d744d5affb86/20230104_150729.jpg',
              download='20230104_150729.jpg', a=wp)

    return wp


jp.justpy(upload_test, websockets=False)


#<a id="1" download="20230104_150729.jpg" href="/static/af5bbeb474dc4a2ab711d744d5affb86/20230104_150729.jpg"
# rel="noopener noreferrer" target="_self" title="" style="color: #069; text-decoration: underline; cursor: pointer;">
# Download</a>

# import justpy as jp
#
#
# grid_options = {
#     'rowHeight': 200,
#     'columnDefs': [
#       {'headerName': "Make", 'field': "make"},
#       {'headerName': "Model", 'field': "model"},
#       {'headerName': "Price", 'field': "price"},
#     ],
#     'rowData': [
#       {'make': "Toyota", 'model': "Celica", 'price': 4},
#       {'make': "Ford", 'model': "Mondeo", 'price': '<div class="m-2 text-red-500 text-5xl">3</div>'},
#       {'make': "Porsche", 'model': "Boxter", 'price': '<img src="https://www.python.org/static/community_logos/python-powered-h-140x182.png">'}
#     ],
# }
#
# def grid_add_test():
#     wp = jp.WebPage()
#     grid = jp.AgGrid(a=wp, options=grid_options)
#     grid.html_columns = [2]
#     return wp
#
# jp.justpy(grid_add_test)