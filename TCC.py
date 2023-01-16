import json
import random
from tracemalloc import Statistic
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass
import statistics as stats




def gerador_Dados(nro_Nodos,nro_Links,nro_Req):

    funcao = {}
    requisicoes = {}
    '''
    for i in range (0,4):
    
        randval= random.randint(2,10)
        BRAM=randval*64
        DSP=random.randint(0,4)
        Lat=random.randint(100,200)
        Thro=random.randint(10,100)
        implementacoes[i] = {
        "nome" : "I" + str(i),
        "CLBs" : randval,
        "BRAM" : BRAM,
        "DSPs" : DSP,
        "Lat" : Lat,
        "Throughput": Thro
        }
    '''
    implementacoes=[{
        "nome" : "FW0",
        "CLBs" : 1150,
        "BRAM" : 5,
        "DSPs" : 0,
        "Lat" : 4.2,
        "Throughput": 2.9},
        {
        "nome" : "FW1",
        "CLBs" : 8537,
        "BRAM" : 1,
        "DSPs" : 0,
        "Lat" : 23,
        "Throughput": 2},
        {
        "nome" : "FW2",
        "CLBs" : 8123,
        "BRAM" : 241,
        "DSPs" : 0,
        "Lat" : 73,
        "Throughput": 92.16},
        {
        "nome" : "DPI0",
        "CLBs" : 8377,
        "BRAM" : 37,
        "DSPs" : 0,
        "Lat" : 278,
        "Throughput": 0.8},
        {
        "nome" : "DPI1",
        "CLBs" : 8612,
        "BRAM" : 438,
        "DSPs" : 0,
        "Lat" : 2778,
        "Throughput": 0.8},
        {
        "nome" : "DPI2",
        "CLBs" : 15206,
        "BRAM" : 36,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 14.4},
        {
        "nome" : "DPI3",
        "CLBs" : 5154,
        "BRAM" : 407,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 40},
        {
        "nome" : "DPI4",
        "CLBs" : 713,
        "BRAM" : 96,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 40},
        {
        "nome" : "DPI5",
        "CLBs" : 6048,
        "BRAM" : 399,
        "DSPs" : 0,
        "Lat" : random.randint(278,2778),
        "Throughput": 102.6},
         {
        "nome" : "AES0",
        "CLBs" : 2532,
        "BRAM" : random.randint(1,5),
        "DSPs" : 0,
        "Lat" : random.randint(2,21),
        "Throughput": 49.38},
        {
        "nome" : "AES1",
        "CLBs" : random.randint(2000,3000),
        "BRAM" : 2,
        "DSPs" : 0,
        "Lat" : 21,
        "Throughput": 1.054},
        {
        "nome" : "AES2",
        "CLBs" : 4095,
        "BRAM" : random.randint(1,5),
        "DSPs" : 0,
        "Lat" : 2,
        "Throughput": 59.3},
        {
        "nome" : "AES3",
        "CLBs" : 2034,
        "BRAM" : random.randint(1,5),
        "DSPs" : 0,
        "Lat" : random.randint(2,21),
        "Throughput": 45},
        {
        "nome" : "AES4",
        "CLBs" : 9561,
        "BRAM" : 450,
        "DSPs" : 0,
        "Lat" : random.randint(2,21),
        "Throughput": 119.3}
    ] #descricao de valores de diferentes implementacoes de funcoes

    


    nro_Func=random.randint(9,12)
    
    for j in range (nro_Func):
        sort_Func=random.randint(0,len(implementacoes)-1)
        if implementacoes[sort_Func]["nome"][0]=='F':
            nome='Firewall'
        elif implementacoes[sort_Func]["nome"][0]=='D':
            nome='Deep Packet Inspection'
        elif implementacoes[sort_Func]["nome"][0]=='A':
            nome='Advanced Encryption Standard'
        funcao[j] = {
            "Nome": nome,
            "implementacao": implementacoes[sort_Func]
            }

    for k in range (0,nro_Req):
        rand_fun=random.randint(0,nro_Func-1)
        rand_nodo_S=random.randint(0,nro_Nodos-1)
        rand_nodo_D=random.randint(0,nro_Nodos-1)
        while rand_nodo_S==rand_nodo_D:
            rand_nodo_D=random.randint(0,nro_Nodos)
        
        aux=funcao[rand_fun]["implementacao"]
        valor=(aux['CLBs']+(aux['BRAM']*10))/50
        valor=valor *random.uniform(0.9,1.1)

        requisicoes[k] = {
            "Nodo_S": rand_nodo_S,
            "Nodo_D": rand_nodo_D,
            "max_Lat": aux["Lat"],
            "min_T": aux["Throughput"],
            "funcao": funcao[random.randint(0,rand_fun)],
            "valor": valor
            }

    G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    '''
    #visualiza grafico em tela

    #subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show() 

    '''
    lista=list(G.edges)


    topologia_rede=[]

    fpga=[[54240,480,1368],[210600,1728,1080],[268560,2520,2880]]
    

    for a in range(0,nro_Nodos):
        lista_Fpga=[]
        lista_Links=[]
        
        for b in lista:
            nodoS = b[0]
            nodoD = b[1]
            if nodoD == a:
                lista_Links.append(nodoS)
            if nodoS == a:
                lista_Links.append(nodoD)

        for c in range(0,len(lista_Links)):
            thro=random.randint(100,1000)
            lat= random.randint(5,200)
            lista_Links[c]={lista_Links[c]: {"Lat": lat, "Throughput": thro}}
       

        nro_fpga=random.randint(0,3)
        if nro_fpga!=0:
            
            for i in range(nro_fpga):

                lista_Part=[]
                sort_Fpga=random.randint(0,2)
                size_CLB = fpga[sort_Fpga][0]
                size_BRAM= fpga[sort_Fpga][1]
                size_DSP= fpga[sort_Fpga][2]

                max_CLB=15200
                max_BRAM=450

                nro_parts=random.randint(1,4)
                if sort_Fpga==0 and nro_fpga ==1:
                    clb=54240
                    bram=480
                    dsp=1368
                    lista_Part.append({"Part0": {"CLBs": clb, "BRAM":bram, "DSP": dsp }})
                    list(lista_Part)
                    continue

                for part in range(nro_parts):
                    if size_CLB-max_CLB <= max_CLB:
                        clb=size_CLB
                    else:
                        clb=max_CLB
                        size_CLB-=max_CLB
                         
                    if size_BRAM-max_BRAM<=max_BRAM:
                        bram=size_BRAM
                    else:
                        bram=max_BRAM
                        size_BRAM-=max_BRAM

                    dsp=int(size_DSP/nro_parts)
                    lista_Part.append({"Part"+str(part): {"CLBs": clb, "BRAM":bram, "DSP": dsp }})
                    list(lista_Part)
                lista_Fpga.append(lista_Part)
                

            
        
        topologia_rede.append({"Nodo"+str(a): {"FPGA": lista_Fpga, "Links": lista_Links}})
     
    with open ("requisicoes.json","w") as outfile:
        json.dump(requisicoes, outfile)

    with open ("funcoes.json","w") as outfile:
        json.dump(funcao, outfile)

    with open ("implementacoes.json","w") as outfile:
        json.dump(implementacoes, outfile)

    with open ("topologia.json","w") as outfile:
        json.dump(topologia_rede, outfile)




def dfs_caminhos(grafo, inicio, fim):
    pilha = [(inicio, [inicio])]
    while pilha:
        vertice, caminho = pilha.pop()
        for proximo in set(grafo[vertice]) - set(caminho):
            if proximo == fim:
                yield caminho + [proximo]
            else:
                pilha.append((proximo, caminho + [proximo]))

@dataclass
class Function:
    name_func:str
    name_imp:str
    clb:int
    bram:int
    dsp:int

@dataclass
class Req:
    init_node:str
    out_node:str
    max_Lat:int
    min_T:int
    func:Function
    price:float

@dataclass
class Partition:
    clb:int
    bram:int
    dsp:int

@dataclass
class Link:
    nodo_d: str
    max_Lat: int
    min_T: int

@dataclass
class Node:
    fpga:Partition
    link: Link


def ler_Dados():
    with open("requisicoes.json") as file1:
        requisicoes = json.load(file1)


    with open("topologia.json") as file2:
        topologia = json.load(file2)
    

    nodos=[]
    parts=[]
    links=[]
    lista_Caminhos=[]
    caminhos=[]
    lista_Fpga=[]
    lista_Req=[]
    lista_Nodos=[]
   
    
    

    for i,v in enumerate(topologia):
        
        nodos.append(str(*v.keys()))
        fpgas=(v[nodos[i]]["FPGA"])
        links=(v[nodos[i]]["Links"])
        caminhos=[]
        lista_Links=[]

        for j in links:
            nodo_d=str(*j.keys())   
            lat=j[nodo_d]["Lat"]
            thro=j[nodo_d]["Throughput"]
            const_Link=Link(nodo_d,lat,thro)
            lista_Links.append(const_Link)
            caminhos.append(int(nodo_d))
        lista_Caminhos.append(caminhos)

        for fpga in fpgas:
            
            for part in fpga:
                lista_Parts=[]
                nodo=str(*part.keys())
            
                clb=part[nodo]["CLBs"]
                bram=part[nodo]["BRAM"]
                dsp=part[nodo]["DSP"]
                const_Part=Partition(clb,bram,dsp)
                lista_Parts.append(const_Part)
                list(lista_Parts)
            lista_Fpga.append(lista_Parts)
            
        const_Nodo=Node(lista_Fpga,lista_Links)
        print(const_Nodo)
        lista_Nodos.append(const_Nodo)
                    
    for a,val in enumerate(requisicoes.values()):
        nodo_S=val["Nodo_S"]
        nodo_D=val["Nodo_D"]
        lat=val["max_Lat"]
        thro=val["min_T"]
        nome_F=val["funcao"]["Nome"]
        imp=val["funcao"]["implementacao"]
        valor=val["valor"]
        nome_I=imp["nome"]
        clb=imp["CLBs"]
        bram=imp["BRAM"]
        dsp=imp["DSPs"]
        lat=imp["Lat"]
        thro=imp["Throughput"]
        c_Func=Function(nome_F,nome_I,clb,bram,dsp)
        c_Req=Req(nodo_S,nodo_D,lat,thro,c_Func,valor)
        lista_Req.append(c_Req)

    return lista_Req,lista_Caminhos,lista_Nodos


def wrong_Run(lista_Nodos):
    print(lista_Nodos)
    lista_Fpga=[]
    for nodo in lista_Nodos:
        for fpga in nodo.fpga:
            clb=0
            bram=0
            dsp=0
            for part in fpga:
                clb+=part.clb
                bram+=part.bram
                dsp+=part.dsp
            lista_Fpga.append([clb,bram,dsp])

    print(lista_Fpga)
    print("Esta quase pronto")





def check_Path(node_D,nodos,req):
    valid_Path=0
    new_Thro=None
    
    for nodo in nodos:
        if int(nodo.nodo_d)==node_D:
            if nodo.max_Lat<=req.max_Lat:
                if nodo.min_T>=req.min_T:
                    new_Thro=nodo.min_T-req.min_T
                    valid_Path=1
                    
    return [valid_Path,node_D,new_Thro]
#checa se o caminho do nodo inicial at� o final � v�lido em rela��o a lat�ncia e vaz�o





def greedy(lista_Req,lista_Paths,lista_Nodos):
    aloc_Req=[]
    cash=0
    for req in lista_Req:
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        check_Node=False
        check_Link=1
        refresh_Links=[]
        

        if lista_Nodos[req.init_node].fpga!=0:
            for a,parts in enumerate(lista_Nodos[req.init_node].part):
                if parts.clb>=req.func.clb:
                    if parts.bram>=req.func.bram:
                        if parts.dsp>=req.func.dsp:
                            check_Node=True
                            break

        for p in path_Ord:
            for b,c in zip(p,p[1:]):
                lista_Check=check_Path(c,lista_Nodos[b].link,req)
                check_Link+=lista_Check[0]
                aux_Lista=b,lista_Check[1],lista_Check[2]
                refresh_Links.append(aux_Lista)
            if check_Link==len(p):
                check_Link=True
                break
            else:
                check_Link=False
        
        if check_Link and check_Node:
            
            aloc_Req.append(req)
            lista_Nodos[req.init_node].part.pop(a)
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (lista_Nodos[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
            cash+=req.price


    ratio=len(aloc_Req)/len(lista_Req)


        
    #print("Requisicoes alocadas:",aloc_Req)
    print("Nr requisicoes alocadas:",len(aloc_Req),"\nRatio:",round(ratio,2),"%")

    return(len(aloc_Req), aloc_Req, cash)
    

    


                            

        





lista_Results={}
dataset_1=[]
dataset_2=[]
dataset_3=[]
aloc_Desv=[]
valor_Desv=[]


modo=input("1- Testar unitario\n2- Teste em escala\n")

if modo == '1':
    nodos_G=int(input("Numero de nodos da rede:\n"))
    links_G=int(input("Numero de links da rede:\n"))
    req=int(input("Numero de requisicoes:\n"))
    gerador_Dados(nodos_G, links_G,req)
    lista_Req,lista_Paths,lista_Nodos=ler_Dados()
    wrong_Run(lista_Nodos)
    #greedy(lista_Req,lista_Paths,lista_Nodos)

else:


    for index in range (5,45,5):
        req_Aloc=[]
        valor_Final=[]
        for cont in range(50):
            size=index
            nodos_G=size
            links_G=int(size*1.2)
            req=random.randint(int(size*1.5),int(size*3))
            gerador_Dados(nodos_G, links_G,req)
            lista_Req,lista_Paths,lista_Nodos=ler_Dados()
            results=greedy(lista_Req,lista_Paths,lista_Nodos)
            lista_Results.update({
                "Teste"+str(index):{
                "Lista Requisicoes": len(lista_Req),
                "Requiscoes alocadas": results[0]},
                "Nodos": len(lista_Nodos),
                "Valor": results[2]
                })

            req_Aloc.append(results[0])
            valor_Final.append(results[2])

        aloc_Desv.append(stats.pstdev(req_Aloc))
        valor_Desv.append(stats.pstdev(valor_Final))
        dataset_1.append(index)
        dataset_2.append(stats.mean(req_Aloc))
        dataset_3.append(stats.mean(valor_Final))

    with open ("Req Alocadas.json","w") as outfile:
        json.dump(lista_Results, outfile)

    '''
    test=zip(dataset_1,dataset_2,dataset_3)
    lista_test=list(sorted(test, key=lambda teste: teste[0]))
    dataset_1,dataset_2,dataset_3 = zip(*lista_test)
    '''

    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot(dataset_1, dataset_2,color='tab:green') 
    ax.errorbar(dataset_1, dataset_2, yerr=aloc_Desv, fmt="go")
    ax2 = ax.twinx() 
    ax2.plot(dataset_1, dataset_3, color = 'tab:red') 
    ax2.errorbar(dataset_1, dataset_3, yerr=valor_Desv,fmt='ro')
    plt.title('Numero de funcoes alocadas', fontweight="bold") 
    ax.grid() 
    ax.set_xlabel("Numero de Nodos") 
    ax.set_ylabel(r"Requisicoes alocadas",color='tab:green') 
    ax2.set_ylabel(r"Valor($)", color='tab:red') 
    ax2.set_ylim(0, 10000) 
    ax.set_ylim(0, 100)
    
    
    plt.show() 








