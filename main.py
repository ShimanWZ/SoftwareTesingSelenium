import random
import string
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk


class SampleTeseCase(unittest.TestCase):
    def setUp(self):
        # open Firefox browser
        self.driver = webdriver.Firefox()
        # maximize the window size
        self.driver.maximize_window()
        # delete the cookies
        self.driver.delete_all_cookies()
        # navigate to the url
        self.driver.get('http://localhost:3000/emoji-search')

    def testCopyToClipboard(self):
        # choosing a random emoji in first page
        random_emoji_index = random.randint(1, 20)
        self.emoji = self.driver.find_element(By.XPATH,
                                              '/html/body/div/div/div[2]/div[' + str(random_emoji_index) + ']')
        # clicking an emoji should copy that to out clipboard
        self.emoji.click()
        # saving chosen emoji's text attribute
        self.emoji_text_attr = self.emoji.get_attribute("data-clipboard-text")
        # finding input element
        self.input = self.driver.find_element(
            By.XPATH, '//div[@class="component-search-input"]/div/input')
        # paste copied emoji to input
        self.input.click()
        self.input.send_keys(Keys.CONTROL + "V")
        time.sleep(1)
        # getting clipboard data
        root = tk.Tk()
        root.withdraw()
        self.clipboard_text = root.clipboard_get()
        # check if the text copied is the same as emoji's text
        self.assertTrue(self.clipboard_text == self.emoji_text_attr)

    def testSearch(self):
        # finding input element
        self.input = self.driver.find_element(
            By.XPATH, '//div[@class="component-search-input"]/div/input')

        # choosing a random letter to search to diversify the emoji range
        random_letter = random.choice(string.ascii_letters)
        self.input.send_keys(random_letter)
        # choosing a random emoji in first page diversified by a random letter
        random_emoji_index = random.randint(1, 20)
        self.emoji_text = self.driver.find_element(By.XPATH,
                                                   '/html/body/div/div/div[2]/div[' + str(
                                                       random_emoji_index) + ']/span[1]').text
        # searching chosen emoji
        self.input.clear()
        self.input.send_keys(self.emoji_text)
        # checking if the emoji appears in search results
        self.results = self.driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div/span[1]')
        self.results = [x.text for x in self.results]
        # check if the text copied is the same as emoji's text
        self.assertTrue(self.emoji_text in self.results)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
