import time

# cosmetic classes to be used throughout project
button_classes = "block w-32 h-10 bg-green-700 hover:bg-green-800 text-white font-bold py-1" \
                 "px-4 rounded m-5 overflow-hidden"
label_classes = "grid uppercase tracking-wide text-gray-700 text-xs font-bold" \
                "mb-2 mt-2"
input_classes = 'form-input'
banner_classes = 'block uppercase w-full place-items-center font-bold text-xs text-white align-left overflow-hidden'
banner_style = 'background:#047857; height:75px; font-size:30px; padding: 10px; border-style: solid; ' \
               'border-bottom-color: #065f46; border-bottom-width: 10px; cursor: pointer;'
banner_sub_classes = 'block uppercase w-full place-items-center italic text-xs text-white'
title_classes = 'text-center font-bold border m-5 mx-60 p-4 w-25 overflow-hidden'
desc_classes = 'text-center text-xs overflow-hidden'
table_title_classes = 'text-center font-bold overflow-hidden'


# go to home page on banner click
def banner_click(self, msg):
    msg.page.redirect = 'http://127.0.0.1:8000/reimbursementtable'


# displays 'saved!' message
def show_saved(self, msg):
    self.saved_div.set_class('visible')
    self.saved_div.visibility_state = 'visible'


# hides 'saved!' message after delay
def hide_saved(self, msg):
    time.sleep(1)
    self.saved_div.set_class('invisible')
    self.saved_div.visibility_state = 'invisible'


# list of purchase types
purchase_types = ['Event', 'Snacks', 'Decorations']
