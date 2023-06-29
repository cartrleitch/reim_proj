import sqlite3
import sys
import justpy as jp
from cosmetic_classes import *
import time
import os
import base64
from main_reim_pur import *


@jp.SetRoute('/editpurchase')
def edit_purchase_main():
    # create and title webpage
    wp = jp.WebPage(delete_flag=False)
    wp.title = 'Add Purchase'

    # creates page banner
    banner_div = jp.Div(text='Five Oaks Church', a=wp, classes=banner_classes,
                        style=banner_style,
                        click=banner_click)
    banner_sub = jp.Div(text='Reimbursement Manager', a=banner_div, classes=banner_sub_classes,
                        style='font-size:15px; padding-top: 10px;')
    title_div = jp.Div(text='Purchase Edit', a=wp,
                       classes=title_classes)
    description_div = jp.Div(text='Edit Purchase', a=title_div,
                             classes=desc_classes)

    # page divs
    form_div = jp.Div(a=wp, classes='grid h-50')
    form1 = jp.Form(a=form_div, classes='border m-5 p-5 w-100')
    input_div = jp.Div(a=form1, classes='flex flex-col items-center py-1')
    button_div = jp.Div(a=form1, classes='flex flex-col items-center py-3')
    button_div2 = jp.Div(a=button_div, classes='flex flex-row items-center py-3')

    sel_pur = pur_ret()
    conn = sqlite3.connect('db_reimbursements.db')
    cur = conn.cursor()
    cur.execute(f"SELECT PurchaseID, PurchaseDate AS 'Purchase Date', Amount AS Amount, "
                f"Content, PurchaseType AS 'PurchaseType' FROM Purchase WHERE PurchaseID = {sel_pur}")
    selected_pur = cur.fetchone()
    conn.close()

    date_val = selected_pur[1]
    amount_val = selected_pur[2]
    contents_val = selected_pur[3]
    type_val = selected_pur[4]

    # date entry
    date_label = jp.Label(a=input_div, text='Date', classes=label_classes)
    date_in = jp.Input(a=input_div, placeholder='Date', value=date_val, classes=input_classes, type='date')
    date_label.for_component = date_in

    # total cost entry
    cost_label = jp.Label(a=input_div, text='Total Cost', classes=label_classes)
    cost_in = jp.Input(a=input_div, placeholder='Total Cost', value=amount_val,  classes=input_classes, type='text')
    cost_label.for_component = cost_in

    # purchase type dropdown menu input
    purchaseType_label = jp.Label(a=input_div, text='Purchase Type', classes=label_classes)
    select = jp.Select(a=input_div, value=type_val)
    for pur_type in purchase_types:
        select.add(jp.Option(value=pur_type, text=pur_type))
    purchaseType_label.for_component = select

    # contents entry
    contents_label = jp.Label(a=input_div, text='Contents', classes=label_classes)
    contents_in = jp.Textarea(a=input_div, placeholder='Contents', value=contents_val,
                              classes='form-input', type='text')
    contents_label.for_component = contents_in

    # receipt image upload
    receipt_img = jp.Label(a=input_div, text='Receipt', classes=label_classes)
    receipt_img_in = jp.Input(a=input_div, classes=input_classes, type='file',
                              multiple=False, accept='image/*')
    receipt_img_in.for_component = receipt_img_in

    # button that calls submit_form when pressed
    save_button = jp.Input(value='Save', type='submit', a=button_div2, classes=button_classes,
                           style='cursor: pointer')
    saved_div = jp.Div(text='Saved!', classes='flex flex-row items-center font-bold text-sm text-green-500 invisible',
                       a=button_div)
    saved_div.visibility_state = 'invisible'
    save_button.saved_div = saved_div

    save_button.on('click', show_saved)
    save_button.on('mouseleave', hide_saved)

    # returns to main page
    done_button = jp.Button(text='Done', type='button', a=button_div2, classes=button_classes,
                            click=done_red)

    form1.on('submit', submit_form)
    # creates webpage
    return wp


def submit_form(self, msg):
    data = msg.form_data
    date = ''
    total_cost = ''
    p_type = ''
    contents = ''
    for output in data:
        if output['placeholder'] == 'Date':
            date = output.value

        if output['placeholder'] == 'Total Cost':
            total_cost = float(output.value)

        if output['html_tag'] == 'select':
            p_type = output.value

        if output['placeholder'] == 'Contents':
            contents = output.value

    # saves image
    # if not in directory named after session id,
    # make one
    if not os.path.isdir(msg.session_id):
        os.mkdir(msg.session_id)

    # set data to submitted file
    for data in msg.form_data:
        if data.type == 'file':
            break

    # open directory and write file to it
    rec_file_update = ''
    for index, value in enumerate(data.files):
        # html to insert for receipt link
        rec_file_update = f'<a id="1" download="{value.name}" ' \
                   f'href="static/{msg.session_id}/{value.name}"' \
                   f' rel="noopener noreferrer" target="_self" title="" ' \
                   f'style="color: #069; text-decoration: underline; cursor: pointer;">Download</a>'
        with open(f'{msg.session_id}/{value.name}', 'wb') as file:
            file.write(base64.b64decode(value.file_content))
    file_list = os.listdir(msg.session_id)

    conn = sqlite3.connect('db_reimbursements.db')
    cur = conn.cursor()
    reim_val = reim_ret()
    pur_val = pur_ret()
    # update selected purchase values
    cur.execute('UPDATE Purchase SET PurchaseDate = ?, Amount = ?, Content = ?, PurchaseType = ?, '
                'ReimID = ?, RecImg = ? '
                'WHERE PurchaseID = ?'
                , (date, total_cost, contents, p_type, reim_val, rec_file_update, pur_val))
    # update corresponding reimbursement total
    cur.execute(f'UPDATE Reimbursements SET Total = (SELECT SUM(Amount) FROM Purchase WHERE ReimID = {reim_val}) '
                f'WHERE ReimID = {reim_val}')
    conn.commit()
    conn.close()


# redirects to main page
def done_red(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/reimbursementtable'


if __name__ == '__main__':
    edit_purchase_main()
