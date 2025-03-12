from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# Load credentials from .env
load_dotenv("/home/user/Desktop/venv/target.env")
EMAIL = os.getenv("TARGET_EMAIL")
PASSWORD = os.getenv("TARGET_PASSWORD")
CVC = os.getenv("TARGET_CVC")

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Login - Target for now, should be modular later
def login_to_target():
    """Logs in to Target using saved credentials."""
    driver.get("https://www.target.com")
    time.sleep(2)

    # Prompt user to manually click sign-in
    print("Please manually click the 'Sign in' button on the Target website.")
    print("Waiting for login form to appear...")
    
    # Wait for the login form to appear (after user clicks Sign in)
    try:
        # Wait for email field to be present
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        print("Login form detected! Auto-filling credentials...")
        
        # Fill Email and Password
        email_field.send_keys(EMAIL)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)  # Press Enter
        print("Credentials auto-filled and submitted!")
        
    except Exception as e:
        print(f"Error during login form completion: {e}")
        driver.save_screenshot("login_form_error.png")
        raise

# Confirm item is available (and eventually price check), then add it to the cart
def check_and_add_to_cart(url):
    """Checks the product's availability and adds it to the cart."""
    driver.get(url)

    # Monitor availability
    while True:
        try:
            add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']")))
            add_to_cart.click()
            print("Item added to cart!")
            break
        except:
            print("Item not available. Retrying...")
            time.sleep(5)  # Retry after a delay

# Checkout - probably has to be specific for target but maybe modular
def proceed_to_checkout():
    """Completes the checkout process."""
    # Go to cart
    driver.get("https://www.target.com/co-cart")

    # Proceed to checkout
    checkout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Checkout']")))
    checkout_btn.click()

    # Input CVC for credit card (assuming saved payment method)
    cvc_field = wait.until(EC.presence_of_element_located((By.NAME, "cvv")))
    cvc_field.send_keys(CVC)
    cvc_field.send_keys(Keys.RETURN)

    print("Checkout process initiated!")

# Main process
try:
    login_to_target()
    check_and_add_to_cart("https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904")
    # proceed_to_checkout()
finally:
    driver.quit()