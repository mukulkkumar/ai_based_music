##
# Contains the module which can play music by listening to your voice
#
# @file
# @copyright 2021 AI Based music module
#

import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from gtts import gTTS
import playsound
import time


class Music(object):
    """
    This class is used to provide the feature in which it will allow user to speak, which song they wants to play, then
    the functionality of class is to search the song in music.com website, and play it for the user from there.
    """
    def __init__(self, browser):
        self.browser = browser

    @staticmethod
    def speak(text):
        tts = gTTS(text=text, lang="en")
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)

    @staticmethod
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
            except Exception as e:
                print("Exception: " + str(e))

        return said

    @staticmethod
    def remove_add(browser):
        try:
            pop_up = browser.find_element_by_css_selector('html.svgfilters.no-svgclippaths.no-svgforeignobject.no-inlinesvg.svgasimg.no-cssscrollbar body.white.removescroll div#popup.popupbg1 a.popup-close')
        except Exception as exec:
            print("The exception for pop is {}".format(exec))
            pop_up = None

        if pop_up:
            print("The add is closed")
            pop_up.click()

    def play_music(self):
        self.speak("Which song, do you want me to play?")
        text = self.get_audio()
        print("The text is {}".format(text))
        if text:
            self.browser.get('https://gaana.com/')
            # for loading the website completely
            time.sleep(5)
            input_element = self.browser.find_element_by_id("sb")
            input_element.send_keys(text)
            input_element.send_keys(Keys.ENTER)
            # let the search gets completed
            time.sleep(2)
            # click on the first song in the search item
            albums = self.browser.find_element_by_css_selector('div.carousel:nth-child(2) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1)').click()
            time.sleep(5)
            # remove the add, if any pop-up comes
            self.remove_add(self.browser)
            try:
                play_song = self.browser.find_elements_by_css_selector('.playalbum')[0].click()
            except Exception as ex:
                play_song = None

            time.sleep(20)
            pause_song = self.browser.find_elements_by_css_selector('.playalbum')[0].click()
            time.sleep(2)


if __name__ == "__main__":
    firefox_browser = webdriver.Firefox(executable_path="/home/mukul/Downloads/geckodriver-v0.29.0-linux32/geckodriver")
    music = Music(firefox_browser)
    while True:
        try:
            music.play_music()
        except Exception as ex:
            print(f"The exception is {ex}")

