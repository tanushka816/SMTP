import os
import sys
import configparser
import base64
import socket
import ssl


PORT = 465
SERVER = 'smtp.yandex.ru'
bnd = "boundaryText"


RECIPIENT = ['tanushka.vasilieva816@yandex.ru']
SENDER = 'testIMAPChe@yandex.ru'
SEND_PSSW = 'fortest'

MIMEs = {'jpeg': 'image/jpeg',
         'png': 'image/png',
         'txt': 'text/plain',
         'pdf': 'application/pdf'}

DIRECTORY = "data"
CONFIG_FILE = "config.ini"


def start(server=SERVER):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, PORT))
    ssl_sock = ssl.wrap_socket(sock)
    data = ssl_sock.recv(1024)
    # print(data)
    end_letter = wrap_up_letter()
    for i in end_letter:
        # i = i + '\r\n'
        # print(i)
        # print("---")
        ssl_sock.send(i.encode())
        answer = ssl_sock.recv(1024)
        print(answer)
    ssl_sock.close()


def wrap_up_letter(recp=RECIPIENT, sender=SENDER, send_pssw = SEND_PSSW):
    text_f, recp, subj, attachm = get_from_config()
    text_mess = ""
    for text_in in text_f:
        text_mess += get_text(text_in)

    # print(build_letter(subj, text_mess, attachm))
    packet = build_letter(subj, text_mess, attachm)
    recp_to = ""
    for rec in recp:
        recp_to += 'RCPT TO: ' + rec + '\r\n'
    result = ['EHLO '+sender.split('@')[0] + '\r\n', 'AUTH LOGIN\r\n',
              base64.b64encode(sender.encode()).decode() + '\r\n',
              base64.b64encode(send_pssw.encode()).decode()+'\r\n',
              'MAIL FROM: ' + sender + '\r\n',
              # *['RCPT TO: ' + r for r in recp + '\r\n'],
              recp_to,
              'DATA\r\n',
              packet + '\r\n',
              'QUIT'
              ]
    return result


def get_from_config(dirct=DIRECTORY, conf_file=CONFIG_FILE):
    """
    Create, read, update, delete config
    """
    path = os.path.join(dirct, conf_file)
    if not os.path.exists(path):
        print("Please, create config.ini with ini_maker.py in data!")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(path)

    recipients = []
    addr_list = config.items("TO")
    for _, recp in addr_list:
        recipients.append(recp)

    subj = config.get("SUBJECT", "subject")
    # text = config.get("TEXT", "text")
    text = []
    text_list = config.items(("TEXT"))
    for _, t in text_list:
        text.append((t))

    attachms = []
    attm_list = config.items("ATTACHMENTS")
    for _, atc in attm_list:
        attachms.append(atc)

    return text, recipients, subj, attachms


def build_letter(subj, text, attachm, recp=RECIPIENT, sender=SENDER):
    global bnd
    result = f"From: {sender}\n"
    for recp in recp:
        result += f"To: {recp}\n"
    result += f"Subject: =?UTF-8?B?{base64.b64encode(subj.encode()).decode()}?=\n"
    # bnd = str(hash("boundaryText"))  # реплэйс
    # # print(bnd)
    # bnd = "boundaryText"
    if text and '\n.\n' in text:
        text = text.replace('\n.\n', '\n..\n')
        # text = text.replace("boundaryText", "boundaryText")

    if attachm:
        result += f"Content-Type: multipart/mixed; boundary={bnd};\n\n"
        if text:
            result += f"--{bnd}\nContent-Type: text/plain; charset=utf-8;\n"
            # result += f"Content-Transfer-Encoding: base64\n\n"
            result += text + '\n.'
        for atc in attachm:
            name_b64 = f'"=?UTF-8?B?{base64.b64encode(atc.encode()).decode()}?="'
            result += f"--{bnd}\nContent-Type:{MIMEs[atc.split('.')[-1]]};\nContent-Transfer-Encoding:base64\n"
            result += f"Content-Disposition:attachment; filename={name_b64}\n\n"  # or relative
            # result += f"--{bnd}\nContent-Disposition:attachment; filename={name_b64}\n"
            # result += f"Content-Transfer-Encoding:base64\nContent-Type:{MIMEs[atc.split('.')[-1]]}; "
            # result += f"name={name_b64}\n\n"

            # result += f"--{bnd}\n Content-Type:{MIMEs[atc.split('.')[-1]]}; name={name_b64}\n "
            # result += f"Content-Transfer-Encoding:base64\n Content-Disposition:attachment; filename={name_b64}\n\n"
            result += f"{attachment_to_base64(atc)}\n\n"
            # print(attachment_to_base64(atc))
        result += f"--{bnd}--\n"
    else:
        # result += f"Content-Type: text/plain; charset=utf-8;\n {text}"
        result += "Content-Type: text/plain; charset=utf-8;\nContent-Transfer-Encoding: base64\n\n"
        result += base64.b64encode(text.encode()).decode()
    # print(result + "\n.")
    return result + "\n."


def attachment_to_base64(atc):
    with open(f"data\\{atc}", mode='rb') as f:
        return base64.b64encode(f.read()).decode()


def get_text(file):
    global bnd
    bnd_count = 0
    result = ""
    with open("data\\" + file, encoding="utf-8", mode='r') as f:
        for line in f:
            if bnd in line:
                bnd += str(bnd_count)
                bnd_count += 1
            result += line
        # if "boundaryText" in
    return result


if __name__ == '__main__':
    start()
