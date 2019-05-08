# Written by Brandt Dillon, VexU team NJIT, 2018-2019 season
# This program computes the gears needed in a multi-stage gear train to reach a desired rpm output

vexGears = [12, 36, 60, 84]
vexSprockets = [6, 12, 18, 24, 30]
vex393Ratios = [1.0, 1.6, 2.4]
v5Ratios = [1.0, 2.0, 6.0]
names = ["Torque", "Speed", "Turbo"]

# function to select the gears given the gears, stages, and target
def gearSelect(gearsList, stages, target, tolerance):
    global out
    global iteration
    global percentTarget
    out = "\n"
    outList = []
    iteration = 0
    percent = 0
    percentTarget = 10
    tol = tolerance
    iterations = (len(gearsList))**(stages*2)
    print('Percent complete: ', end = "")
    def mainLoop(gearsList, num, tarR, lst, tr): #recursive loop for each stage
        for g1 in gearsList:
            lst.append(g1)
            for g2 in gearsList:
                if (g1 in vxGrs and g2 in vxGrs) or (g1 in vxSprckts and g2 in vxSprckts):
                    lst.append(g2)
                    trb = tr * float(g1) / float(g2)
                    if num > 1:
                        num = num - 1
                        mainLoop(gearsList, num, tarR, lst, trb)
                        num = num + 1
                    else: #deepest level
                        if trb < tarR + tol and trb > tarR - tol:
                            global out
                            ind = 0
                            lstTm = []
                            lstTm.extend(lst)
                            for entry in lst: #removes redundant 1:1 ratio stages
                                ind = ind + 1
                                if ind % 2 == 0:
                                    if lstTm[(ind-2)] == lstTm[(ind-1)]:
                                        del lstTm[ind-2]
                                        del lstTm[ind-2]
                                        ind = ind - 2
                            if lstTm not in outList: #prepares output for non-duplicate entrys           
                                outList.append(lstTm)
                                out = out + '{:04.2f}'.format(100 * trb * r) + ": " + str(lstTm) + '\n'           
                        global iteration    
                        iteration = iteration + 1
                        percent = int(100 * (iteration / iterations))
                        global percentTarget
                        if(percent >= percentTarget):         
                            print('X ', end = "")
                            percentTarget = percentTarget + 10
                    lst.pop()
                else:
                    iteration = iteration + (len(gearsList))**(2*(num-1))       
            lst.pop()
    mainLoop(gearsList, stages, target, [], 1.0)
    if (len(out) > 2):
        return out
    else:
        return "\nNo matching combinations within tolerance \n"

#Main loop for user input and printing results
while(True):
    try:
        desiredRatio = float(input("Desired RPM: "))/ 100.00
        ans = "n"
        while(ans == "n"):
            stage = int(input("Max number of stages: "))
            if(stage > 4):
                print("WARNING: Number of stages will cause large computational times.")
                ans = input("Proceed? ('Y' or 'N'):").lower()
            else:
                ans = "y"
        toler = 0.001 + float(input("RPM Tolerance: ")) / 100.00
        vexMode = input("Vex Motor ratios? ('393' or 'V5'): ").lower()
        typ = input("Press 'S' for sprockets, 'G' for gears, or 'C' for combination: ").lower()
        gearsEnt = []
        vxSprckts = []
        vxSprckts.extend(vexSprockets)
        vxGrs = []
        vxGrs.extend(vexGears)      
        while(True):
            s = input("Gears or sprockets to exclude (input teeth number, enter to continue): ")
            if s.isdigit():
                if typ == 's':
                    if int(s) in vxSprckts:
                        vxSprckts.remove(int(s))
                elif typ == 'g':
                    if int(s) in vxGrs:
                        vxGrs.remove(int(s))
                else:
                    s2 = input("Is this a gear or sprocket? (press 'g' or 's'):").lower()
                    if s2 == 's':
                        if int(s) in vxSprckts:
                            vxSprckts.remove(int(s))
                    else:
                        if int(s) in vxGrs:
                            vxGrs.remove(int(s))
            else:
                break        
        while(True):
            s = input("Custom size gears or sprockets (input teeth number, enter to continue): ")
            if s.isdigit():
                if typ == 's':
                    if int(s) not in vxSprckts:
                        vxSprckts.append(int(s))
                elif typ == 'g':
                    if int(s) not in vxGrs:
                        vxGrs.append(int(s))
                else:
                    s2 = input("Is this a gear or sprocket? (press 'g' or 's'):").lower()
                    if s2 == 's':
                        if int(s) not in vxSprckts:
                            vxSprckts.append(int(s))
                    else:
                        if int(s) not in vxGrs:
                            vxGrs.append(int(s))
            else:
                if typ == 's':
                    gearsEnt.extend(vxSprckts)
                elif typ == 'g':
                    gearsEnt.extend(vxGrs)
                else:
                    tmpL = []
                    tmpL.extend(vxSprckts)
                    tmpL.extend(vxGrs)
                    gearsEnt.extend(list(set(tmpL)))
                break    
        print("\n")
        
        #Prints the results
        i = 0
        if(vexMode == '393'):
            for r in vex393Ratios:
                print(names[i])
                print("Motor ratio: "+ str(r))
                print(gearSelect(gearsEnt, stage, float(desiredRatio)/float(r), toler/r)+"\n")
                i += 1
        elif(vexMode == 'v5'):
            for r in v5Ratios:
                print(names[i])
                print("Motor ratio: "+ str(r))
                print(gearSelect(gearsEnt, stage, float(desiredRatio)/float(r), toler/r)+"\n")
                i += 1
        else:
            print(gearSelect(gearsEnt, stage, desiredRatio, toler))

        #prints diagram of gear train set-up
        print("Output Diagram:")
        i = 0
        print("\n     [M]")
        while(i < stage):
            i += 1
            j = 0
            while(j < i):
                print("     ",end = "")
                j += 1
            print("[G"+str(2*i-1)+"] [G"+str(2*i)+"]",end = "\n")
        j = 0
        while(j < i):
            print("     ",end = "")
            j += 1
        print("      [O]\n")
        
        #asks user if they wish to continue
        answer = input("Continue? (Y/N): ")
        if answer.upper() == 'Y':
            print("\n")
            continue
        else:
            print("Goodbye!")
            break
    except ValueError:
       print("Invalid Input")
