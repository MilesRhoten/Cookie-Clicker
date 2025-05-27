from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Set up Chrome options to use your existing user profile

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\localadmin\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"--profile-directory=Profile 1")

options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


# Set up the WebDriver (Make sure 'chromedriver' is in PATH)
service = Service(r"C:\Users\localadmin\Downloads\chromedriver-win64(1)\chromedriver-win64\chromedriver.exe")  # Update this path
driver = webdriver.Chrome(service=service, options=options)
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
        
        buildingEff1 = 0
        buildingEff2 = 0
        ioBuilding1 = 0
        ioBuilding2 = 0

        upgradeEff1 = 0
        upgradeEff2 = 0
        ioUpgrade1 = 0
        ioUpgrade2 = 0


        # check buildings
        for i in range(20):
            buildingStoredTotalCps = driver.execute_script("return Game.ObjectsById[" + str(i) + "].storedTotalCps")
            buildingName = driver.execute_script("return Game.ObjectsById[" + str(i) + "].name")
            amtBuilding = driver.execute_script("return Game.ObjectsById[" + str(i) + "].amount")
            price = driver.execute_script("return Game.ObjectsById[" + str(i) + "].price")
            name = driver.execute_script("return Game.ObjectsById[" + str(i) + "].name")
            cpsEach = (globalMul * buildingStoredTotalCps) / amtBuilding
            efficiency = (cpsEach / price)
            
            #print(name)
            #print("Efficiency", efficiency)
            #print("buildingEff1", buildingEff1)
            #print("buildingEfff2", buildingEff2)

            # check to beat both
            if (efficiency >= buildingEff1):
                # move 1 to 2
                buildingEff2 = buildingEff1
                ioBuilding2 = ioBuilding1

                buildingEff1 = efficiency
                ioBuilding1 = i
            elif (efficiency >= buildingEff2):
                buildingEff2 = efficiency
                ioBuilding2 = i

            #print("building 1",ioBuilding1)
            #print("building 2", ioBuilding2)
            
            
            


            #print(f"{buildingName} CPS each: {cpsEach}")
            #print(f"{buildingName} price: {price}")
            #print(f"{buildingName} efficiency: {efficiency}")

        # check upgrades
        numUpgrades = driver.execute_script("return Game.UpgradesInStore.length")
        for i in range(numUpgrades):
            if (driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].pool") == "cookie"):
                # probably a % boost
                percent = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].desc").split()[3][4]
                price = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].getPrice()")
                cps = cpsRaw * (int(percent) / 100)
                efficiency = cps / price
                # check to beat both
                if (efficiency > upgradeEff1):
                    # move 1 to 2
                    upgradeEff2 = upgradeEff1
                    ioUpgrade2 = ioUpgrade1

                    upgradeEff1 = efficiency
                    ioUpgrade1 = i
                elif (efficiency > upgradeEff2):
                    upgradeEff2 = efficiency
                    ioUpgrade2 = i


            if (driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].pool") == ""):
                buildingNum = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].buildingTie.id")
                amtBuilding = driver.execute_script("return Game.ObjectsById[" + str(buildingNum) + "].amount")
                buildingStoredTotalCps = driver.execute_script("return Game.ObjectsById[" + str(buildingNum) + "].storedTotalCps")
                cps = (globalMul * buildingStoredTotalCps) / amtBuilding
                price = driver.execute_script("return Game.UpgradesInStore[" + str(i) + "].getPrice()")
                efficiency = cps / price
                # check to beat both
                if (efficiency > upgradeEff1):
                    # move 1 to 2
                    upgradeEff2 = upgradeEff1
                    ioUpgrade2 = ioUpgrade1

                    upgradeEff1 = efficiency
                    ioUpgrade1 = i
                elif (efficiency > upgradeEff2):
                    upgradeEff2 = efficiency
                    ioUpgrade2 = i
        
        
        print(f"Best Upgrade: {driver.execute_script("return Game.UpgradesInStore[" + str(ioUpgrade1) + "].name")}")
        print(f"2nd Best Upgrade: {driver.execute_script("return Game.UpgradesInStore[" + str(ioUpgrade2) + "].name")}")

        
        print(f"Best Building: {driver.execute_script("return Game.ObjectsById[" + str(ioBuilding1) + "].name")}")
        print(f"2nd Best Building: {driver.execute_script("return Game.ObjectsById[" + str(ioBuilding2) + "].name")}")
        

        if (buildingEff1 >= upgradeEff1):
            print(f"Building better")
        else:
            print(f"Upgrade better")


        sleep(10)  # Update every 60 second


except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
