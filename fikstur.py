#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import random

dosya = open('Takimlar.txt', 'w')          #Dosyalar
dosya2 = open('TakimlarRovans.txt')

count = 0
count2 = 0
countcift=0
hafta_numarasi=1

tekmaclarda_evsahipleri = []
tekmaclar = []
tekmaclar2 = []

ciftmaclarda_evsahipleri = []
ciftmaclar = []
ciftmaclar2 = []

def rövanslar(array,hafta_numarasi):       #15. haftadan sonra yapılacak rövans macları
    yeni_hafta = swap_cols(array, 0, 1)
    rövans_haftasi=hafta_numarasi+15
    count = 0
    count2 = 0
    for i in range(1, 9):
        dosya2.write("%d. hafta %d. maç: %d. Takım vs %d. Takım \n" % (rövans_haftasi, i, yeni_hafta[count, count2], yeni_hafta[count, count2 + 1]))
        count += 1

    dosya2.write("\n")

def swap_cols(arr, frm, to):             #Örnek 1. haftanın sütunları(ev sahibi-deplasman) değişir böylece 16. hafta elde edilir.
    arr[:,[frm, to]] = arr[:,[to, frm]]
    return arr

def eslesmeler():
    takimlar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    yerlestirilen_takimlar = []
    eslesmeler = np.zeros([8, 2])

    for i in range(8):            #1. haftanın ev sahiplerini belirlenir
        ev_sahibi_takim = random.choice(takimlar)
        if ev_sahibi_takim in yerlestirilen_takimlar:
            x=0
            while x == 0:
                ev_sahibi_takim = random.choice(takimlar)
                if ev_sahibi_takim not in yerlestirilen_takimlar:
                    x=1
                    eslesmeler[i, 0] = ev_sahibi_takim
                    yerlestirilen_takimlar.append(ev_sahibi_takim)
        else:
            eslesmeler[i, 0] = ev_sahibi_takim
            yerlestirilen_takimlar.append(ev_sahibi_takim)

    for i in range(8):              #1. haftanın deplasman takımları belirlenir
        deplasman_takim = random.choice(takimlar)
        if deplasman_takim in yerlestirilen_takimlar:
            x=0
            while x == 0:
                deplasman_takim = random.choice(takimlar)
                if deplasman_takim not in yerlestirilen_takimlar:
                    x = 1
                    eslesmeler[i, 1] = deplasman_takim
                    yerlestirilen_takimlar.append(deplasman_takim)
        else:
            eslesmeler[i, 1] = deplasman_takim
            yerlestirilen_takimlar.append(deplasman_takim)

    return eslesmeler

hafta1_eslesmeler = eslesmeler()
hafta1_eslesmeler = hafta1_eslesmeler.astype(int)

for i in range(1,9):
    dosya.write("%d. hafta %d. maç: %d. Takım vs %d. Takım \n" % (hafta_numarasi, i, hafta1_eslesmeler[count, count2], hafta1_eslesmeler[count, count2 + 1]))
    count += 1

dosya.write("\n")

rövanslar(hafta1_eslesmeler,hafta_numarasi)

for i in range(8):                         #1. haftanın deplasman ve ev sahibi takımları hafıza tutulur
    tekmaclarda_evsahipleri.append(hafta1_eslesmeler[i,0])
    ciftmaclarda_evsahipleri.append(hafta1_eslesmeler[i, 1])

hafta_numarasi+=1
for i in range(2,16):            #1. hafta referans alınarak 15. haftaya kadar düzenleme yapılır.

    count = 0
    count2 = 0
    yeni_hafta = np.zeros([8, 2])
    array1=[]
    array2=[]

    if i<9:            #İlk 8 hafta
        if i%2 == 0:                   #Çift numaralı maçlar
            if i == 2:
                tekmaclar = tekmaclarda_evsahipleri
                for i in range(8):
                    if i == 7:
                        ciftmaclar.insert(0, ciftmaclarda_evsahipleri[7])
                    else:
                        ciftmaclar.append(ciftmaclarda_evsahipleri[i])
            else:
                for i in range(8):
                    if i == 7:
                        ciftmaclar.insert(0, ciftmaclarda_evsahipleri[7-countcift])
                    else:
                        ciftmaclar.append(ciftmaclarda_evsahipleri[i])

            array1 = np.array(tekmaclar, dtype=np.int32)
            array2 = np.array(ciftmaclar, dtype=np.int32)

            for i in range(8):
                yeni_hafta[i][0] += array1[i]
                yeni_hafta[i][1] += array2[i]

        elif i%2 == 1:            #Tek numaraları maçlar
            for i in range(8):
                if i == 7:
                    ciftmaclar.insert(0, ciftmaclarda_evsahipleri[7 - countcift])
                else:
                    ciftmaclar.append(ciftmaclarda_evsahipleri[i])

            array1 = np.array(tekmaclar, dtype=np.int32)
            array2 = np.array(ciftmaclar, dtype=np.int32)

            for i in range(8):
                yeni_hafta[i][0] += array2[i]
                yeni_hafta[i][1] += array1[i]

        countcift += 1


    elif i in range(9, 16): #Örnek: 1. haftanın ev sahiplerinden bir takım 9. haftaya geldiklerinde 1. haftanın deplasman takımlarının
                            #       hepsi ile maç yapmış olur. Bu nedenle 9. haftadan sonra farklı bir gruplandırma yapılır.
        if i % 2 == 0:  # Çift numaralı maçlar
            for i in range(8):
                if i == 7:
                    ciftmaclar2.insert(0, tekmaclar[8-countcift])
                else:
                    ciftmaclar2.append(ciftmaclar[i])


            array1 = np.array(tekmaclar2, dtype=np.int32)
            array2 = np.array(ciftmaclar2, dtype=np.int32)

            for i in range(8):
                yeni_hafta[i][0] += array1[i]
                yeni_hafta[i][1] += array2[i]

        elif i % 2 == 1:  # Tek numaraları maçlar
            if i==9:
                ciftmaclar=ciftmaclar[:8]
                countcift = 0

                for i in range(0,8):
                    if i%2==0:
                        tekmaclar2.append(tekmaclar[i])
                    else:
                        tekmaclar2.append(ciftmaclar[i])

                for i in range(0,8):
                    if i%2==1:
                        ciftmaclar2.append(tekmaclar[i])
                    else:
                        ciftmaclar2.append(ciftmaclar[i])

                tekmaclar2.reverse()
                array1 = np.array(tekmaclar2, dtype=np.int32)
                array2 = np.array(ciftmaclar2, dtype=np.int32)

                for i in range(8):
                    yeni_hafta[i][0] += array2[i]
                    yeni_hafta[i][1] += array1[i]

            else:
                for i in range(8):
                    if i == 7:
                        ciftmaclar2.insert(0, ciftmaclar[8 - countcift])
                    else:
                        ciftmaclar2.append(ciftmaclar[i])

                array1 = np.array(tekmaclar2, dtype=np.int32)
                array2 = np.array(ciftmaclar2, dtype=np.int32)

                for i in range(8):
                    yeni_hafta[i][0] += array2[i]
                    yeni_hafta[i][1] += array1[i]

        countcift += 1

    for i in range(1,9):
            dosya.write("%d. hafta %d. maç: %d. Takım vs %d. Takım \n" % (hafta_numarasi,i,yeni_hafta[count,count2],yeni_hafta[count,count2+1]))
            count+=1
    dosya.write("\n")

    rövanslar(yeni_hafta, hafta_numarasi)
    hafta_numarasi+=1
