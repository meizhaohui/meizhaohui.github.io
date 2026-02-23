import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮箱的 SMTP 服务器地址, 用于新浪邮箱是: smtp.sina.com
mail_host = 'smtp.sina.com'
# 用户名
mail_user = 'your-email@sina.com'
# 密码(部分邮箱为授权码)
mail_pass = 'your-password'

# 发送方邮箱地址
sender = 'your-email@sina.com'
# 接收方邮箱地址
receivers = ['receiver@example.com']

# 设置邮件信息
message = MIMEText('通过加密方式发送的邮件正文.', 'plain', 'utf-8')
# message['From'] = Header('发件人昵称', 'utf-8')
# 此处巨坑，必须填写发送者的邮箱
# message['From'] = Header(sender, 'utf-8')
# message[‘From’]的Header不能添加第2个参数”utf-8”，否则检查不能通过
message['From'] = Header(sender)
message['To'] = Header('收件人昵称', 'utf-8')


subject = '通知邮件主题'
message['Subject'] = Header(subject, 'utf-8')

try:
    # 不使用SSL
    # smtpObj = smtplib.SMTP()
    # smtpObj.connect(mail_host, 25)  # 连接 SMTP 服务器

    # 使用SSL
    smtpObj = smtplib.SMTP_SSL(mail_host, "465")
    smtpObj.starttls()

    smtpObj.login(mail_user, mail_pass)  # 登录邮箱
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送邮件
    print('邮件发送成功')
except smtplib.SMTPException as e:
    print('邮件发送失败: ', e)
finally:
    smtpObj.quit()