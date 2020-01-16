import datetime, requests, json, time, sys, ssl, smtplib

class send_email:
    def __init__(self, message=None, username='vijaykrishnannarayan@gmail.com', passcode='AmazonstrongwarrioR797', recipients=['nikhil.sunkad@gmail.com'], mail_server='smtp.gmail.com', subject=None):
        try:
            mail_message = 'Subject: %s\n\n%s' % (subject, message)
            self.mail_socket = smtplib.SMTP_SSL(host=mail_server, port=465)
            self.mail_socket.ehlo('smtp')
            self.mail_socket.login(user=username, password=passcode)

            for each_person in recipients:
                self.mail_socket.sendmail(from_addr=username, to_addrs=each_person, msg=mail_message)
            self.mail_socket.quit()

        except smtplib.SMTPConnectError:
            print('Network connection has failed. Try again or adjust network configuration, please.')
            sys.exit()
        except (smtplib.SMTPDataError, smtplib.SMTPHeloError):
            print('The mail server refused your data or request to send an email.')
            sys.exit()
        except smtplib.SMTPServerDisconnected:
            print('The server unexpectedly disconnected. Try again, please.')
            sys.exit()
        except UnicodeDecodeError:
            print('Unicode decode error with article:', message)
        except UnicodeEncodeError as exc:
            print('Unicode encode error with article:', message)
            print('Exception:', exc)
        except Exception as error:
            print('Failed to send mail. ', end='')
            error_code = str(error)
            print('Unknown error - Error code: %s\n' % error_code, end='')
            sys.exit()

class newspaper:
    def __init__(self):
        self.today = str(datetime.date.today())
        self.last_week = str(datetime.date.today() - datetime.timedelta(days=2))
        self.key = 'd50057161f60480a8aa5c4be47fed7b9'
        self.articles = dict()

        self.subjects = [
            'iran',
            'iraq',
            'saudi_arabia',
            'united_states',
            'oil',
            'israel',
            'china',
            'india',
            'technology',
            'britain',
            'europe',
            'terrorism',
            'us_election',
            'south_america',
            'markets',
            'trade'
        ]

        self.current_stories = list()

        for each_subject in self.subjects:
            paper = ''
            self.gather_info(each_subject)
            for article_number, each_article in enumerate(self.current_stories):
                new_story = self.parse_article(each_article, article_number)
                paper += new_story
            self.send_paper(each_subject, paper)
            self.current_stories = []

    def gather_info(self, current_subject):
        #Queries api, converts json to hash table, and puts info into article class
        request = 'https://newsapi.org/v2/everything?q=%s&from=%s&to=%s&sortBy=date&language=en&apiKey=%s' % (current_subject, self.last_week, self.today, self.key)
        news_response = requests.get(request)
        parsed_response = json.loads(news_response.content)
        news_response.close()

        all_articles = parsed_response['articles']
        self.current_stories = all_articles.copy()

    def parse_article(self, current_article, article_number):
        #Puts info into class
        publication = current_article['source']['name']
        title = current_article['title']
        external_link = current_article['url']
        publishing_time = current_article['publishedAt'].replace('T', ' at ')

        article_header = '#%d: \"%s\" from %s on %s. Read more at %s.\n' % (article_number, title, publication, publishing_time, external_link)
        try:
            encoded_header = article_header.encode('ASCII')
            return article_header
        except(UnicodeEncodeError):
            return ' '

    def send_paper(self, category, paper):
        subject = 'Your news about %s on %s' % (category, self.today)
        send_email(message=paper,
        username='vijaykrishnannarayan@gmail.com',
        passcode='AmazonstrongwarrioR797',
        recipients=['nikhil.sunkad@gmail.com', 'ns0631@pleasantonusd.net', 'nickcrumpet.litty@gmail.com'],
        mail_server='smtp.gmail.com',
        subject=subject)

def adjust(string):
    if len(string) == 1:
        string = '0' + string
    elif len(string) == 0:
        string = '00'
    return string

def main():
    while 1:
        last_time_file = open('last_time.txt', 'r')
        last_news_time = last_time_file.readline().rstrip('\n')
        last_time_file.close()
        today = str(datetime.date.today())
        last_complete_date = datetime.datetime.strptime(last_news_time, '%Y-%m-%d')
        last_date = str(last_complete_date.year) + '-' + adjust(str(last_complete_date.month)) + '-' + adjust(str(last_complete_date.day))

        if today > last_date:
            print('Current date:', today)
            print('Date last sent:', last_date)
            instance = newspaper()
            last_time_file = open('last_time.txt', 'w')
            last_news_time = last_time_file.write(today + '\n')
            last_time_file.close()

        time.sleep(1200)

if __name__ == '__main__':
    try:
        main()
    except(EOFError, KeyboardInterrupt):
        print('\nEnding news delivery program.')
    except Exception as error:
        breakpoint()
        print('An unexpected exception was raised. Exception:', error)
        print(sys.exc_info())
