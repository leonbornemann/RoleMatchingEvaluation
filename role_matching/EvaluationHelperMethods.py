import pandas as pd

datasetToAbbreviation = {
'austintexas' : 'AU',
'chicago' : 'CH',
'gov.maryland' : 'MD',
'oregon' : 'OR',
'utah' : 'UT',
'education' : 'ED',
'football' : 'FO',
'military' : 'MI',
'politics' : 'PO',
'tv_and_film' : 'TV'
}

def getBucketAndDatasetToWeight(pathTo95TVA2DVASample):
    dsNames = ["education", "football", "military", "politics", "tv_and_film"]
    datasets = list(map(lambda dsName: pd.read_csv(pathTo95TVA2DVASample + dsName + ".csv"),dsNames))
    largeSampleDF = pd.concat(datasets)
    largeSampleDF["[0.0,0.7) (<70%)"] = largeSampleDF['compatibilityPercentageNoDecay'] < 0.7
    largeSampleDF["[0.7,1.0) (70%)"] = ((largeSampleDF['compatibilityPercentageNoDecay'] >= 0.7) & (
                largeSampleDF['compatibilityPercentageNoDecay'] < 1.0))
    largeSampleDF["[1.0,1.0] (full)"] = largeSampleDF['compatibilityPercentageNoDecay'] == 1.0

    bucketNames = ["[0.0,0.7) (<70%)", "[0.7,1.0) (70%)", "[1.0,1.0] (full)"]
    bucketAndDatasetToWeight = {}
    bucketToWeight = {}
    for bucketName in bucketNames:
        for dsName in dsNames:
            thisDF = largeSampleDF[largeSampleDF['dataset'] == dsName]
            share = sum(thisDF[bucketName]) / len(thisDF.index)
            bucketAndDatasetToWeight[(dsName, bucketName)] = share
        share = sum(largeSampleDF[bucketName]) / len(largeSampleDF.index)
        bucketToWeight[bucketName] = share
        # print(dsName,bucketName, share)
    # Relative Sizes of the three buckets:
    return bucketAndDatasetToWeight,bucketToWeight


def readGoldStandard(path,pathTo95TVA2DVASample):
    df = pd.read_csv(path)
    df['isInCBRBNoDecay'] = ((df['compatibilityPercentageNoDecay'] >= 0.8))
    df['isInCBRBNoDecayWithTransitionFilter'] = (
            (df['compatibilityPercentageNoDecay'] >= 0.8) & df['hasTransitionOverlapNoDecay'])
    df['isInStrictBlockingNoDecayWithTransitionFilter'] = (
            (df['compatibilityPercentageNoDecay'] >= 1.0) & df['hasTransitionOverlapNoDecay'])
    df['isInStrictCompatibleBlocking'] = (df['strictlyCompatiblePercentage'] >= 1.0)
    # filters:
    addFilteredBlockingMethods(df)
    bucketAndDatasetToWeight, _ = getBucketAndDatasetToWeight(pathTo95TVA2DVASample)
    df['bucket'] = df['compatibilityPercentageNoDecay'].map(lambda x: getGroup(x))
    df["weight"] = df.apply(lambda x: getWeight(bucketAndDatasetToWeight, x), axis=1)
    return df
def readGoldStandardEvaluation(goldStandardPath,loadDiverseGoldStandard,pathTo95TVA2DVASample,missingValuePercentage=None):
    if(missingValuePercentage==None):
        if (loadDiverseGoldStandard):
            return readGoldStandard(goldStandardPath + "/dgs.csv",pathTo95TVA2DVASample)
        else:
            return readGoldStandard(goldStandardPath + "/rgs.csv", pathTo95TVA2DVASample)
    else:
        if (loadDiverseGoldStandard):
            return readGoldStandard(goldStandardPath + "/dgs/dgs_cleaned_" + str(missingValuePercentage) + ".csv",pathTo95TVA2DVASample)
        else:
            return readGoldStandard(goldStandardPath + "/rgs/rgs_cleaned_" + str(missingValuePercentage) + ".csv", pathTo95TVA2DVASample)
def addFilteredBlockingMethods(df):
    df['isInStrictBlockingNoDecayWithFilter'] = ((df['isInStrictBlockingNoDecay']) & df['hasTransitionOverlapNoDecay'])
    df['isInValueSetBlockingWithFilter'] = ((df['isInValueSetBlocking']) & df['hasTransitionOverlapNoDecay'])
    df['isInSequenceBlockingWithFilter'] = ((df['isInSequenceBlocking']) & df['hasTransitionOverlapNoDecay'])
    df['isInExactMatchBlockingWithFilter'] = ((df['isInExactMatchBlocking']) & df['hasTransitionOverlapNoDecay'])
    df['isInTSMBlockingWithFilter'] = ((df['isInTSMBlockingNoWildcard']) & df['hasTransitionOverlapNoDecay'])
    #TVA filterd
    df['isInStrictBlockingNoDecayWithDVAFilter'] = ((df['isInStrictBlockingNoDecay']) & (df['DVACount'] > 0))
    df['isInValueSetBlockingWithDVAFilter'] = ((df['isInValueSetBlocking']) & (df['DVACount'] > 0))
    df['isInSequenceBlockingWithDVAFilter'] = ((df['isInSequenceBlocking']) & (df['DVACount'] > 0))
    df['isInExactMatchBlockingWithDVAFilter'] = ((df['isInExactMatchBlocking']) & (df['DVACount'] > 0))
    df['isInTSMBlockingWithDVAFilter'] = ((df['isInTSMBlockingNoWildcard']) & (df['DVACount'] > 0))

def addRMMethodWithParameter(df,param,withTransitionFilter=False):
    if withTransitionFilter:
        df["isInRM" + str(param)] = ((df["exactSequenceMatchPercentage"] >= param) & (df['hasTransitionOverlapNoDecay']))
    else:
        df["isInRM" + str(param)] = (df["exactSequenceMatchPercentage"] >= param)

def addShortDataset(df):
    df['datasetShort'] = df['dataset'].map(lambda x: datasetToAbbreviation[x])

def getGroup(x):
    if(x==1.0):
        return "[1.0,1.0] (full)"
    elif(x >=0.7):
        return "[0.7,1.0) (70%)"
    else:
        return "[0.0,0.7) (<70%)"

def getShortGroup(x):
    if (x == 1.0):
        return "[1.0,1.0]"
    elif (x >= 0.7):
        return "[0.7,1.0)"
    else:
        return "[0.0,0.7)"


def getWeight(bucketAndDatasetToWeight,x):
    return bucketAndDatasetToWeight[(x['dataset'],x['bucket'])]

def addDVA2VA95Blocking(df):
    df['isInDVA2VA95Blocking'] = ((df["DVACount"] >=2) & (df["VACount"]>=95))

def addDVA2VA95Blocking(df):
    df['isInDVA2VA95Blocking'] = ((df["DVACount"] >=2) & (df["VACount"]>=95))
