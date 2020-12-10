#! /usr/bin/python3

import asyncio
import json
import cgi
import cgitb
cgitb.enable()

async def get_led_manager_status ():
    message = '?\r\n'

    reader, writer = await asyncio.open_connection ('localhost', 8080)

    writer.write (message.encode ())

    data = await reader.readline ()
    count = int (data.decode ().rstrip ())

    json_items = []
    for i in range (count):
        data = await reader.readline ()
        mode_line = data.decode ().rstrip ()
        is_curr_p = mode_line[0] == '>'
        single_json_item = { 'name': mode_line[1:],
                             'current': is_curr_p }
        json_items.append (single_json_item)
    writer.close ()

    report_json (json_items)

async def set_led_manager_mode (mode):
    if len (mode) > 100:
        report_error ()
    for ch in mode:
        if not ch.isalnum () and ch != '_' and ch != '-':
            report_error ()
    message = "!%s\r\n" % mode

    reader, writer = await asyncio.open_connection ('localhost', 8080)

    writer.write (message.encode ())

    data = await reader.readline ()
    msg = data.decode ().rstrip ()

    if msg == 'OK':
        json_status = { 'status': 'OK' }
    else:
        json_status = { 'status': 'error' }

    report_json (json_status)

def report_json (obj):
    print ("Content-Type: application/json\n\n")
    print (json.dumps (obj))
    exit (0)
    
def report_error ():
    print ("Content-Type: application/json\n\n")
    json_item = { 'status': 'error' }
    print (json.dumps (json_item))
    exit (0)

form = cgi.FieldStorage()
if "action" not in form:
    report_error ()

if form['action'].value == 'status':
    asyncio.run (get_led_manager_status ())
elif form['action'].value == 'set':
    if "mode" not in form:
        report_error ()
    else:
        asyncio.run (set_led_manager_mode (form['mode'].value))
else:
    report_error ()


