
from jinja2 import Template
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
# Create a sample DataFrame
data1 = {'# Total Issues this week': ['1']}
df1 = pd.DataFrame(data1)
data2 = {'# No. of New Issues this week': ['10'] }
df2 = pd.DataFrame(data2)
data3 = {'# No. of Issues fixed this week': ['5'] }
df3 = pd.DataFrame(data3)
print(df3)


# Create the Jinja template
template = Template('''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>emaill new</title>
    <style>
        body {
            Margin: 0 !important;
            padding: 15px;
            background-color: #FFF;
        }

        .wrapper {
            width: 100%;
            table-layout: fixed;
        }

        .wrapper-inner {
            width: 100%;
            max-width: 900px;
            Margin: 0 auto;
        }

        .phead {
            background-color: grey;
            color: whitesmoke;
            font-family: Arial, Helvetica, sans-serif;
        }

        * {
            box-sizing: border-box;
            border: black;
        }

        .thirdl {
            font-weight: bold;
            font-family: Arial, Helvetica, sans-serif;
        }

        .table-container {
              display: flex;
            /* justify-content: space-between; */
            align-items: flex-start;
           
             width: 100%;
            max-width: 900px;
            Margin: 0 auto;
        }

        table {
            width: 20%;
            /* Adjust the table width as needed */
            max-width: 250px;
            /* Limit maximum table width */
            border: 2px solid #FFFFFF;
            border-spacing: 0;
        }

        th,
        td {
            text-align: center;
            padding: 1rem;
            border-color: #FFFFFF;
            border-bottom: solid #073763;
            border-right: solid #073763;
            border-left: solid #073763;
            border-top: solid #073763;
        }

        th {
            background-color: #073763;
            color: #f3f6f8;
        }

        @media screen and (max-width: 750px) {
            .column {
                width: 100%;
                overflow-x: scroll;
            }
        }
    </style>
</head>

<body>
    <div class="wrapper">
        <div class="wrapper-inner">

            <p>Hello,</p>
            <p class="secondl">I hope you had a great week. Here is the summary on areas of focus for the Ads.txt
                entries
            </p>
            <p class="thirdl">Ads.Txt Summary for the week of [Respective time period Monday Date]</p>
        </div>
        <div class="table-container">
           <table>
                    <tr>
                        {% for column in df1.columns %}
                            <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                    {% for row in df1.itertuples(index=False) %}
                        <tr>
                            {% for value in row %}
                                <td>{{ value }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                </table>
             <table>
                    <tr>
                        {% for column in df2.columns %}
                            <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                    {% for row in df2.itertuples(index=False) %}
                        <tr>
                            {% for value in row %}
                                <td>{{ value }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                </table>
            <table>
                    <tr>
                        {% for column in df3.columns %}
                            <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                    {% for row in df3.itertuples(index=False) %}
                        <tr>
                            {% for value in row %}
                                <td>{{ value }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                </table>
        </div>
        <div class="wrapper-inner">
            <p>Note: <br>
                * The above table consists of only Top-5 Pubishers with missing entries.<br>
                * For all publishers, please visit the dashboard shared in the email or download the Attachment"
            </p>
            <p>The linked report <i>[Hyperlink the datastudio dashboard link]</i> provides additional information on
                the
                above details</p>
            <p><b>Attached files </b><br>
                1. Publisher Domains & Missing entries <br>
                2. Full ads.txt file </p>
        </div>
    </div>
</body>

</html>
''')


# Render the template and print the resulting HTML
html = template.render(df1=df1, df2=df2, df3=df3)
attachment_path = r"C:\Users\Avinash Reddy\Downloads\Sample-Spreadsheet-100-rows.csv"

# SENDING AN EMAIL
SENDER_EMAIL = 'ingestion@databeat.io'
password = 'mtzshqoxjsvtqmek'
recipient_list = ['avinash.reddy@databeat.io',
                  'hussain@databeat.io']
message = MIMEMultipart("alternatives")
part_html = MIMEText(html, "html")
message.attach(part_html)
message["Subject"] = "Ads.Txt Summary for the week of [Respective time period Monday Date]"
message['From'] = SENDER_EMAIL
message["To"] = ",".join(recipient_list)
with open(attachment_path, "rb") as attachment:
    att = MIMEApplication(attachment.read(), _subtype="csv")
    att.add_header("Content-Disposition",
                   f"attachment; filename=attachment.csv")
    message.attach(att)
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(SENDER_EMAIL, password)

for recipient in recipient_list:
    server.sendmail(SENDER_EMAIL, recipient, message.as_string())
server.quit()
