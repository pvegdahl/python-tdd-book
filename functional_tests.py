from selenium import webdriver

browser = webdriver.Firefox()

# Go to the webpage to check out the app
browser.get('http://localhost:8000')

# The page title mentions to-do lists
assert 'To-Do' in browser.title

# The user is invited to enter a to-do immediately

# She enters "Buy peacock feathers" into a text box

# She hits enter, the page updates, and now lists:
# "1: Buy peacock feathers" as a to-do list item

# There is still a text box to enter another item.  She
# enters "Use peacock feathers to make a fly"

# The page updates again, and now shows both items

# There is now a unique URL to use to save her to-do list
# There is explanatory text to that effect.

# The user visits that unique URL and the todo list is still there!

# Satisfied, she goes back to sleep
browser.quit()
