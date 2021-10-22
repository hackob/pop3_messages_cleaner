import config
import poplib
from datetime import datetime
from datetime import date
from datetime import timezone
from email.header import Header, decode_header, make_header


Mailbox = poplib.POP3_SSL(config.POP_SERVER, config.POP_SERVER_PORT) 
Mailbox.user(config.POP_USER)
Mailbox.pass_(config.POP_PASSWD)

messages_in_mailbox = len(Mailbox.list()[1])
today = datetime.now(timezone.utc)
print(f'Number of messages in inbox : {messages_in_mailbox}')

for message_id in range(messages_in_mailbox):
    deleivery_date      = None
    subject             = None
    current_message_id  = None
    message_export_text = None
    export_message_name = None
    charset             = 'utf-8'
    
    got_deleivery_date      = False
    got_subject             = False
    message_will_be_deleted = False

    current_message_id = message_id + 1  

    for msg_line in Mailbox.retr(current_message_id)[1]:
        try:
            message_string = msg_line.decode()
        except UnicodeDecodeError:
            message_string = msg_line.decode('latin-1')

        if message_string.startswith('Delivery-date: '):
            deleivery_date_str    = message_string.replace('Delivery-date: ', '')
            deleivery_date_object = datetime.strptime(deleivery_date_str, '%a, %d %b %Y %H:%M:%S %z')
            got_deleivery_date = True
        
        if message_string.startswith('Subject: '):
            subject = message_string.replace('Subject: ', '')
            subject = str(make_header(decode_header(subject)))
            got_subject = True

        if got_subject and got_deleivery_date:
            days_since_message_received = (today - deleivery_date_object).days
            if days_since_message_received > config.DAYS_TO_MARK_OLD:
                message_will_be_deleted = True

                deleivery_date_object = datetime.strptime(deleivery_date_str, '%a, %d %b %Y %H:%M:%S %z')
                export_message_name = f"{deleivery_date_object.strftime('%Y%m%d_%H%M%S')}_{current_message_id:05d}.msg"

                with open('./bkp_messages/' + export_message_name, 'wb') as export_message_file:
                    for export_message_line in Mailbox.retr(current_message_id)[1]:
                        export_message_file.write(export_message_line)

                Mailbox.dele(current_message_id)

            print(f'{current_message_id}\t | {deleivery_date_str}\t | {message_will_be_deleted}\t | {subject}')
            Mailbox.noop()
            
            break

Mailbox.quit()