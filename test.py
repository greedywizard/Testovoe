from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the webdriver (use the appropriate driver for your browser)
driver = webdriver.Chrome()

# Navigate to the dynamic web page
driver.get("https://example.com/your-dynamic-web-page")

# Wait for a specific element to be present
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "your_element_id"))
)

# Perform actions on the element or continue with your script
print(element.text)

# Close the driver when done
driver.quit()