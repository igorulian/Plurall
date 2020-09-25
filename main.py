from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import time
import crendentials
from buttons import clickClass
from buttons import clickXPath
import os


link_da_apostial = 'https://atividades.plurall.net/material/2748190/'

forcar_bloco = 0
forcar_tarefa = 0

option = Options()
option.headless = False

driver = webdriver.Firefox(executable_path=r'C:\Users\Particular\Documents\GeckoDriver\geckodriver.exe', options=option)

def logar():
    print("Autenticando...")
    driver.get('https://login.plurall.net/login')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(crendentials.email)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(crendentials.passw)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(Keys.ENTER)
    print("Autenticado com sucesso ✔️")
    print("   ")
    time.sleep(1)

def seguirParaApostila():
    print("Seguindo para area da apostila...")
    driver.get(link_da_apostial)
    time.sleep(2)


def verificarAcerto(link_da_questao):
    print("Verificando acerto...")
    try:
        print("Clicando em tentar novamente...")
        btn_agr_nao = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/span/div[4]/button")
        btn_agr_nao.click()
        return False
    except:
        try:
            # clica para
            print("Clicando para ler a apostila...")
            time.sleep(2)
            btn_tire_sua_duvida = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/span/div[1]/a/div")

            ActionChains(driver).key_down(Keys.CONTROL).click(btn_tire_sua_duvida).key_up(Keys.CONTROL).perform()
            # btn_tire_sua_duvida.click()
            time.sleep(1.5)
            driver.switch_to_window(driver.window_handles[1])
            driver.close()

            driver.switch_to_window(driver.window_handles[0])
            return False
        except:
            return True
        
        return True

def verificarQuestaoDiscursiva():
    print("Verificando questão discursiva....")
    try:
        time.sleep(1)
        #driver.find_element_by_tag_name("textarea")
        driver.find_element_by_xpath("//*[contains(text(),'Enviar resposta')]")
        return True
    except:
        return False

def lerOTrem(link_da_questao):
    
    #Ler o trem
    print("Lendo o trem...")

    time.sleep(1.5)
    try:   
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div/section/section/a/div").click()       
        time.sleep(2)
    except:
        print("Trem não encontrado")
    
    #Volta para area das questoes
    print("Voltando para area de questões...")

    driver.get(link_da_questao)

def getQuantidadeDeQuestoes():
    questoes = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[3]")
    questoes = questoes.get_attribute('innerHTML').split(" ")

    quantidade_de_questoes = 0

    for x in range(len(questoes)):
        if "<a" in questoes[x]:
            quantidade_de_questoes = quantidade_de_questoes + 1
    return quantidade_de_questoes


def getQuantidadeDeQuestoesSecaoExercicios():
    questoes = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[5]")
    questoes = questoes.get_attribute('innerHTML').split(" ")

    quantidade_de_questoes = 0

    for x in range(len(questoes)):
        if "<a" in questoes[x]:
            quantidade_de_questoes = quantidade_de_questoes + 1
    return quantidade_de_questoes


def verificarSecaoDeExercicios():
    print("Verificando sessão de execicios")
    time.sleep(0.5)
    try:
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[5]")
        return True
    except:
        return False


def resolverQuestaoDiscursiva():
    ## manda discursiva
    print("Questao Discursiva identificada!")
    print("Mandando resposta...")
    # digitar resposta
    driver.find_element_by_tag_name("textarea").send_keys("feito")
    time.sleep(1)

    btn = driver.find_element_by_xpath("//*[contains(text(),'Enviar resposta')]")
    btn.click()

    # confirmar
    time.sleep(1)
    btn_confirmar = driver.find_element_by_xpath("//*[contains(text(),'confirmar')]")
    btn_confirmar.click()

    print('Resposta discursiva enviada! ✔️')


def resolverQuestao(x):

    #Verificar Disponibilidade 
    print("    ")
    print("   Veriricando Disponibilidade Da Questão...")
    try:
        driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[3]/a[{x}]/div[@class="jsx-2800942400 exercise-card correct"]')
        print("   Resposta ja correta, seguindo para proxima...")
        return
    except:
        pass

    try:
        driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[3]/a[{x}]/div[@class="jsx-2800942400 exercise-card wrong"]')
        print("   Resposta ja incorreta, seguindo para proxima...")
        return
    except:
        pass

    #Clicar na questão
    clickXPath(f'/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[3]/a[{x}]', driver)

    # Chutar
    chutes_efetuados = []

    for y in range(1,4):
        time.sleep(2)

        if verificarQuestaoDiscursiva():
            resolverQuestaoDiscursiva()
            break

        #Resolver questão multipla escolha
        print(f'    Efetuado chute.. {y}')
        chutes_efetuados.append(y)
        driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div/section[1]/div[2]/div/div/div/ul/li[{y}]/span[1]')                 
        clickXPath(f'/html/body/div[1]/div[2]/div/div[3]/div/section[1]/div[2]/div/div/div/ul/li[{y}]/span[1]',driver)
        print(f'    Chute {y} efetuado!')

        time.sleep(2)

        if verificarAcerto(driver.current_url):
            print('    Resposta correta! ✔️')
            break
        else:
            print('    Resposta incorreta! ❌')


def resolverQuestaoSessaoDeExercicios(x):

    #Verificar Disponibilidade 
    print("    ")
    print("   Veriricando Disponibilidade Da Questão de exercicio...")
    try:
        driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[5]/a[{x}]/div[@class="jsx-2800942400 exercise-card correct"]')
        print("   Resposta ja correta, seguindo para proxima...")
        return
    except:
        pass

    try:                            
        driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[5]/a[{x}]/div[@class="jsx-2800942400 exercise-card wrong"]')
        print("   Resposta ja incorreta, seguindo para proxima...")
        return
    except:
        pass

    #Clicar na questão
    clickXPath(f'/html/body/div[1]/div[2]/div/div[3]/div/section/div/div[5]/a[{x}]', driver)

    # Chutar
    chutes_efetuados = []

    for y in range(1,4):
        time.sleep(2)

        if verificarQuestaoDiscursiva():
            resolverQuestaoDiscursiva()
            break

        #Resolver questão multipla escolha
        print(f'    Efetuado chute.. {y}')
        chutes_efetuados.append(y)
        driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div/section[1]/div[2]/div/div/div/ul/li[{y}]/span[1]')    
        clickXPath(f'/html/body/div[1]/div[2]/div/div[3]/div/section[1]/div[2]/div/div/div/ul/li[{y}]/span[1]',driver)
        print(f'    Chute {y} efetuado!')

        time.sleep(2)

        if verificarAcerto(driver.current_url):
            print('    Resposta correta! ✔️')
            break
        else:
            print('    Resposta incorreta! ❌')

def resolverTarefa(bloco,tarefa):   

    ##===                  
    print("  Selecionando a Tarefa...")

    #Selecionar t/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/section/section[1]
    clickXPath(f'/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[{bloco}]/section/section[{tarefa}]',driver)
    link_da_questao = driver.current_url
    time.sleep(1)

    lerOTrem(link_da_questao)

    ## Pegar quant de questões
    try:
        quantidade_de_questoes = getQuantidadeDeQuestoes()
            
        print(f'  Quantidade de questões: {quantidade_de_questoes}')

        print("  Começando a resolver as questões..") 
        time.sleep(1)

        #Começar a resolver questão
        for questao_x in range(1,quantidade_de_questoes + 1):
            time.sleep(1)
            print(f'  Começando a resolver a questao {questao_x}')

            driver.get(link_da_questao)
            resolverQuestao(questao_x)

        driver.get(link_da_questao)

        if verificarSecaoDeExercicios():
            # /html/body/div[1]/div[2]/div/div[3]/div/section/div/div[5]
            print("   Sessão de exercicios identificada!")
            quantidade_de_questoes_sessao_exercico = getQuantidadeDeQuestoesSecaoExercicios()
            
            print(f'  Quantidade de questões: {quantidade_de_questoes_sessao_exercico}')

            print("  Começando a resolver as questões..") 
            time.sleep(1)

            #Começar a resolver questão
            for questao_x in range(1,quantidade_de_questoes_sessao_exercico + 1):
                time.sleep(1)
                print(f'  Começando a resolver a questao {questao_x}')

                driver.get(link_da_questao)
                resolverQuestaoSessaoDeExercicios(questao_x)
                pass
    except:
        print("   Nenhuma questão identificada, seguindo...")



def resolverBlocos():

    bloco_inicial = 1
    if forcar_bloco != 0:
        bloco_inicial = forcar_bloco

    tarefa_inicial = 1
    if forcar_tarefa != 0:
        tarefa_inicial = forcar_tarefa

    for bloco in range(bloco_inicial,100):
        seguirParaApostila()

        # for _ in rage(bloco * 10):
        #     # Scrolla para baixo

        print("Rolando pagina...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f'Começando a resolver bloco {bloco}...')

        #Scrolar
        print("Scrollando até o bloco...")

        for _ in range(int(bloco / 4)):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1.5)

        #Scrolar

        time.sleep(2)

        print("to no final da pagina?")

        bloquin = driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div[{bloco}]/section')
        bloquin = bloquin.get_attribute('innerHTML').split(" ")

        tarefas_dentro_do_bloquinho_y = 0

        for x in range(len(bloquin)):
            if "<section" in bloquin[x]:
                tarefas_dentro_do_bloquinho_y+= 1

        print(f'tarefas totais bloco {bloco}: {tarefas_dentro_do_bloquinho_y}')

        for tarefa in range(tarefa_inicial,tarefas_dentro_do_bloquinho_y + 1):
            print(f' Começando a resolver tarefa, bloco {bloco}; tarefa{tarefa}')
            seguirParaApostila()

            time.sleep(1)

            #Scrolar
            print("Scrollando até a tarefa...")

            for _ in range(int(bloco / 4)):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1.5)

            #Scrolar
            
            resolverTarefa(bloco,tarefa)

    
    

def start():
    os.system("clear")
    logar()
    seguirParaApostila()
    resolverBlocos()

start()