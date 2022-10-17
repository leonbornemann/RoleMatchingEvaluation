import pandas as pd

def getPRF(scoreName, group):
    tp = sum(((group[scoreName]) & (group['isSemanticRoleMatch'])))
    fp = sum(((group[scoreName]) & (~group['isSemanticRoleMatch'])))
    #tn = sum(((~group['isInCBRB']) & (~group['isSemanticRoleMatch'])))
    fn = sum((~group[scoreName] & group['isSemanticRoleMatch']))
    if(tp + fp ==0):
        precision=0
        recall=0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
    if(precision+recall == 0):
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1

def getPRFN(scoreName, group):
    p,r,f = getPRF(scoreName,group)
    n = sum(group[scoreName])
    return p,r,f,n

def getWEIGHTEDPRF(scoreName,df,bucketAndDatasetToWeight):
    grouped = df.groupby(['dataset','bucket'])
    weightedNominator = 0
    weightedDenominatorRecall = 0
    weightedDenominatorPrecision = 0
    for (dataset,bucketName),group in grouped:
        weight = bucketAndDatasetToWeight[(dataset,bucketName)]
        tp = weight*sum(((group[scoreName]) & (group['isSemanticRoleMatch'])))
        fp = weight*sum(((group[scoreName]) & (~group['isSemanticRoleMatch'])))
        #tn = sum(((~group['isInCBRB']) & (~group['isSemanticRoleMatch'])))
        fn = weight*sum((~group[scoreName] & group['isSemanticRoleMatch']))
        weightedNominator += tp
        weightedDenominatorRecall += (tp+fn)
        weightedDenominatorPrecision += (tp+fp)
    if(weightedDenominatorPrecision==0):
        precision=0
    else:
        precision = weightedNominator / weightedDenominatorPrecision
    if(weightedDenominatorRecall==0):
        recall=0
    else:
        recall = weightedNominator / weightedDenominatorRecall
    if(recall+precision==0):
        f1=0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1

def roundToPercentage(number):
    return str(int(round(100*number,2)))

def getPrecisionRecallF1String(df,scoreName,weighted,bucketAndDatasetToWeight):
    if(weighted):
        precision,recall,f1 = getWEIGHTEDPRF(scoreName,df,bucketAndDatasetToWeight)
    else:
        precision,recall,f1 = getPRF(scoreName,df)
    return roundToPercentage(precision) + "," + roundToPercentage(recall) + ", " + roundToPercentage(f1)

def getRecall(df,scoreName,weighted,bucketAndDatasetToWeight):
    if (weighted):
        _, recall, _ = getWEIGHTEDPRF(scoreName, df, bucketAndDatasetToWeight)
    else:
        _, recall, _ = getPRF(scoreName, df)
    return recall

def getRecallString(df,scoreName,weighted,bucketAndDatasetToWeight):
    recall = getRecall(df,scoreName,weighted,bucketAndDatasetToWeight)
    return roundToPercentage(recall)

def printPostiveRateForNonparametrizedMethodsDF(dataset,df,methodNames,weighted,bucketAndDatasetToWeight):
    dfWithMatches = df[df['isSemanticRoleMatch']]
    totalTP = len(dfWithMatches.index)
    strings = ",".join(list(map(lambda x: getPrecisionRecallF1String(df,x,weighted,bucketAndDatasetToWeight),methodNames)))
    print(dataset,totalTP,strings, sep=",")

def printRecallForNonparametrizedMethodsDF(dataset,df,methodNames,weighted,bucketAndDatasetToWeight):
    dfWithMatches = df[df['isSemanticRoleMatch']]
    totalTP = len(dfWithMatches.index)
    strings = ",".join(list(map(lambda x: getRecallString(df,x,weighted,bucketAndDatasetToWeight),methodNames)))
    print(dataset,totalTP,strings, sep=",")

def getRecallForNonparametrizedMethodsDF(df,methodNames,weighted,bucketAndDatasetToWeight):
    recalls = list(map(lambda x: getRecall(df,x,weighted,bucketAndDatasetToWeight),methodNames))
    return recalls



def printMacroAverages(param, df,methodNames,weighted,bucketAndDatasetToWeight):
    resultDF = getMetricsPerDataset(bucketAndDatasetToWeight, df, methodNames, weighted)
    byMethod = resultDF.groupby(['method']).agg({'precision':"mean",'recall':"mean",'f1':"mean"})
    metricNames = ['precision','recall','f1']
    #print(byMethod)
    print(param,",,",sep="",end="")
    for method in methodNames:
        for metric in metricNames:
            print(str(int(round(100*byMethod.loc[method][metric],2))),",",sep="",end="")


def getMetricsPerDataset(bucketAndDatasetToWeight, df, methodNames, weighted):
    groups = df.groupby(['dataset'])
    resultRows = []
    for (key), group in groups:
        for method in methodNames:
            if (weighted):
                precision, recall, f1 = getWEIGHTEDPRF(method, group, bucketAndDatasetToWeight)
            else:
                precision, recall, f1 = getPRF(method, group)
            resultRows.append({'dataset': key, 'method': method, 'precision': precision, 'recall': recall, 'f1': f1})
    resultDF = pd.DataFrame(resultRows)
    return resultDF


def printMacroAveragesRecall(param, df,methodNames,weighted,bucketAndDatasetToWeight):
    resultDF = getMetricsPerDataset(bucketAndDatasetToWeight, df, methodNames, weighted)
    byMethod = resultDF.groupby(['method']).agg({'recall':"mean"})
    metricNames = ['recall']
    #print(byMethod)
    print(param,",,",sep="",end="")
    for method in methodNames:
        for metric in metricNames:
            print(str(int(round(100*byMethod.loc[method][metric],2))),",",sep="",end="")

def getMacroAveragesRecall(df,methodNames,weighted,bucketAndDatasetToWeight):
    resultDF = getMetricsPerDataset(bucketAndDatasetToWeight, df, methodNames, weighted)
    byMethod = resultDF.groupby(['method']).agg({'recall': "mean"})
    # print(byMethod)
    result = []
    for method in methodNames:
        result.append(byMethod.loc[method]["recall"])
    return result

def getNAndRecallString(df, scoreName):
    _,r,_,n = getPRFN(scoreName,df)
    return str(n) + "," + str(int(round(100*r,2)))

def printNAndRecallForNonparametrizedMethodsDF(dataset,df,methods):
    dfWithMatches = df[df['isSemanticRoleMatch']]
    totalTP = len(dfWithMatches.index)
    strings = list(map(lambda x : getNAndRecallString(df,x),methods))
    # recallExactMatch = getNAndRecallString(df,'isInExactMatchBlocking')
    # recallSequence = getNAndRecallString(df,'isInSequenceBlocking')
    # recallSet = getNAndRecallString(df,'isInValueSetBlocking')
    # recallFullyCompatibleNoDecay = getNAndRecallString(df,'isInStrictBlockingNoDecay')
    # recallFullyCompatibleNoDecayWithFilter = getNAndRecallString(df,'isInStrictBlockingNoDecayWithFilter')
    print(dataset + "," + str(totalTP) + "," + ','.join(strings))
    #äprint(dataset,totalTP,recallExactMatch,recallSequence,recallSet,recallFullyCompatibleNoDecay,recallFullyCompatibleNoDecayWithFilter,sep=",")


def printMacroAveragesNAndRecall(name, df,methodNames):
    groups = df.groupby(['dataset'])
    resultRows = []
    for (key),group in groups:
        for method in methodNames:
            precision,recall,f1,n = getPRFN(method,group)
            resultRows.append({'dataset':key,'method':method,'recall':recall,'n':n})
    resultDF = pd.DataFrame(resultRows)
    byMethod = resultDF.groupby(['method']).agg({'recall':"mean",'n':"mean"})
    metricNames = ['n','recall']
    #print(byMethod)
    print(name, ",,", sep="", end="")
    for method in methodNames:
        print(str(int(round(100*byMethod.loc[method]["recall"],2))),",",sep="",end="")
        print(str(int(round(byMethod.loc[method]["n"],2))),",",sep="",end="")
        # for metric in metricNames:
        #     print(str(int(round(100*byMethod.loc[method][metric],2))),",",sep="",end="")
    #print(byMethod)

def printBestPrecisionAtTargetRecall(dsName,finalDFWithoutDatasetInGrouping, targetRecall):
    filtered = finalDFWithoutDatasetInGrouping[finalDFWithoutDatasetInGrouping['recall']>=targetRecall]
    filtered.sort_values("precision",ascending=False,inplace=True)
    print(dsName)
    print(filtered.head(1))


def getPrecisionForTargetRecall(df, targetRecall,methodName):
    dfFiltered = df[df['method']==methodName]
    filtered = dfFiltered[dfFiltered['recall'] >= targetRecall]
    filtered.sort_values("precision",ascending=False,inplace=True)
    if(len(filtered.index)==0):
        return 0
    else:
        return filtered.iloc[0]['precision'],filtered.iloc[0]

def getPrecisionForTargetRecallForMethod(df, targetRecall, methodName,weighted=True):
    if(not weighted):
        precision,recall,threshold = precision_recall_curve(df['isSemanticRoleMatch'], df[methodName])
    else:
        precision,recall,threshold = precision_recall_curve(df['isSemanticRoleMatch'], df[methodName], sample_weight=df["weight"])
    index = np.argmax(recall < targetRecall)-1
    return precision[index],threshold[index]


def printSetDifferences(set1, set2, firstName, secondName):
    cbrbMinusRM = set1.difference(set2)
    rmMinusCBRB = set2.difference(set1)
    inBoth = set1.intersection(set2)
    union = set1.union(set2)
    #cbrbMinusCBRBNoDecay = cbrb.difference(cbrbNoDecay)
    print(firstName,"-",secondName,":",len(cbrbMinusRM),"Percentage:",len(cbrbMinusRM) / len(union))
    print(secondName,"-",firstName,":",len(rmMinusCBRB),"Percentage:",len(rmMinusCBRB) / len(union))
    print(firstName,"INTERSECT",secondName,":",len(inBoth),"Percentage:",len(inBoth) / len(union))
    print("-------------------------------------------------------------")
    print(firstName,"-",secondName,":")
    for elem in cbrbMinusRM:
        print(elem)
    print(secondName,"-",firstName,":")
    for elem in rmMinusCBRB:
        print(elem)

def printForReductionRatioForMethodNames(methodNames, groupedByDS):
    for dataset, group in groupedByDS:
        printReductionRateForAllMethods(dataset, group, methodNames)

def printReductionRateForAllMethods(dataset, df, methodNames):
    for methodName in methodNames:
        thisDF = df[df[methodName]]
        print(dataset, methodName, len(thisDF.index), "/", len(df.index), "(",
              100 * (1-len(thisDF.index) / len(df.index)), "%)")

def printReductionRate(baseSet,method,nHits,nMisses,nAllPairs):
    estimatedCount = (nHits / (nHits+nMisses)) * nAllPairs
    print(method,"Reduction Rate to",baseSet,":",round(estimatedCount),"/",nAllPairs,method,1 - (estimatedCount / nAllPairs))

def getReductionRate(nHits,nMisses,nAllPairs):
    estimatedCount = (nHits / (nHits+nMisses)) * nAllPairs
    return estimatedCount,1 - (estimatedCount / nAllPairs)

def getReductionRateToOtherMethod(method1, method2, thisDF):
    method1Hits = len(thisDF[thisDF[method1]].index)
    method2Hits = len(thisDF[thisDF[method2]].index)
    return 1 - (method1Hits / method2Hits)

def printReductionRateToOtherMethod(method1, method2, thisDF):
    method1Hits = len(thisDF[thisDF[method1]].index)
    method2Hits = len(thisDF[thisDF[method2]].index)
    print(method1,"Reduction Rate to",method2,":",method1Hits,"/",method2Hits,1 - (method1Hits / method2Hits))
