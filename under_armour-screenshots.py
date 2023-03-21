# Import necessary modules
from selenium import webdriver
import time
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

inc = 0

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://about.underarmour.com/en/stories/articles.html')

time.sleep(3)

try:
    close_button = driver.find_element_by_xpath('//button[@aria-label="Privacy Close"]')
    close_button.click()
except:
    pass

# Find and click the "75" button to show more stories
button = driver.find_element(by='xpath', value='//button[@value="75"]')
button.click()

next_button = driver.find_element(by='xpath', value='//button[@class="pagination__next-btn pagination--btn" and not(@disabled)]')

#add a click and sleep after each page finishes
next_button.click()
time.sleep(3)

# Find all "a" tags with href starting with "/content/ua/about/en/stories"
story_links = driver.find_elements_by_xpath('//a[starts-with(@href, "/content/ua/about/en/stories")]')

link_list = []
for link in story_links:
    link_list.append(link.get_attribute('href'))

# Visit every link in link_list and screenshot the entire page
for link in link_list:
    driver.get(link)
    time.sleep(7)
    try:
        close_button = driver.find_element_by_xpath('//button[@aria-label="Privacy Close"]')
        close_button.click()
    except:
        pass
    # Get the full height of the page
    full_height = driver.execute_script("return document.documentElement.scrollHeight")
    # Set initial scroll position and screenshot height
    current_scroll = 0
    screenshot_height = 0
    # Initialize a list to hold the screenshots
    screenshots = []
    # Repeat until we have scrolled to the bottom of the page
    while current_scroll < full_height:
        # Take a screenshot of the visible area
        screenshot = driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot = screenshot.convert('RGB')
        # Append the screenshot to the list
        screenshots.append(screenshot)
        # Scroll down by the height of the visible area
        current_scroll += screenshot_height
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        # Wait for the page to finish rendering
        time.sleep(1)
        # Calculate the height of the next visible area
        screenshot_height = driver.execute_script("return Math.min(document.documentElement.clientHeight, document.documentElement.scrollHeight - window.pageYOffset);")
    # Combine the screenshots into one image
    combined_image = Image.new('RGB', (screenshots[0].width, full_height))
    current_height = 0
    for screenshot in screenshots:
        combined_image.paste(screenshot, (0, current_height))
        current_height += screenshot.height
    # Save the combined image as a JPEG in the current working directory
    combined_image.save(f"{inc}-{link.split('/')[-1]}.jpg")
    inc=inc+1
        
# Close the Chrome webdriver
driver.quit()
