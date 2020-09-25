
def clickID(id,driver):
    while True:
        try:
            btn = driver.find_element_by_id("anchor-acessar")
            btn.click()
            break
        except:
            # print('Tentando clicar..')
            pass

def clickXPath(xpah,driver):
    while True:
        try:
            btn = driver.find_element_by_xpath(xpah)
            btn.click()
            break
        except:
            # print('Tentando clicar..')
            pass

def clickClass(clas,driver):
    while True:
        try:
            btn = driver.find_element_by_class_name(clas)
            btn.click()
            break
        except:
            # print('Tentando clicar..')
            pass