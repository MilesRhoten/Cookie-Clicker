from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Set up Chrome options to use your existing user profile
options = webdriver.ChromeOptions()  # Use webdriver.ChromeOptions() instead of Options()
options.add_argument(r"user-data-dir=C:\Users\localadmin\AppData\Local\Google\Chrome\User Data")  # Replace with your path
#options.add_argument("--guest")
options.add_argument(r"profile-directory=Profile 1")  # Or the specific profile name if it's not "Default"

options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


# Set up the WebDriver (Make sure 'chromedriver' is in PATH)
service = Service(r"C:\Users\localadmin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update this path
driver = webdriver.Chrome(service=service, options=options)  # Pass options here!
# driver = webdriver.Chrome(service=service)  # Pass options here!

try:
    # Open Cookie Clicker
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    sleep(5)  # Wait for the game to load

    # Select language (if needed)
    try:
        lang_select = driver.find_element(By.ID, "langSelect-EN")
        lang_select.click()
        sleep(3)  # Wait for language to apply
    except:
        print("Language selection not needed.")

    # Extract the number of cookies
    while True:
        #cookies = driver.execute_script("return Game.cookies;")
        #print(f"Cookies: {int(cookies)}")

        cpsRaw = driver.execute_script("return Game.cookiesPsRaw;")
        print(f"CpsRaw: {int(cpsRaw)}")

        #buildingsOwned = driver.execute_script("return Game.BuildingsOwned;")
        #print(f"Total Buildings Owned: {int(buildingsOwned)}")

        #cookiesPsByType = driver.execute_script("return Game.cookiesPsByType;")
        #print(f"cookiesPsByType: {cookiesPsByType}")

        #cookiesMultByType = driver.execute_script("return Game.cookiesMultByType;")
        #print(f"cookiesMultByType: {cookiesMultByType}")

        

        #priceCursor = driver.execute_script("return Game.Objects.Cursor.bulkPrice")
        #cursorCpsTotal = driver.execute_script("return Game.cookiesPsByType.Cursor")
        #kittenMul = driver.execute_script("return Game.cookiesMultByType.kittens")

        globalMul = driver.execute_script("return Game.globalCpsMult")
        
        amtCursors = driver.execute_script("return Game.Objects.Cursor.amount")
        print(f"amtCursors: {amtCursors}")
        
        cursorStoredTotalCps = driver.execute_script("return Game.Objects.Cursor.storedTotalCps")
        print(f"Cursor Total CPS: {globalMul * cursorStoredTotalCps}")


        sleep(60)  # Update every 60 second

except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
