#new for loop
from jinja2 import Template
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
import tempfile
# Create a sample DataFrame


df = pd.read_csv(
    r"C:\Users\Avinash Reddy\Downloads\bquxjob_3fce411c_18a3db1f288.csv")

temp_sfaccount = df['SFAccountName'].unique().tolist()
template = Template('''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>emaill new</title>
    <style>
        /* Responsive layout - makes the two columns stack on top of each other instead of next to each other on screens that are smaller than 600 px */
        @media screen and (max-width: 750px) {
            .column {
                width: 100%;
                overflow-x: scroll;
            }
        }

        p {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 15px;
        }

        th,
        td {
            text-align: center;
            padding: 1rem;
            border-color: #f2f2f2;
            border-bottom: solid #d0d2d4;
            border-right: solid #d0d2d4;
        }

        table {
            border-collapse: collapse;
            border-spacing: 12;
            width: 50%;
            border: 2px solid #d0d2d4;
        }

        th {
            background-color: #073763;
            color: #f3f6f8;

        }

        
    </style>
</head>

<body>
    <div class="wrapper">
        <div class="">

            <p>Hello,</p>
            <p class="secondl">I hope you had a great week. Here is the summary on areas of focus for the Ads.txt
                entries
            </p>
            <p class="thirdl">Ads.Txt Summary for the week of [Respective time period Monday Date]</p>
        </div>
        <div class="">
            <table>
                <th>Total Issues this week</th>
                <th>#No. of Issues this week</th>
                <th>#No. of Issues fixed this week</th>
                <tr>
                    {% for row in df1.itertuples(index=False) %}
                        {% for value in row %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    {% endfor %}

                    {% for row in df2.itertuples(index=False) %}
                        {% for value in row %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    
                    {% endfor %}

                    {% for row in df3.itertuples(index=False) %}
                        {% for value in row %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    {% endfor %}
                </tr>



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

for get_sfaccout in temp_sfaccount:

    df_fil = df.loc[df['SFAccountName'] == get_sfaccout]

    df4_fil = df_fil.iloc[:, :-6]

    total_issues = df_fil['Missing'].sum()
    no_of_issues = df_fil['Fixed'].sum()
    no_of_fixed = df_fil['New_missing'].sum()

    with tempfile.NamedTemporaryFile(delete=True, suffix='.csv') as temp_csv:
        filtered_csv_path = f'{get_sfaccout}.csv'
        df4_fil.to_csv(filtered_csv_path, index=False)

        data1 = {'# Total Issues this week': [total_issues]}
        df1 = pd.DataFrame(data1)
        data2 = {'# No. of New Issues this week': [no_of_issues]}
        df2 = pd.DataFrame(data2)
        print(df2)
        data3 = {'# No. of Issues fixed this week': [no_of_fixed]}
        df3 = pd.DataFrame(data3)
        print(df3)
        # Create the Jinja template

        # Render the template and print the resulting HTML
        html = template.render(df1=df1, df2=df2, df3=df3)

        # SENDING AN EMAIL
        SENDER_EMAIL = 'ingestion@databeat.io'
        password = 'mtzshqoxjsvtqmek'
        recipient_list = ['avinash.reddy@databeat.io',
                          'shani.suthar@databeat.io', 'hussain.mohammed@databeat.io', 'aditya@databeat.io']
        #recipient_list = ['avinash.reddy@databeat.io']
        message = MIMEMultipart("alternatives")
        part_html = MIMEText(html, "html")
        message.attach(part_html)
        message["Subject"] = "Ads.Txt Summary for the week of [Respective time period Monday Date]"
        message['From'] = SENDER_EMAIL
        message["To"] = ",".join(recipient_list)
        print(get_sfaccout)
        with open(filtered_csv_path, "rb") as attachment:
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
