import json
import math
import random
import statistics as stats
from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx
import copy
import numpy as np




def gerador_Topologia(nro_Nodos, nro_Links):
    
    G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    
    while not(nx.is_connected(G)):
        G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    
    #visualiza grafico em tela
    
    subax1 = plt.subplot(121)
    nx.draw_circular(G, with_labels=True, font_weight='bold')
    
    plt.savefig('Grafo.png')
    #plt.show() 
    subax1.clear()
    
    lista=list(G.edges)

    topologia_rede=[]
    fpga=[]
    


    fpga=[[30300,600,1920],[67200,1680,768],[134280,3780,1800]]
    list_thro=[40,100,200,400]
    
    fpga_P=[
                {   "Modelo": 'P',
                    
                    "Part0": {
                        "CLBs": 22200,
                        "BRAM": 480,
                        "DSP": 1560
                    }
                },
                {   "Modelo": 'P',   
                 
                    "Part0": {
                        "CLBs": 10800,
                        "BRAM": 300,
                        "DSP": 600
                    },
                    "Part1": {
                        "CLBs": 10800,
                        "BRAM": 180,
                        "DSP": 600
                    },
                    "Part2": {
                        "CLBs": 2958,
                        "BRAM": 40,
                        "DSP": 240
                    }
                } 
            ]  
    fpga_M=[
            {       "Modelo": 'M',
             
                    "Part0": {
                        "CLBs": 19200,
                        "BRAM": 480,
                        "DSP": 192
                    },
                    "Part1": {
                        "CLBs": 20160,
                        "BRAM": 480,
                        "DSP": 192
                    },
                    "Part2": {
                        "CLBs": 10440,
                        "BRAM": 288,
                        "DSP": 144
                    },
                    
                    "Part3": {
                        "CLBs": 3060,
                        "BRAM": 108,
                        "DSP": 0
                    },
                    "Part4": {
                        "CLBs": 3060,
                        "BRAM": 144,
                        "DSP": 72
                    },
                    "Part5": {
                        "CLBs": 3060,
                        "BRAM": 72,
                        "DSP": 72
                    }
            }             
            ]
    fpga_G=[
        {           "Modelo": 'G',
         
                    "Part0": {
                        "CLBs": 19800,
                        "BRAM": 504,
                        "DSP": 288
                    },
                    "Part1": {
                        "CLBs": 19080,
                        "BRAM": 576,
                        "DSP": 288
                    },
                    "Part2": {
                        "CLBs": 22140,
                        "BRAM": 540,
                        "DSP": 216
                    },
                    
                    "Part3": {
                        "CLBs": 19440,
                        "BRAM": 540,
                        "DSP": 216
                    },
                    "Part4": {
                        "CLBs": 10980,
                        "BRAM": 288,
                        "DSP": 144
                    },
                    "Part5": {
                        "CLBs": 10800,
                        "BRAM": 360,
                        "DSP": 144
                    },
                    "Part6": {
                        "CLBs": 2940,
                        "BRAM": 72,
                        "DSP": 0
                    },
                    "Part7": {
                        "CLBs": 2940,
                        "BRAM": 72,
                        "DSP": 0
                    },
                    "Part8": {
                        "CLBs": 2940,
                        "BRAM": 84,
                        "DSP": 24
                    }
            }
        ]
                
    size_Fgpa=[fpga_P,fpga_M,fpga_G]

    for a in range(nro_Nodos):
        lista_Fpga=[]
        lista_Links=[]
        
        for b in lista:
            nodoS = b[0]
            nodoD = b[1]
            if nodoD == a:
                lista_Links.append(nodoS)
            if nodoS == a:
                lista_Links.append(nodoD)

        for c in range(len(lista_Links)):
            thro=random.choice(list_thro)
            lat= random.randint(20,200)
            lista_Links[c]={lista_Links[c]: {"Lat": lat, "Throughput": thro}}
       

        nro_fpga=random.randint(0,3)
        
        if nro_fpga!=0:
            lista_Part=[]
            for device in range(nro_fpga):
                
                
                sort_Fpga=random.choice(range(len(fpga)))
                
                lista_Part.append(random.choice(size_Fgpa[sort_Fpga]))
                
            lista_Fpga.append(lista_Part)
           
        topologia_rede.append({"Nodo"+str(a): {"FPGA": lista_Fpga, "Links": lista_Links}})
        
    with open ("topologia.json","w") as outfile:
        json.dump(topologia_rede, outfile, indent=4)


def check_Lat(nodo_S,nodo_D,lista_Paths,lista_Nodos): #checa menor lat dentre os caminhos possiveis
    
    path=list(dfs_caminhos(lista_Paths,nodo_S,nodo_D))
    path_Ord=sorted(path,key=len)
    menor_Lat=None
    
    for p in path_Ord:
        lat=None
        
        for b,c in zip(p,p[1:]):
            for nodo in lista_Nodos[b].link:
                if int(nodo.nodo_d)==c:
                    if lat==None:
                        lat=nodo.min_Lat
                    else:
                        lat=lat+nodo.min_Lat
        if menor_Lat==None:
            menor_Lat=lat
        
        if lat<menor_Lat:
            menor_Lat=lat
        
    return menor_Lat         
    

def gerador_Req(nro_Nodos,nro_Req):

    
    lista_Caminhos,lista_Nodos=ler_Topologia()
        
    funcao = {}
    requisicoes = {}

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
    
    for func in range (nro_Func):
        sort_Func=random.randint(0,len(implementacoes)-1)
        if implementacoes[sort_Func]["nome"][0]=='F':
            nome='Firewall'
        elif implementacoes[sort_Func]["nome"][0]=='D':
            nome='Deep Packet Inspection'
        elif implementacoes[sort_Func]["nome"][0]=='A':
            nome='Advanced Encryption Standard'
        funcao[func] = {
            "Nome": nome,
            "implementacao": implementacoes[sort_Func]
            }
        implementacoes[sort_Func]["CLBs"]=int(implementacoes[sort_Func]["CLBs"]*1.25) #considera que apenas 80% das clb são de fato utilizadas
    
    for index in range (nro_Req):
        rand_fun=random.randint(0,nro_Func-1)
        rand_nodo_S=random.randint(0,(nro_Nodos-1))
        rand_nodo_D=random.randint(0,(nro_Nodos-1))
        
        while rand_nodo_S==rand_nodo_D:
            rand_nodo_D=random.randint(0,nro_Nodos-1)
        
        aux=funcao[rand_fun]["implementacao"]
        valor=(aux['CLBs']+(aux['BRAM']*10))/50
        valor=int(valor*random.uniform(0.9,1.1))
        

        lat=check_Lat(rand_nodo_S,rand_nodo_D,lista_Caminhos, lista_Nodos)            
        
        requisicoes[index] = {
            "Id": index,
            "Nodo_S": rand_nodo_S,
            "Nodo_D": rand_nodo_D,
            "max_Lat": int(lat*1.3),
            "min_T": aux["Throughput"],
            "funcao": funcao[rand_fun],
            "valor": valor
            }

    with open ("requisicoes.json","w") as outfile:
        json.dump(requisicoes, outfile, indent=4)

    with open ("funcoes.json","w") as outfile:
        json.dump(funcao, outfile, indent=4)

    with open ("implementacoes.json","w") as outfile:
        json.dump(implementacoes, outfile, indent=4)

    
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
    id:int
    init_node:int
    out_node:int
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
    min_Lat: int
    max_T: int

@dataclass
class Node:
    id:str
    fpga:Partition
    link: Link


def ler_Requisicoes():
    
    with open("requisicoes.json") as file1:
        requisicoes = json.load(file1)
        
        
        
    lista_Req=[]
    
    for a,val in enumerate(requisicoes.values()):
        Id=val["Id"]
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
        c_Func=Function(nome_F,nome_I,clb,bram,dsp)
        c_Req=Req(Id,nodo_S,nodo_D,lat,thro,c_Func,valor)
        lista_Req.append(c_Req)
        
    return lista_Req


def ler_Topologia():
    


    with open("topologia.json") as file2:
        topologia = json.load(file2)
    

    nodos=[]
    links=[]
    lista_Caminhos=[]
    caminhos=[]
    lista_Nodos=[]


    for i,v in enumerate(topologia):
        
        nodos.append(str(*v.keys()))
        nodo_id=nodos[i]
        fpgas=(v[nodos[i]]["FPGA"])
        links=(v[nodos[i]]["Links"])
        caminhos=[]
        lista_Links=[]
        lista_Fpga=[]

        for l in links:
            nodo_d=str(*l.keys())   
            lat=l[nodo_d]["Lat"]
            thro=l[nodo_d]["Throughput"]
            const_Link=Link(nodo_d,lat,thro)
            lista_Links.append(const_Link)
            caminhos.append(int(nodo_d))
        lista_Caminhos.append(caminhos)

        
        for fpga in fpgas:
            
            for parts in fpga:
                lista_Parts=[]
                for part in parts:
                #id=str(*part.keys())
                    if part=='Modelo':
                        continue
                    clb=parts[part]["CLBs"]
                    bram=parts[part]["BRAM"]
                    dsp=parts[part]["DSP"]
                    const_Part=Partition(clb,bram,dsp)
                    lista_Parts.append(const_Part)
                lista_Fpga.append(lista_Parts)
            
        const_Nodo=Node(nodo_id,lista_Fpga,lista_Links)
        
        lista_Nodos.append(const_Nodo)
                    
    

    return lista_Caminhos,lista_Nodos


def wrong_Run(lista_Req,lista_Paths,lista_Nodos):
    
    lista_Fpga=[]
    for nodo in lista_Nodos:
        for fpga in nodo.fpga:
            clb=0
            bram=0
            dsp=0
            nodo_id=nodo.id
            for part in fpga:
                clb+=part.clb
                bram+=part.bram
                dsp+=part.dsp
            if int(clb/110000)==1:
                modelo=3
            elif int(clb/58000)==1:
                modelo=2
            elif int(clb/22000)==1:
                modelo=1
            lista_Fpga.append([nodo_id,modelo,clb,bram,dsp])
            
            
    
    with open ("topologia_wrong.json","w") as outfile:
        json.dump(lista_Fpga, outfile, indent=4)       
            
    aloc_Req=[]
    
    for nr_req,req in enumerate(lista_Req):
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        check_Node=False
        check_Link=1
        refresh_Links=[]
        device_id=None
        
        
        for caminho in path_Ord:
            
            check_Node=False
            check_Link=1
            for nodo in caminho:
                
                for i,device in enumerate(lista_Fpga):
                    if device[0]=='Nodo'+str(nodo):
                        if device[2]>=req.func.clb:
                            if device[3]>=req.func.bram:
                                if device[4]>=req.func.dsp:
                                    check_Node=True
                                    device_id=i  
                                    break            
                                #checa se fpga tem recursos para alocar requisicao
                if check_Node==True:
                    break
        
            for b,c in zip(caminho,caminho[1:]):
                lista_Check=check_Path(c,lista_Nodos[b].link,req)
                check_Link+=lista_Check[0]
                aux_Lista=b,lista_Check[1],lista_Check[2]
                refresh_Links.append(aux_Lista)
            if check_Link==len(caminho):
                check_Link=True
                break
            else:
                check_Link=False
        #checa se caminho tem capacidade de throughput
        
        if check_Link and check_Node:
            
            aloc_Req.append([req,device[1],i])
            lista_Fpga[device_id][2]=lista_Fpga[device_id][2]-req.func.clb
            lista_Fpga[device_id][3]=lista_Fpga[device_id][3]-req.func.bram
            lista_Fpga[device_id][4]=lista_Fpga[device_id][4]-req.func.dsp
            
            
            
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (lista_Nodos[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
        #se link e recursos satisfazem os requisitos, req eh alocada e atualiza-se recursos consumidos
    
    ratio=len(aloc_Req)/len(lista_Req)
    
    #print("Nr requisicoes alocadas W:",len(aloc_Req),"\nRatio:",round(ratio,2),"%")
    
    
    
    return(len(aloc_Req), aloc_Req)
#executa o algoritmo guloso pela visão '

def check_Path(node_D,nodos,req):
    valid_Path=0
    new_Thro=None
    
    for nodo in nodos:
        if int(nodo.nodo_d)==node_D:
            if nodo.min_Lat<=req.max_Lat:
                if nodo.max_T>=req.min_T:
                    new_Thro=nodo.max_T-req.min_T
                    valid_Path=1
                    
    return [valid_Path,node_D,new_Thro]
#checa se o caminho do nodo inicial ate o final eh valido em relacao a latencia e vazio

def check_Parts(devices, requisition):
    
    
    pesos=[]
    
    weight_clb=1
    weight_bram=50
    weight_dsp=20
    
    for fpga,partitions in enumerate(devices):
        if len(partitions)==0: 
            return False
        for index_part,part in enumerate(partitions):
            total_weight=0
            
            if part.clb-requisition.func.clb<0:
                continue
            if part.bram-requisition.func.bram<0:
                continue
            if part.bram-requisition.func.bram<0:
                continue
            total_weight=(part.clb-requisition.func.clb)*weight_clb
            total_weight+=(part.bram-requisition.func.bram)*weight_bram
            total_weight+=(part.dsp-requisition.func.dsp)*weight_dsp
            pesos.append([total_weight,fpga,index_part])
            
    if len(pesos)==0: 
            return False    
    
    
    min_value = min(pesos, key=lambda sublist: sublist[0])
    
    return(min_value) 
#Checa por partição que aloca melhor a req     

def check_Wrong(aloc_Req,lista_Paths):
    
    with open("topologia_wrong.json") as file:
        topologia = json.load(file)
    
       
    #fpga=[[30300,600,1920],[67200,1680,768],[134280,3780,1800]]
      
    aloc_W=[]
    
    for req in aloc_Req:
        path=list(dfs_caminhos(lista_Paths,req[0].init_node,req[0].out_node))
        path_Ord=sorted(path,key=len)
        
        not_valid=True
        min_Tile_clb=math.ceil(req[0].func.clb/60)
        min_Tile_bram=math.ceil(req[0].func.bram/12)
        
        for id,device in enumerate(topologia):
            
            for path in path_Ord:
                for nodo in path:
                    
                    if device[0]!="Nodo"+str(nodo) or device[1]==0:
                        continue

                    dispositivo=device
                    
                    min_Clb=0
                    min_Bram=0
                        
                    if dispositivo[1]==1:
                        divisor=5
                        min_Tile=5
                    elif dispositivo[1]==2:
                        divisor=8
                        min_Tile=3
                    elif dispositivo[1]==3:
                        divisor=15
                        min_Tile=2
                        
                    comparador=0
                    
                    #checa por numero de CLB
                    for linha in range(divisor,0,-1):
                        if min_Tile_clb%linha == 0 and min_Tile_clb<(dispositivo[2]*(linha/divisor)):
                            for index in range(0,int(min_Tile_clb/linha),10):            
                                min_Bram+=linha
                            melhor=0
                            break
                        else:
                            if comparador==0:
                                comparador=(min_Tile_clb%linha) / linha
                                
                            else:
                                if comparador>((min_Tile_clb%linha) / linha):
                                    comparador=(min_Tile_clb%linha) / linha
                                    melhor=linha              #checa por menor ratio entre coluna/linha, priorizando colunas maiores
                    if melhor!=0:
                        for index in range(0,int(min_Tile_clb/melhor),10):            
                            min_Bram+=melhor
                        linha=melhor
                    
                    part=[linha,math.ceil(min_Tile_clb/linha)]
                    
                    comparador=0
                    #checa por numero de BRAM
                    for linha in range(divisor,0,-1):
                        
                        if min_Tile_bram%linha == 0 and min_Tile_bram<(dispositivo[3]*(linha/divisor)):
                            for index in range(0,int(min_Tile_bram/linha),min_Tile):            
                                min_Clb+=linha
                            melhor=0
                            break
                        else:
                            if comparador==0:
                                comparador=(min_Tile_bram%linha) / linha
                                
                            else:
                                if comparador>((min_Tile_bram%linha) / linha):
                                    comparador=(min_Tile_bram%linha) / linha
                                    melhor=linha              #checa por menor ratio entre coluna/linha, priorizando colunas maiores
                    if melhor!=0:
                        for index in range(0,int(min_Tile_bram/melhor),min_Tile):            
                            min_Clb+=melhor
                        linha=melhor
                    
                    
                    if dispositivo[2]-min_Tile_bram<0 or dispositivo[3]-min_Tile_bram<0:
                        continue
                    
                    else:
                        if min_Bram>=min_Tile_bram or min_Clb>=min_Tile_clb:
                            if part[0]>=linha: 
                                min_Clb=part[0]*math.ceil(min_Tile_clb/part[0])*60
                                min_Bram=part[0]*math.ceil(min_Tile_bram/part[0])*12
                                topologia[id][2]=topologia[id][2]-min_Clb
                                topologia[id][3]=topologia[id][3]-min_Bram
                                not_valid = False
                                break
                            else:
                                min_Clb=linha*math.ceil(min_Tile_clb/linha)*60
                                min_Bram=linha*math.ceil(min_Tile_bram/linha)*12
                                topologia[id][2]=topologia[id][2]-min_Clb
                                topologia[id][3]=topologia[id][3]-min_Bram
                                not_valid = False
                                break
                            
                if not_valid == False:
                    break
            if not_valid == False:
                    break
                                               
                    
                            
        if not_valid == True: 
            aloc_W.append([req])
    return aloc_W
                 
                                     
def greedy(lista_Req,lista_Paths,node_List):
    aloc_Req=[]
    cash=0
    for req in lista_Req:
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        
        refresh_Links=[]
        check_Link=False

        
        for caminho in path_Ord:
            
            if check_Link == True:
                break
            check_Node=False
            check_Link=1
            
            for nodo in caminho:
                if len(node_List[nodo].fpga)==0:
                    continue
    
                best_part=check_Parts(node_List[nodo].fpga,req)
                if best_part==False:
                    continue
                else:
                    check_Node=True
                    break
                '''
                if parts[best_part].clb>=req.func.clb:
                    if parts[best_part].bram>=req.func.bram:
                        if parts[best_part].dsp>=req.func.dsp:
                            check_Node=True
                            fpga_num=a
                            break
                            '''
            
    #for p in path_Ord:
            if check_Node==False:
                continue
            
            for b,c in zip(caminho,caminho[1:]):
                lista_Check=check_Path(c,node_List[b].link,req)
                check_Link+=lista_Check[0]
                aux_Lista=b,lista_Check[1],lista_Check[2]
                refresh_Links.append(aux_Lista)
            if check_Link==len(caminho):
                check_Link=True
                break
            else:
                check_Link=False
                
    
        if check_Link and check_Node:
            
            aloc_Req.append(req)
            node_List[nodo].fpga[best_part[1]].pop(best_part[2])
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (node_List[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
        #cash+=req.price

    #ratio=len(aloc_Req)/len(lista_Req)
    

    return(len(aloc_Req), aloc_Req, cash)
    

def plot_Func(aloc_Desv,valor_Desv,dataset_index,dataset_req_Aloc,dataset_wrongrun):
    
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot(dataset_index, dataset_req_Aloc,color='tab:green',label='Abordagem Ciente de Partições') 
    ax.errorbar(dataset_index, dataset_req_Aloc, yerr=aloc_Desv, fmt="go")
    ax.plot(dataset_index, dataset_wrongrun, color = 'tab:red', label='Abordagem Não Ciente de Partições') 
    ax.errorbar(dataset_index, dataset_wrongrun, yerr=valor_Desv,fmt='ro')
    #plt.title('Numero de funcoes alocadas', fontweight="bold") 
    ax.grid() 
    ax.set_xlabel("Número de Nodos") 
    ax.set_ylabel("Funções Alocadas") 
    ax.set_ylim(0)
    
    plt.legend(loc=2)
    plt.savefig('Grafico_Func.png')
    plt.show()


def plot_Invalidos_fpga(lista_Invalidos,lista_Nodos_all, nr_Simul,lista_Wrong_run):
    
    
    #quebra a lista de req inv em lista de listas com tamanho de acordo com nr de simulaçoes por tamanho de rede
    result = [lista_Invalidos[i:i+nr_Simul] for i in range(0, len(lista_Invalidos), nr_Simul)]
    lista_Nodos= [lista_Nodos_all[i:i+nr_Simul] for i in range(0, len(lista_Nodos_all), nr_Simul)]
    lista_Req = [lista_Wrong_run[i:i+nr_Simul] for i in range(0, len(lista_Wrong_run), nr_Simul)]
    
    nodo_5=[]
    nodo_10=[]
    nodo_15=[]
    nodo_20=[]
    nodo_25=[]
    nodo_30=[]
    nodo_35=[]
    nodo_40=[]
    total=[0,0,0]
    nodos=[nodo_5,nodo_10,nodo_15,nodo_20,nodo_25,nodo_30,nodo_35,nodo_40,total]
  
    

    KU040_Total=[]
    KU095_Total=[]
    VU190_Total=[]
    
    
    
    for i in range(len(lista_Req)):
        for j in range(len(lista_Req[i])):
            for req in lista_Req[i][j]:
                for requisition in result[i][j]:
               
                        
                            if result[i][j] == [0,0,0]:
                                continue
                            
                            if req==requisition[0]:
                                lista_Req[i][j].remove(req)
    
    
    
    
    
    for step in lista_Nodos:
        KU040=0
        KU095=0
        VU190=0
        for inst in step:
            for nodo in inst:
                for fpga in nodo.fpga:
                        if len(fpga)==9:
                            VU190+=1
                        elif len(fpga)==6:
                            KU095+=1
                        elif len(fpga)==3 or len(fpga)==1:
                            KU040+=1
        KU040_Total.append(KU040)
        KU095_Total.append(KU095)
        VU190_Total.append(VU190)
    
    
    
    for nodo in range(len(KU040_Total)):
        nodos[nodo].append(KU040_Total[nodo])
        nodos[nodo].append(KU095_Total[nodo])
        nodos[nodo].append(VU190_Total[nodo])
        nodos[8][0]+=KU040_Total[nodo]
        nodos[8][1]+=KU095_Total[nodo]
        nodos[8][2]+=VU190_Total[nodo]


    KU040_Total=[]
    KU095_Total=[]
    VU190_Total=[]
   
    
    for step in lista_Req:
        KU040=0
        KU095=0
        VU190=0
        
        for inst in step:
            lista_ids=[]
            for req in inst:
                if req==0:
                    continue
                if req[2] in lista_ids:
                    continue
                else:
                    lista_ids.append(req[2])
                    if req[1]==3:
                        VU190+=1
                    elif req[1]==2:
                        KU095+=1
                    elif req[1]==1:
                        KU040+=1
        KU040_Total.append(KU040)
        KU095_Total.append(KU095)
        VU190_Total.append(VU190)

    soma_KU040=0
    soma_KU095=0
    soma_VU190=0
    
    for nodo in range(len(KU040_Total)):
        nodos[nodo][0]=(KU040_Total[nodo]/ nodos[nodo][0])
        soma_KU040+=KU040_Total[nodo]
        nodos[nodo][1]=KU095_Total[nodo]/ nodos[nodo][1]
        soma_KU095+=KU095_Total[nodo]
        nodos[nodo][2]=VU190_Total[nodo]/ nodos[nodo][2]
        soma_VU190+=VU190_Total[nodo]
    
    nodos[8][0]=soma_KU040/ nodos[8][0]
    nodos[8][1]=soma_KU095/ nodos[8][1]
    nodos[8][2]=soma_VU190/ nodos[8][2]
    
    barWidth = 0.1
    br1 = np.arange(3)
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    br5 = [x + barWidth for x in br4]
    br6 = [x + barWidth for x in br5]
    br7 = [x + barWidth for x in br6]
    br8 = [x + barWidth for x in br7]
    br9 = [x + barWidth for x in br8]
    
    plt.close()
    plt.bar(br1, nodos[0], color ='tab:red', width = barWidth,
            edgecolor ='k', label ='5')
    plt.bar(br2, nodos[1], color ='tab:orange', width = barWidth,
            edgecolor ='k', label ='10')
    plt.bar(br3, nodos[2], color ='tab:olive', width = barWidth,
            edgecolor ='k', label ='15')
    plt.bar(br4, nodos[3], color ='tab:green', width = barWidth,
            edgecolor ='k', label ='20')
    plt.bar(br5, nodos[4], color ='tab:blue', width = barWidth,
            edgecolor ='k', label ='25')
    plt.bar(br6, nodos[5], color ='tab:cyan', width = barWidth,
            edgecolor ='k', label ='30')
    plt.bar(br7, nodos[6], color ='tab:pink', width = barWidth,
            edgecolor ='k', label ='35')
    plt.bar(br8, nodos[7], color ='tab:purple', width = barWidth,
            edgecolor ='k', label ='40')
    plt.bar(br9, nodos[8], color ='tab:brown', width = barWidth,
            edgecolor ='k', label ='Média')
    
    
    labels=['KU040', 'KU095', 'VU190']
    # Adding Xticks
    plt.xlabel('Modelos FPGA')
    plt.ylabel('Fração de soluções inválidas')
    plt.legend(loc='upper left',  ncol = 3)
    plt.xticks(br1+0.4,labels)
    plt.ylim(0,0.7)
    plt.savefig('Grafico_FPGA.png')
    plt.show()
    

def plot_Solutions_inv(nr_Simul,lista_Invalidos):
    
    
    
    total_Inv=[]
    result = [lista_Invalidos[i:i+nr_Simul] for i in range(0, len(lista_Invalidos), nr_Simul)]
    
    for step in result:
        cont_Inv=0
        for inst in step:
            if inst == [0,0,0]:
                cont_Inv+=1
        total_Inv.append(cont_Inv)
        
    for step in range(len(result)):  
        total_Inv[step]=nr_Simul-total_Inv[step]
        total_Inv[step]=total_Inv[step]/nr_Simul
        
        
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot([5,10,15,20,25,30,35,40], total_Inv,color='tab:green')
    ax.grid() 
    ax.set_xlabel("Número de Nodos") 
    ax.set_ylabel("Fração de soluções inválidas") 
    plt.savefig('Grafico_Func_invalido.png')
    plt.show()
    

def main():

    modo=None
    while  (modo != '2' and modo != '1'):
        
        modo=input("1- Testar unitario\n2- Teste em escala\n")

        if modo == '1':
            nodos_G=int(input("Numero de nodos da rede:\n"))
            links_G=int(input("Numero de links da rede:\n"))
            req=int(input("Numero de requisicoes:\n"))
            gerador_Topologia(nodos_G,links_G)
            gerador_Req(nodos_G,req)
            lista_Paths,lista_Nodos=ler_Topologia()
            lista_Req=ler_Requisicoes()
            res_w=wrong_Run(lista_Req,lista_Paths,lista_Nodos)
            res_g=greedy(lista_Req,lista_Paths,lista_Nodos)
            
            #visualização apenas
            a=[]
            b=[]
            c=[]
            for i in res_w[1]:
                a.append(i.id)
            print("W:",a)
            for j in res_g[1]:
                b.append(j.id)
            print("G:",b)
            j=check_Wrong(res_w[1])
            for i in j:
                c.append(i[0].id)
            print("WW:",c)
            

        elif modo=='2':
            
            
            nr_Repeat=500

            print('Executando...')
            lista_Results_g=[]
            lista_Results_w=[]
            dataset_index=[]
            dataset_req_Aloc=[]
            dataset_wrongrun=[]
            aloc_Desv=[]
            #valor_Desv=[]
            wrong_Desv=[]
            lista_Invalidos=[]
            lista_Nodos_all=[]
            lista_Nodos_W=[]
            
            for index in range (5,45,5):
                req_Aloc_g=[]
                req_Aloc_w=[]
                nr_req_Aloc_W=[]
                #valor_Final=[]
                for cont in range(nr_Repeat):
                    size=index
                    nodos_G=size
                    links_G=int(size*1.2)
                    req=random.randint(int(size*1.5),int(size*3))
                    gerador_Topologia(nodos_G, links_G)
                    gerador_Req(nodos_G,req)
                    lista_Paths,lista_Nodos=ler_Topologia()
                    lista_Nodos_aux=copy.deepcopy(lista_Nodos)
                    lista_Req=ler_Requisicoes()
                    results_g=greedy(lista_Req,lista_Paths,lista_Nodos)
                    lista_Nodos=copy.deepcopy(lista_Nodos_aux)
                    results_w=wrong_Run(lista_Req,lista_Paths,lista_Nodos)
                    lista_Nodos=copy.deepcopy(lista_Nodos_aux)
                    aux=check_Wrong(results_w[1],lista_Paths)
                    if len(aux)==0:
                        aux=[0,0,0]
                    lista_Invalidos.append(aux)
                    lista_Nodos_all.append(lista_Nodos)

                    lista_Results_g.append({
                        "Teste"+str(index):{
                        "Lista Requisicoes": len(lista_Req),
                        "Requiscoes alocadas": results_g[0]},
                        "Nodos": len(lista_Nodos),
                        #"Valor": results_g[2]
                        })

                    req_Aloc_g.append(results_g[0])
                    #valor_Final.append(results[2])

                    lista_Results_w.append({
                        "Teste"+str(index):{ 
                        "Lista Requisicoes": len(lista_Req),
                        "Requiscoes alocadas": results_w[0]},
                        "Nodos": len(lista_Nodos),
                        })
                    
                    nr_req_Aloc_W.append(results_w[0])
                    lista_Nodos_W.append(results_w[1])
                aloc_Desv.append(stats.pstdev(req_Aloc_g))
                #valor_Desv.append(stats.pstdev(valor_Final))
                wrong_Desv.append(stats.pstdev(nr_req_Aloc_W))
                dataset_index.append(index)
                dataset_req_Aloc.append(stats.mean(req_Aloc_g))
                dataset_wrongrun.append(stats.mean(nr_req_Aloc_W))
                
               
            plot_Invalidos_fpga(lista_Invalidos,lista_Nodos_all,nr_Repeat,lista_Nodos_W)  
            plot_Solutions_inv(nr_Repeat, lista_Invalidos)
            plot_Func(aloc_Desv,wrong_Desv,dataset_index,dataset_req_Aloc,dataset_wrongrun)
            

            with open("Req_Alocadas.txt","w") as outfile:
                for result in results_g[1]:
                    outfile.write(str(result))
                    outfile.write('\n')
                
            with open("Req_Wrong.txt","w") as outfile:
                for result in results_w[1]:
                    outfile.write(str(result))
                    outfile.write('\n')

        
        else:
            print("Modo inválido")


if __name__ == "__main__":
    main()