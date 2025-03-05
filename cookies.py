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
        
        #amtCursors = driver.execute_script("return Game.Objects.Cursor.amount")
        #print(f"amtCursors: {amtCursors}")

        #cursorStoredTotalCps = driver.execute_script("return Game.Objects.Cursor.storedTotalCps")
        #print(f"Cursor Total CPS: {globalMul * cursorStoredTotalCps}")

        #buildings = driver.execute_script("return Game.ObjectsById")
        
        maxEfficiency = 0
        indexOf = 0
        isUpgrade = 0
        maxCps = 0

        # check buildings
        for i in range(20):
            buildingStoredTotalCps = driver.execute_script("return Game.ObjectsById[" + str(i) + "].storedTotalCps")
            buildingName = driver.execute_script("return Game.ObjectsById[" + str(i) + "].name")
            amtBuilding = driver.execute_script("return Game.ObjectsById[" + str(i) + "].amount")
            price = driver.execute_script("return Game.ObjectsById[" + str(i) + "].price")
            cpsEach = (globalMul * buildingStoredTotalCps) / amtBuilding
            efficiency = (cpsEach / price)
            if (efficiency > maxEfficiency):
                maxEfficiency = efficiency
                indexOf = i
                maxCps = cpsEach
            #print(f"{buildingName} CPS each: {cpsEach}")
            #print(f"{buildingName} price: {price}")
            #print(f"{buildingName} efficiency: {efficiency}")

        print(f"Best building efficiency: {maxEfficiency}")
        print(f"Best building: {driver.execute_script("return Game.ObjectsById[" + str(indexOf) + "].name")}")
        

        # check upgrades
        numUpgrades = driver.execute_script("return Game.UpgradesInStore.length")
        for i in range(numUpgrades):
            if (driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].pool") == "cookie"):
                # probably a % boost
                percent = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].desc").split()[3][4]
                price = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].getPrice()")
                cps = cpsRaw * (int(percent) / 100)
                efficiency = cps / price
                if (efficiency > maxEfficiency):
                    maxEfficiency = efficiency
                    indexOf = i
                    maxCps = cps
                    isUpgrade = 1
            if (driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].pool") == ""):
                buildingNum = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].buildingTie.id")
                amtBuilding = driver.execute_script("return Game.ObjectsById[" + str(buildingNum) + "].amount")
                buildingStoredTotalCps = driver.execute_script("return Game.ObjectsById[" + str(buildingNum) + "].storedTotalCps")
                cps = (globalMul * buildingStoredTotalCps) / amtBuilding
                price = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].getPrice()")
                efficiency = cps / price
                if (efficiency > maxEfficiency):
                    maxEfficiency = efficiency
                    indexOf = i
                    maxCps = cps
                    isUpgrade = 1
                print(efficiency)
        
        print(f"Best efficiency overall: {maxEfficiency}")
        if (isUpgrade):
            print(f"Best thing: {driver.execute_script("return Game.UpgradesInStore[" + str(indexOf) + "].name")}")
        else:
            print(f"Best thing: {driver.execute_script("return Game.ObjectsById[" + str(indexOf) + "].name")}")
        print(f"% cps added: {(maxCps / cpsRaw) * 100}%")
        sleep(10)  # Update every 60 second


except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
