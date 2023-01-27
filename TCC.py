import json
import random
from tracemalloc import Statistic
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass
import statistics as stats
import numpy as np


def gerador_Topologia(nro_Nodos, nro_Links):
    
    G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    
    while not(nx.is_connected(G)):
        G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    '''
    #visualiza grafico em tela
    
    subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show() 
    plt.savefig('Grafo.png')
    '''
    lista=list(G.edges)

    topologia_rede=[]

    fpga=[[27120,480,1824],[105300,1728,1080],[134280,2520,2880]]
    list_thro=[40,100,200,400]

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
            thro=random.choice(list_thro)
            lat= random.randint(20,200)
            lista_Links[c]={lista_Links[c]: {"Lat": lat, "Throughput": thro}}
       

        nro_fpga=random.randint(0,3)
        if nro_fpga!=0:
            
            for i in range(nro_fpga):

                lista_Part=[]
                sort_Fpga=random.choice(fpga)
                size_CLB = sort_Fpga[0]
                size_BRAM= sort_Fpga[1]
                size_DSP= sort_Fpga[2]

                part_p=[2640,96,192]
                part_m=[8640,144,576]
                part_g=[27120,480,1824]
                part_tipos=[part_p,part_m,part_g]
                '''
                max_CLB=15200
                max_BRAM=450

                nro_parts=random.randint(1,4)
                if sort_Fpga==0 and nro_fpga ==1:
                    clb=27120
                    bram=480
                    dsp=1368
                    lista_Part.append({"Part0": {"CLBs": clb, "BRAM":bram, "DSP": dsp }})
                    list(lista_Part)
                
                else:

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

                        ''' #modo antigo de particionamento


                part=0
                while size_CLB!=0 and size_BRAM!=0 and size_DSP!=0:
                    
                    sort_part=random.choice(part_tipos)
                    
                    if size_CLB-sort_part[0]<part_p[0]or size_BRAM-sort_part[1]<part_p[1] or size_DSP-sort_part[2]<part_p[2]:
                        clb=size_CLB
                        bram=size_BRAM
                        dsp=size_DSP
                        lista_Part.append({"Part"+str(part): {"CLBs": clb, "BRAM":bram, "DSP": dsp }})
                        size_DSP=0
                        size_BRAM=0
                        size_DSP=0
                                
                    else:
                        clb=sort_part[0]
                        bram=sort_part[1]
                        dsp=sort_part[2]
                        size_CLB=size_CLB-sort_part[0]
                        size_BRAM=size_BRAM-sort_part[1]
                        size_DSP=size_DSP-sort_part[2]
                        lista_Part.append({"Part"+str(part): {"CLBs": clb, "BRAM":bram, "DSP": dsp }})
                    
                    part+=1

                lista_Fpga.append(lista_Part)
                        
        topologia_rede.append({"Nodo"+str(a): {"FPGA": lista_Fpga, "Links": lista_Links}})
        
    with open ("topologia.json","w") as outfile:
        json.dump(topologia_rede, outfile, indent=4)


def check_Lat(nodo_S,nodo_D,lista_Paths,lista_Nodos):
    
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
        rand_nodo_S=random.randint(0,(nro_Nodos-1))
        rand_nodo_D=random.randint(0,(nro_Nodos-1))
        while rand_nodo_S==rand_nodo_D:
            rand_nodo_D=random.randint(0,nro_Nodos-1)
        
        aux=funcao[rand_fun]["implementacao"]
        valor=(aux['CLBs']+(aux['BRAM']*10))/50
        valor=valor *random.uniform(0.9,1.1)
        

        lat=check_Lat(rand_nodo_S,rand_nodo_D,lista_Caminhos, lista_Nodos)            
        
        requisicoes[k] = {
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
        c_Req=Req(nodo_S,nodo_D,lat,thro,c_Func,valor)
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
            lista_Parts=[]
            for part in fpga:
                
                nodo=str(*part.keys())

                clb=part[nodo]["CLBs"]
                bram=part[nodo]["BRAM"]
                dsp=part[nodo]["DSP"]
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
            lista_Fpga.append([nodo_id,clb,bram,dsp])
            
    with open ("topologia_wrong.json","w") as outfile:
        json.dump(lista_Fpga, outfile, indent=4)       
            
    aloc_Req=[]
    
    for req in lista_Req:
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        check_Node=False
        check_Link=1
        refresh_Links=[]
        device_id=None
        

        if lista_Nodos[req.init_node].fpga!=0:
            for i,device in enumerate(lista_Fpga):
                if int(device[0][4])==req.init_node:
                    if device[1]>=req.func.clb:
                        if device[2]>=req.func.bram:
                            if device[3]>=req.func.dsp:
                                check_Node=True
                                device_id=i  
                                break            
                            #checa se fpga tem recursos para alocar requisicao

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
        #checa se caminho tem capacidade de throughput
        
        if check_Link and check_Node:
            
            aloc_Req.append(req)
            lista_Fpga[device_id][1]=lista_Fpga[device_id][1]-req.func.clb
            lista_Fpga[device_id][2]=lista_Fpga[device_id][2]-req.func.bram
            lista_Fpga[device_id][3]=lista_Fpga[device_id][3]-req.func.dsp
            
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (lista_Nodos[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
            
        #se link e recursos satisfazem os requisitos, req eh alocada e atualiza-se recursos consumidos

    ratio=len(aloc_Req)/len(lista_Req)
    
    #print(lista_Fpga)
    print("Nr requisicoes alocadas W:",len(aloc_Req),"\nRatio:",round(ratio,2),"%")
    
    
    
    return(len(aloc_Req), aloc_Req)


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

def check_Parts(partitions, requisitions):
    pesos=[]
    for part in partitions:
        total_weight=0
        weight_clb=1
        weight_bram=50
        weight_dsp=20
        total_weight=(part.clb-requisitions.func.clb)*weight_clb
        total_weight+=(part.bram-requisitions.func.bram)*weight_bram
        total_weight+=(part.dsp-requisitions.func.dsp)*weight_dsp
        pesos.append(total_weight)
    index_min = min(range(len(pesos)), key=pesos.__getitem__)
    return(index_min) 
        

def greedy(lista_Req,lista_Paths,lista_Nodos):
    aloc_Req=[]
    cash=0
    for req in lista_Req:
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        check_Node=False
        check_Link=1
        refresh_Links=[]
        

        if len(lista_Nodos[req.init_node].fpga)!=0:
            for a,parts in enumerate(lista_Nodos[req.init_node].fpga):
                if len(parts)==0:
                    continue
                best_part=check_Parts(parts,req)
                if parts[best_part].clb>=req.func.clb:
                    if parts[best_part].bram>=req.func.bram:
                        if parts[best_part].dsp>=req.func.dsp:
                            check_Node=True
                            fpga_num=a
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
            lista_Nodos[req.init_node].fpga[fpga_num].pop(best_part)
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (lista_Nodos[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
            cash+=req.price


    ratio=len(aloc_Req)/len(lista_Req)


        
    #print("Requisicoes alocadas:",aloc_Req)
    print("Nr requisicoes alocadas G:",len(aloc_Req),"\nRatio:",round(ratio,2),"%")

    return(len(aloc_Req), aloc_Req, cash)
    

def plot(aloc_Desv,valor_Desv,dataset_index,dataset_req_Aloc,dataset_wrongrun):
    '''
    test=zip(dataset_1,dataset_2,dataset_3)
    lista_test=list(sorted(test, key=lambda teste: teste[0]))
    dataset_1,dataset_2,dataset_3 = zip(*lista_test)
    '''
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot(dataset_index, dataset_req_Aloc,color='tab:green') 
    ax.errorbar(dataset_index, dataset_req_Aloc, yerr=aloc_Desv, fmt="go")
    ax2 = ax.twinx() 
    ax2.plot(dataset_index, dataset_wrongrun, color = 'tab:red') 
    ax2.errorbar(dataset_index, dataset_wrongrun, yerr=valor_Desv,fmt='ro')
    plt.title('Numero de funcoes alocadas', fontweight="bold") 
    ax.grid() 
    ax.set_xlabel("Numero de Nodos") 
    ax.set_ylabel(r"Nossa abordagem",color='tab:green') 
    ax2.set_ylabel(r"Abordagem conflitante", color='tab:red') 
    ax2.set_ylim(0, 100) 
    ax.set_ylim(0, 100)
    #ax.set_xlim(0,40)
    
    plt.savefig('Resultado.png')
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
            print("Wrong:",res_w[1])
            res_g=greedy(lista_Req,lista_Paths,lista_Nodos)
            print("Greedy:",res_g[1])
            

        elif modo=='2':

            lista_Results_g=[]
            lista_Results_w=[]
            dataset_index=[]
            dataset_req_Aloc=[]
            dataset_wrongrun=[]
            aloc_Desv=[]
            #valor_Desv=[]
            wrong_Desv=[]

            for index in range (5,45,5):
                req_Aloc_g=[]
                req_Aloc_w=[]
                #valor_Final=[]
                for cont in range(50):
                    size=index
                    nodos_G=size
                    links_G=int(size*1.2)
                    req=random.randint(int(size*1.5),int(size*3))
                    gerador_Topologia(nodos_G, links_G)
                    gerador_Req(nodos_G,req)
                    lista_Paths,lista_Nodos=ler_Topologia()
                    lista_Req=ler_Requisicoes()
                    results_g=greedy(lista_Req,lista_Paths,lista_Nodos)
                    results_w=wrong_Run(lista_Req,lista_Paths,lista_Nodos)
                    
                    
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
                    req_Aloc_w.append(results_w[0])

                aloc_Desv.append(stats.pstdev(req_Aloc_g))
                #valor_Desv.append(stats.pstdev(valor_Final))
                wrong_Desv.append(stats.pstdev(req_Aloc_w))
                dataset_index.append(index)
                dataset_req_Aloc.append(stats.mean(req_Aloc_g))
                dataset_wrongrun.append(stats.mean(req_Aloc_w))
                
               
            plot(aloc_Desv,wrong_Desv,dataset_index,dataset_req_Aloc,dataset_wrongrun)

            with open ("Req_Alocadas.json","w") as outfile:
                json.dump(lista_Results_g, outfile,indent=4)
                
            with open ("Req_Wrong.json","w") as outfile:
                json.dump(lista_Results_w, outfile,indent=4)

        
        else:
            print("Modo inválido")


if __name__ == "__main__":
    main()

