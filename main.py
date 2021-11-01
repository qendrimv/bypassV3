import requests
import re

r = requests.Session()
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.google.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def anchor_get_req(url): # You can get the anchor url by looking at the headers of the main POST request which returns the recaptchaV3 token, the referer header in that request is the anchor url, it also has the word "anchor" in it.
    source = r.get(url, headers=headers).text
    token = re.search(r'input type="hidden" id="recaptcha-token" value="(.*?)"', source).group(1)
    return token


def get_recaptchaV3_token(url, anchor_url): # The url is the POST url that is being made to receive the recaptcha V3 respond. The referer in the headers is the anchor url
    token = anchor_get_req(anchor_url)
    headers['referer'] = anchor_url
    data = f'reason=q&c={token}'
    source = r.post(url, headers=headers, data=data).text
    recaptchaV3_token = re.search(r'"rresp","(.*?)"', source).group(1)
    
    return recaptchaV3_token


def login_to_wordpress(email, password, recaptchaV3_token):
    headers['origin'] = 'https://login.wordpress.org'
    headers['referer'] = 'https://login.wordpress.org'
    data = f'log={email}&pwd={password}&wp-submit=Log+In&redirect_to=https%3A%2F%2Flogin.wordpress.org%2F&_reCaptcha_v3_token={recaptchaV3_token}'

    source = r.post('https://login.wordpress.org/wp-login.php', headers=headers, data=data).text
    return source

if __name__ == '__main__':
    recaptchaV3_token = get_recaptchaV3_token('https://www.google.com/recaptcha/api2/reload?k=6LckXrgUAAAAANrzcMN7iy_WxvmMcseaaRW-YFts', 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LckXrgUAAAAANrzcMN7iy_WxvmMcseaaRW-YFts&co=aHR0cHM6Ly9sb2dpbi53b3JkcHJlc3Mub3JnOjQ0Mw..&hl=en&v=UrRmT3mBwY326qQxUfVlHu1P&size=invisible&cb=wyzyluf9z4zq')

    email = 'test@gmail.com'
    password = 'password'
    login_response = login_to_wordpress(email, password, recaptchaV3_token)
    if 'The password you entered for the username' in login_response:
        print('Request made successfully!')
    elif 'is not registered on WordPress.org' in login_response:
        print('Request made successfully!')
    elif '">Log Out<' in login_response:
        print('Request made successfully! You logged into your account.')
    else:
        print(login_response)
