import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


engine = webdriver.Chrome()
engine.get('https://www.instagram.com/')
sleep(3)

user_name = ""
passwd = ""

uid = engine.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(user_name)
passwd = engine.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(passwd)
btn = engine.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
sleep(5)

skip = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
sleep(2)

notification_skip = engine.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
sleep(2)

main_win = engine.current_window_handle

pofile = engine.find_element_by_xpath('/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').click()
sleep(2)

def blue_tick():
    holder = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]')
    try:
        bluetick = holder.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/span')
        return True
    except Exception as e:
        return False


def get_followers():
    follower = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
    sleep(2)

    scroll_box = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
    engine.execute_script('arguments[0].scrollIntoView()',scroll_box)
    last_ht = 0
    ht = 1
    while last_ht != ht: 
        last_ht = ht
        sleep(2)
        ht = engine.execute_script("""
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight;
        """,scroll_box)
    
    fList  = scroll_box.find_elements_by_tag_name('a')
    follower_names = [names.text for names in fList if names.text != '']
    finish = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
        .click()
    return follower_names

def get_following():
    following = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
    sleep(2)

    scroll_bar = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
    engine.execute_script('arguments[0].scrollIntoView()', scroll_bar)
    last_ht = 0
    ht = 1
    while last_ht != ht: 
        last_ht = ht
        sleep(2)
        ht = engine.execute_script("""
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight;
        """,scroll_bar)

    fList  = scroll_bar.find_elements_by_tag_name('a')
    following_names = [names.text for names in fList if names.text != '']
    finish = engine.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
        .click()
    return following_names


follower = get_followers()
print('got the followers')
following = get_following()
print('got the following')

not_following = [user for user in following if user not in follower]

print(not_following)

engine.switch_to_window(main_win)

for name in not_following:
    search = engine.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(name)
    sleep(2)

    popup = engine.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]')
    engine.execute_script('arguments[0].scrollIntoView()', popup)

    unfollower = popup.find_element_by_tag_name('a').click()
    sleep(2)

    verification = blue_tick()
    if not verification:
        unfollow_btn = engine.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button/div/span').click()
        sleep(2)
        unfollow_popup = engine.find_element_by_xpath('/html/body/div[4]/div/div/div')
        engine.execute_script('arguments[0].scrollIntoView()', unfollow_popup)
        unfollow = unfollow_popup.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
        print("Successfuly Unfollowed:" + name)
        sleep(2)

engine.close()






